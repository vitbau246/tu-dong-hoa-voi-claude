"""Tập 1 - Tạo thư mục Downloads lộn xộn để demo.

Chạy:  python chuan-bi.py
Kết quả: ./demo/Downloads (khoảng 300 file, có file trùng nội dung, ngày sửa trải 2024-2026)
         ./dap-an.json (đáp án để đối chiếu)
Chạy lại bất cứ lúc nào để reset demo (thư mục demo cũ sẽ bị xóa).
"""
import hashlib
import json
import os
import random
import shutil
import struct
import sys
import zipfile
import zlib
from datetime import datetime, timedelta
from pathlib import Path

from docx import Document
from openpyxl import Workbook
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo" / "Downloads"
rng = random.Random(2026)

def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def png(path, w, h, color):
    raw = b"".join(b"\x00" + bytes(color) * w for _ in range(h))
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def pdf(path, text):
    c = canvas.Canvas(str(path))
    c.drawString(72, 750, text)
    c.drawString(72, 730, f"Ma tai lieu: {rng.randint(100000, 999999)}")
    c.save()


def docx(path, text):
    d = Document()
    d.add_heading(text, 1)
    d.add_paragraph(f"Nội dung mẫu số {rng.randint(1000, 9999)}.")
    d.save(path)


def xlsx(path, text):
    wb = Workbook()
    ws = wb.active
    ws.append([text])
    for i in range(5):
        ws.append([f"Dòng {i + 1}", rng.randint(1, 10_000_000)])
    wb.save(path)


def zipf(path, text):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("readme.txt", f"{text} {rng.random()}")


def raw(path, text):
    path.write_bytes(text.encode() + os.urandom(rng.randint(2_000, 20_000)))


def txt(path, text):
    path.write_text(f"{text}\nGhi chú {rng.randint(1, 99999)}\n", encoding="utf-8")


def anh(path, text):
    png(path, rng.randint(40, 160), rng.randint(40, 160), [rng.randint(0, 255) for _ in range(3)])


# (loại, đuôi, hàm tạo, danh sách tên gốc, số lượng)
NHOM = [
    ("pdf", ".pdf", pdf, ["hoa-don-dien-T{m}", "Cong van so {n}-CV", "scan_{n}", "To trinh {n}", "Bien ban hop {n}",
                          "HopDong_{n}", "Huong dan su dung {n}", "sao-ke-{m}-2025"], 55),
    ("word", ".docx", docx, ["Bao cao tuan {n}", "Ke hoach Q{q}", "Giấy mời họp {n}", "Đề xuất mua sắm {n}",
                             "Quyet dinh {n}", "Bien ban ban giao {n}"], 38),
    ("excel", ".xlsx", xlsx, ["Doanh thu T{m}", "Bang luong T{m}", "Danh sach khach hang {n}", "Theo doi cong viec",
                              "Bao gia {n}", "Chi phi Q{q}"], 42),
    ("pptx", ".pptx", raw, ["Slide gioi thieu {n}", "Thuyet trinh Q{q}", "Dao tao noi bo {n}"], 14),
    ("anh", ".png", anh, ["Screenshot 2025-{m:02d}-{d:02d} {n}", "IMG_{n}", "anh-hop-to-{n}", "z{n}_zalo"], 62),
    ("anh", ".jpg", raw, ["DSC_{n}", "chup-man-hinh-{n}", "bien-lai-{n}"], 25),
    ("nen", ".zip", zipf, ["tai-lieu-{n}", "Ho so du thau {n}", "backup_{n}"], 14),
    ("caidat", ".exe", raw, ["ZoomInstaller{n}", "setup_unikey_{n}", "ChromeSetup{n}"], 9),
    ("caidat", ".msi", raw, ["teams-setup-{n}", "office-update-{n}"], 4),
    ("video", ".mp4", raw, ["record_{n}", "Video hop {n}"], 8),
    ("amthanh", ".m4a", raw, ["ghi-am-cuoc-hop-{n}", "voice_{n}"], 5),
    ("khac", ".txt", txt, ["ghi chu {n}", "new {n}", "pass wifi {n}"], 9),
    ("khac", ".csv", txt, ["export_{n}", "data ({n})"], 6),
]

SO_TRUNG = 27  # số bản sao trùng nội dung cần Claude phát hiện


def ngau_nhien_ngay():
    goc = datetime(2024, 1, 3)
    return goc + timedelta(days=rng.randint(0, 1030), hours=rng.randint(7, 22), minutes=rng.randint(0, 59))


def ten_moi(mau):
    return mau.format(n=rng.randint(100, 9999), m=rng.randint(1, 12), q=rng.randint(1, 4), d=rng.randint(1, 28))


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def main():
    lam_moi(DEMO.parent)
    DEMO.mkdir(parents=True)

    tao = []
    for loai, duoi, ham, mau_ten, so in NHOM:
        for _ in range(so):
            ten = ten_moi(rng.choice(mau_ten)) + duoi
            while (DEMO / ten).exists():
                ten = ten_moi(rng.choice(mau_ten)) + duoi
            p = DEMO / ten
            ham(p, ten)
            tao.append((p, loai))

    # Tạo file trùng nội dung: kiểu "(1)", " - Copy", hoặc tên hoàn toàn khác
    nguon = rng.sample([p for p, loai in tao if loai not in ("caidat",)], SO_TRUNG)
    nhom_trung = []
    for i, p in enumerate(nguon):
        kieu = i % 3
        if kieu == 0:
            ten = f"{p.stem} (1){p.suffix}"
        elif kieu == 1:
            ten = f"{p.stem} - Copy{p.suffix}"
        else:
            ten = f"tai-ve-{rng.randint(10000, 99999)}{p.suffix}"
        q = DEMO / ten
        shutil.copyfile(p, q)
        nhom_trung.append({"goc": p.name, "ban_sao": q.name})

    # Ngày sửa đổi ngẫu nhiên 2024 - 10/2026
    nam = {}
    for p in DEMO.iterdir():
        t = ngau_nhien_ngay().timestamp()
        os.utime(p, (t, t))
        y = datetime.fromtimestamp(t).year
        nam[y] = nam.get(y, 0) + 1

    # Đếm lại theo đuôi file và kiểm chứng số file trùng bằng hash
    theo_duoi = {}
    hashes = {}
    for p in DEMO.iterdir():
        theo_duoi[p.suffix] = theo_duoi.get(p.suffix, 0) + 1
        hashes.setdefault(md5(p), []).append(p.name)
    so_ban_thua = sum(len(v) - 1 for v in hashes.values())
    tong_dung_luong = sum(p.stat().st_size for p in DEMO.iterdir())

    dap_an = {
        "tong_so_file": sum(theo_duoi.values()),
        "tong_dung_luong_MB": round(tong_dung_luong / 1_048_576, 1),
        "theo_duoi_file": dict(sorted(theo_duoi.items())),
        "theo_nam_sua_doi": dict(sorted(nam.items())),
        "so_ban_sao_thua_trung_noi_dung": so_ban_thua,
        "so_nhom_trung": sum(1 for v in hashes.values() if len(v) > 1),
        "vi_du_trung": nhom_trung[:6],
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dap_an, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
