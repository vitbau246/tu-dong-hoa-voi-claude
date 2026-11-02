"""Tập 14 - Website đối thủ (hư cấu) + bảng giá của mình, để dựng hệ thống theo dõi giá tự động.

Chạy:  python chuan-bi.py              -> NGÀY 1: demo/web-doi-thu/index.html, demo/bang-gia-cua-minh.csv, dap-an.json
       python chuan-bi.py --ngay 2     -> đổi website sang NGÀY 2 (giữ nguyên các file khác) để mô phỏng đối thủ đổi giá
       python chuan-bi.py --giai-phap  -> chép thêm theo-doi.py
Mở web: python -m http.server 8001 -d demo/web-doi-thu

Thay đổi gài sẵn từ ngày 1 -> ngày 2 (xem dap-an.json):
  3 giảm giá mạnh (mặt hàng chủ lực) · 2 tăng giá · 2 hết hàng · 1 có hàng trở lại · 2 sản phẩm mới · 1 ngừng bán
"""
import csv
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
WEB = DEMO / "web-doi-thu"

# (mã, tên, giá ngày 1, còn hàng ngày 1, giá của mình)
SP = [
    ("VP-001", "Ghế công thái học Ergo Pro", 5_490_000, True, 5_400_000),
    ("VP-002", "Máy in laser HP 107w", 2_890_000, True, 2_850_000),
    ("VP-003", "Màn hình 24 inch IPS", 3_350_000, True, 3_290_000),
    ("VP-004", "Bàn làm việc 1m2 chân sắt", 2_790_000, True, 2_750_000),
    ("VP-005", "Hộp mực HP 107A", 710_000, True, 690_000),
    ("VP-006", "Giấy A4 Double A (thùng)", 395_000, True, 385_000),
    ("VP-007", "Bàn phím cơ không dây", 1_190_000, True, 1_150_000),
    ("VP-008", "Chuột không dây Logitech M331", 335_000, True, 320_000),
    ("VP-009", "Máy hủy tài liệu 3S16", 2_190_000, True, 2_150_000),
    ("VP-010", "Tủ hồ sơ sắt 4 ngăn", 3_690_000, False, 3_650_000),
    ("VP-011", "Đèn bàn LED chống cận", 435_000, True, 420_000),
    ("VP-012", "Bảng trắng 1.2x2.4m", 1_290_000, True, 1_250_000),
    ("VP-013", "Bút ký Parker Jotter", 465_000, True, 450_000),
    ("VP-014", "Máy chiếu Epson EB-X51", 12_200_000, True, 11_900_000),
    ("VP-015", "Ghế xoay lưới văn phòng", 1_420_000, True, 1_390_000),
]
NGAY2 = {
    "giam_gia": {"VP-001": 4_590_000, "VP-002": 2_450_000, "VP-003": 2_890_000},
    "tang_gia": {"VP-006": 425_000, "VP-005": 750_000},
    "het_hang": ["VP-008", "VP-013"],
    "co_hang_lai": ["VP-010"],
    "moi": [("VP-016", "Ghế công thái học Ergo Lite", 3_290_000), ("VP-017", "Combo 5 thùng giấy A4", 1_850_000)],
    "ngung": ["VP-012"],
}


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def vnd(x):
    return f"{x:,}".replace(",", ".") + "₫"


def ghi_web(ds, ngay):
    the = "".join(
        f'<article class="item" data-sku="{m}"><h3 class="name">{t}</h3><p class="sku">SKU: {m}</p>'
        f'<p class="price">{vnd(g)}</p><p class="stock {"in" if c else "out"}">{"Còn hàng" if c else "Tạm hết hàng"}</p></article>'
        for m, t, g, c in ds)
    WEB.mkdir(parents=True, exist_ok=True)
    (WEB / "index.html").write_text(
        '<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Thiết bị văn phòng Đối Thủ (DEMO)</title>'
        "<style>body{font-family:Segoe UI,Arial;margin:30px;background:#fafafa}.grid{display:grid;grid-template-columns:"
        "repeat(auto-fill,minmax(220px,1fr));gap:14px}.item{background:#fff;padding:14px;border-radius:8px;box-shadow:0 1px 3px #0002}"
        ".price{color:#d00;font-weight:700;font-size:18px}.out{color:#999}.in{color:#080}.sku{color:#888;font-size:12px}</style></head>"
        f'<body><h1>Thiết bị văn phòng Đối Thủ (DEMO)</h1><p>Cập nhật: ngày {ngay}</p><div class="grid">{the}</div>'
        '<p style="color:#999;font-size:11px">Website hư cấu phục vụ video hướng dẫn.</p></body></html>', encoding="utf-8")


def main():
    ngay = 2 if "--ngay" in sys.argv and sys.argv[sys.argv.index("--ngay") + 1] == "2" else 1
    ds = [(m, t, g, c) for m, t, g, c, _ in SP]
    if ngay == 2:
        moi = []
        for m, t, g, c in ds:
            if m in NGAY2["ngung"]:
                continue
            g = NGAY2["giam_gia"].get(m, NGAY2["tang_gia"].get(m, g))
            c = False if m in NGAY2["het_hang"] else (True if m in NGAY2["co_hang_lai"] else c)
            moi.append((m, t, g, c))
        moi += [(m, t, g, True) for m, t, g in NGAY2["moi"]]
        ghi_web(moi, 2)
        print("Website đối thủ đã chuyển sang NGÀY 2")
        return

    lam_moi(DEMO)
    ghi_web(ds, 1)
    with open(DEMO / "bang-gia-cua-minh.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["sku_doi_thu", "ten", "gia_cua_minh"])
        for m, t, _, _, gm in SP:
            w.writerow([m, t, gm])
    if "--giai-phap" in sys.argv:
        shutil.copy(GOC / "giai-phap" / "theo-doi.py", DEMO / "theo-doi.py")
        shutil.copy(GOC / "giai-phap" / "dang-ky-theo-doi.ps1", DEMO / "dang-ky-theo-doi.ps1")
        print("Đã chép theo-doi.py, dang-ky-theo-doi.ps1 vào demo/")

    gia1 = {m: g for m, _, g, _, _ in SP}
    gia_minh = {m: gm for m, _, _, _, gm in SP}
    dap_an = {
        "giam_gia": {m: {"truoc": gia1[m], "sau": g, "phan_tram": round((g - gia1[m]) / gia1[m] * 100, 1),
                         "doi_thu_re_hon_minh": f"{(gia_minh[m] - g) / gia_minh[m] * 100:.1f}%"} for m, g in NGAY2["giam_gia"].items()},
        "tang_gia": {m: {"truoc": gia1[m], "sau": g, "phan_tram": round((g - gia1[m]) / gia1[m] * 100, 1)} for m, g in NGAY2["tang_gia"].items()},
        "het_hang": NGAY2["het_hang"], "co_hang_lai": NGAY2["co_hang_lai"],
        "san_pham_moi": [m for m, _, _ in NGAY2["moi"]], "ngung_ban": NGAY2["ngung"],
        "tong_so_thay_doi": 3 + 2 + 2 + 1 + 2 + 1,
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print("NGÀY 1: đã tạo demo/web-doi-thu/, demo/bang-gia-cua-minh.csv, dap-an.json")


if __name__ == "__main__":
    main()
