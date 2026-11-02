"""Tập 11 - Chuẩn bị đề bài nghiên cứu + một "bản nháp của đồng nghiệp" có trích dẫn sai để kiểm chứng.

Chạy:  python chuan-bi.py              -> demo/de-bai.md, demo/ban-nhap-dong-nghiep/{bao-cao.md, nguon.csv}, dap-an.json
       python chuan-bi.py --giai-phap  -> chép thêm kiem-chung-trich-dan.py + .claude/skills/nghien-cuu/

Bản nháp lấy câu THẬT từ Wikipedia ngay lúc chạy (nên luôn khớp nguồn hiện tại), rồi gài:
  - 2 trích dẫn bị sửa con số
  - 1 trích dẫn bịa hoàn toàn (nguồn không hề có)
"""
import csv
import json
import random
import re
import shutil
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
NGUON_URL = "https://vi.wikipedia.org/wiki/Kinh_t%E1%BA%BF_Vi%E1%BB%87t_Nam"
rng = random.Random(11)

DE_BAI = """# Đề bài nghiên cứu

**Câu hỏi:** Thị trường thương mại điện tử (TMĐT) bán lẻ Việt Nam năm 2025 lớn cỡ nào, tăng trưởng ra sao,
và những nền tảng nào đang dẫn đầu?

**Người đọc:** Ban Giám đốc một công ty bán lẻ văn phòng phẩm đang cân nhắc bán hàng trên sàn TMĐT.

**Yêu cầu bắt buộc**
1. Mọi con số phải có nguồn (đường dẫn) và trích dẫn NGUYÊN VĂN câu chứa con số đó.
2. Ưu tiên nguồn gốc: cơ quan nhà nước, báo cáo của tổ chức nghiên cứu, sau đó mới tới báo chí.
3. Nếu các nguồn đưa ra số khác nhau: nêu cả hai, không tự chọn một.
4. Tách rõ: SỐ LIỆU (có nguồn) và NHẬN ĐỊNH (của người viết).
5. Độ dài báo cáo: tối đa 1 trang A4 + bảng nguồn.
"""


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def cau_co_so(url):
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (video huong dan)"}, timeout=30).content
    soup = BeautifulSoup(html, "lxml")
    cau = []
    for p in soup.select("#mw-content-text p"):
        for t in p.find_all("sup"):
            t.decompose()  # bỏ chú thích [1], [2] cho câu sạch
        for c in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", p.get_text(" ")).strip()):
            if re.search(r"\d{2,}", c) and 60 <= len(c) <= 220 and "(" not in c:
                cau.append(c.strip())
    return cau


def sua_so(cau):
    """Đổi một con số trong câu (giống lỗi nhớ nhầm / gõ nhầm số liệu)."""
    so = re.findall(r"\d+(?:[.,]\d+)?", cau)
    goc = max(so, key=len)
    moi = list(goc)
    i = max(j for j, ch in enumerate(moi) if ch.isdigit())
    moi[i] = str((int(moi[i]) + rng.randint(2, 7)) % 10)
    moi = "".join(moi)
    return cau.replace(goc, moi, 1), goc, moi


def main():
    lam_moi(DEMO)
    (DEMO / "de-bai.md").write_text(DE_BAI, encoding="utf-8")
    nhap = DEMO / "ban-nhap-dong-nghiep"
    nhap.mkdir()

    cau = cau_co_so(NGUON_URL)
    if len(cau) < 8:
        sys.exit(f"Chỉ lấy được {len(cau)} câu từ nguồn, kiểm tra kết nối mạng.")
    chon = cau[:8]

    dong, sai = [], []
    for i, c in enumerate(chon, 1):
        trich = c
        if i in (3, 6):
            trich, goc, moi = sua_so(c)
            sai.append({"ma": f"N{i}", "loi": f"Sửa số {goc} → {moi}"})
        dong.append({"ma": f"N{i}", "nhan_dinh": trich[:80], "trich_dan": trich, "url": NGUON_URL})
    dong.append({"ma": "N9", "nhan_dinh": "Quy mô TMĐT bán lẻ đạt 32 tỷ USD (bịa)",
                 "trich_dan": "Quy mô thương mại điện tử bán lẻ của Việt Nam năm 2025 đạt khoảng 32 tỷ USD, tăng 27% so với năm trước.",
                 "url": NGUON_URL})
    sai.append({"ma": "N9", "loi": "Trích dẫn bịa: nguồn không có câu này"})

    with open(nhap / "nguon.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["ma", "nhan_dinh", "trich_dan", "url"])
        w.writeheader()
        w.writerows(dong)
    (nhap / "bao-cao.md").write_text(
        "# Tổng quan kinh tế Việt Nam (bản nháp của đồng nghiệp)\n\n"
        + "\n".join(f"- {d['trich_dan']} [{d['ma']}]" for d in dong)
        + "\n\n_Nguồn: xem nguon.csv_\n", encoding="utf-8")

    if "--giai-phap" in sys.argv:
        shutil.copy(GOC / "giai-phap" / "kiem-chung-trich-dan.py", DEMO / "kiem-chung-trich-dan.py")
        shutil.copytree(GOC / "giai-phap" / ".claude", DEMO / ".claude")
        print("Đã chép kiem-chung-trich-dan.py và skill nghien-cuu vào demo/")

    dap_an = {"nguon": NGUON_URL, "so_trich_dan": len(dong), "trich_dan_sai": sai,
              "ky_vong": "6 KHỚP · 3 KHÔNG THẤY (N3, N6 sai số; N9 bịa)"}
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dap_an, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
