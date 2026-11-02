"""Kiểm chứng trích dẫn: mở lại TỪNG nguồn gốc và xác nhận câu trích có thật sự nằm trong đó.

Vì sao cần: công cụ WebFetch của Claude tóm tắt trang bằng một model riêng (mất mát thông tin),
và AI có thể diễn đạt lại / nhớ nhầm con số. Script này tải trang NGUYÊN BẢN và so khớp từng trích dẫn.

Dùng:   python kiem-chung-trich-dan.py nguon.csv  [nguon-2.csv ...]
Đầu vào: CSV (UTF-8) có các cột: ma, nhan_dinh, trich_dan, url
Đầu ra:  kiem-chung.csv (cùng thư mục file đầu tiên) + bảng tóm tắt
Trạng thái: KHỚP (nguyên văn) | GẦN ĐÚNG (>= 85%, cần xem lại) | KHÔNG THẤY | KHÔNG TẢI ĐƯỢC
"""
import csv
import io
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
HEADERS = {"User-Agent": "Mozilla/5.0 (kiem-chung-trich-dan; +video huong dan)"}


def chuan_hoa(s):
    s = unicodedata.normalize("NFC", s).lower()
    s = re.sub(r"[“”\"'‘’«»]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def tai_van_ban(url, bo_nho={}):
    if url in bo_nho:
        return bo_nho[url]
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    if "pdf" in r.headers.get("content-type", "") or url.lower().endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(io.BytesIO(r.content)) as pdf:
            text = " ".join(p.extract_text() or "" for p in pdf.pages)
    else:
        soup = BeautifulSoup(r.content, "lxml")
        for t in soup(["script", "style", "noscript"]):
            t.decompose()
        text = soup.get_text(" ")
    bo_nho[url] = chuan_hoa(text)
    return bo_nho[url]


def do_khop(trich, van_ban):
    """Trả về (tỉ lệ khớp tốt nhất 0..1, đoạn văn bản khớp nhất) của câu trích trong nguồn."""
    if trich in van_ban:
        return 1.0, trich
    # Neo theo các "từ hiếm" (dài nhất) để tìm vùng ứng viên, rồi so mờ quanh đó
    tu = sorted(set(trich.split()), key=len, reverse=True)[:4]
    tot_nhat, vung_tot, n = 0.0, "", len(trich)
    for neo in tu:
        for m in re.finditer(re.escape(neo), van_ban):
            vung = van_ban[max(0, m.start() - n): m.end() + n]
            sm = SequenceMatcher(None, trich, vung, autojunk=False)
            ty_le = sum(b.size for b in sm.get_matching_blocks()) / n
            if ty_le > tot_nhat:
                tot_nhat, vung_tot = ty_le, vung
    return tot_nhat, vung_tot


def so_trong(s):
    return re.findall(r"\d+(?:[.,]\d+)*", s)


def main(duong_dan):
    dong = []
    for p in duong_dan:
        with open(p, encoding="utf-8-sig") as f:
            dong += list(csv.DictReader(f))
    ket_qua = []
    for d in dong:
        trich = chuan_hoa(d["trich_dan"])
        try:
            van_ban = tai_van_ban(d["url"].strip())
            ty_le, vung = do_khop(trich, van_ban)
            if ty_le >= 0.999:
                tt = "KHỚP"
            elif ty_le >= 0.85:
                # Gần đúng nhưng con số khác với ĐOẠN nguồn tương ứng thì coi là KHÔNG THẤY (sai số liệu là lỗi nặng)
                so_thieu = [x for x in so_trong(trich) if x not in so_trong(vung)]
                tt = "KHÔNG THẤY" if so_thieu else "GẦN ĐÚNG"
                if so_thieu:
                    d["ghi_chu"] = f"Số không có trong nguồn: {', '.join(so_thieu)}"
            else:
                tt = "KHÔNG THẤY"
        except Exception as e:  # trang chặn bot, cần JavaScript, hết thời gian...
            ty_le, tt = 0.0, "KHÔNG TẢI ĐƯỢC"
            d["ghi_chu"] = type(e).__name__
        ket_qua.append({**d, "trang_thai": tt, "ty_le_khop": f"{min(ty_le, 1):.1%}", "ghi_chu": d.get("ghi_chu", "")})

    out = Path(duong_dan[0]).with_name("kiem-chung.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(ket_qua[0].keys()))
        w.writeheader()
        w.writerows(ket_qua)

    dem = {}
    for k in ket_qua:
        dem[k["trang_thai"]] = dem.get(k["trang_thai"], 0) + 1
        dau = {"KHỚP": "✅", "GẦN ĐÚNG": "🟡", "KHÔNG THẤY": "❌", "KHÔNG TẢI ĐƯỢC": "⚠️"}[k["trang_thai"]]
        print(f"{dau} [{k['ma']}] {k['trang_thai']:15} {k['ty_le_khop']:>6}  {k['nhan_dinh'][:60]}  {k['ghi_chu']}")
    print(f"\nTổng {len(ket_qua)} trích dẫn: " + " · ".join(f"{v} {k}" for k, v in dem.items()) + f"\n→ {out}")
    sys.exit(1 if dem.get("KHÔNG THẤY") else 0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
