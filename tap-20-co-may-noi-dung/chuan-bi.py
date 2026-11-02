"""Tập 20 - Không gian làm việc của phòng Marketing cho "cỗ máy nội dung" hằng tuần.

Chạy:  python chuan-bi.py              -> demo/ (CLAUDE.md, san-pham.csv, ke-hoach-noi-dung.csv, wp-gia-lap.py, chay-hang-tuan.ps1)
       python chuan-bi.py --giai-phap  -> dựng lại + chép marketplace/ (plugin tro-ly-marketing + tro-ly-van-phong)
"""
import csv
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
S = GOC.parent
DEMO = GOC / "demo"

# Kế hoạch 4 tuần (đầu ra tập 15). Hai việc tuần 1 đã xong, việc "Chưa làm" đầu tiên là bài viết mới.
KE_HOACH = [
    ("1", "giấy a4 double a giá", "Mua", "Viết lại tiêu đề + mô tả", "Đã xong"),
    ("1", "bàn làm việc chân sắt", "Cân nhắc", "Gộp 2 trang tự cạnh tranh", "Đã xong"),
    ("2", "máy hủy tài liệu", "Cân nhắc", "Viết mới", "Chưa làm"),
    ("2", "ghế công thái học giá rẻ", "Cân nhắc", "Viết mới", "Chưa làm"),
    ("3", "bảng trắng văn phòng", "Mua", "Tối ưu trang danh mục", "Chưa làm"),
    ("3", "máy hủy tài liệu mini", "Cân nhắc", "Viết mới", "Chưa làm"),
    ("4", "ghế công thái học", "Cân nhắc", "Viết mới", "Chưa làm"),
]


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    for d in ("brief", "bai-viet", "da-kenh", "cho-duyet"):
        (DEMO / d).mkdir()
    shutil.copy(S / "tap-16-viet-bai-chuan-seo/du-lieu/CLAUDE.md", DEMO / "CLAUDE.md")
    shutil.copy(S / "tap-16-viet-bai-chuan-seo/du-lieu/san-pham.csv", DEMO / "san-pham.csv")
    shutil.copy(S / "tap-17-dang-wordpress-da-kenh/wp-gia-lap.py", DEMO / "wp-gia-lap.py")
    ps1 = (GOC / "giai-phap" / "chay-hang-tuan.ps1").read_text(encoding="utf-8-sig")
    (DEMO / "chay-hang-tuan.ps1").write_text(ps1, encoding="utf-8-sig")  # PowerShell 5.1 cần BOM
    with open(DEMO / "ke-hoach-noi-dung.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["tuan", "tu_khoa", "y_dinh", "loai_viec", "trang_thai", "ngay_cap_nhat"])
        for r in KE_HOACH:
            w.writerow([*r, ""])
    (DEMO / ".gitignore").write_text(".env\nwp-gia-lap-media/\n", encoding="utf-8")

    if "--giai-phap" in sys.argv:
        subprocess.run([sys.executable, str(GOC / "giai-phap" / "dong-goi.py")], check=True)
        shutil.copytree(GOC / "giai-phap" / "marketplace", DEMO / "marketplace")
        print("Đã chép marketplace/ (2 plugin) vào demo/")
    print("Đã tạo demo/: CLAUDE.md, san-pham.csv, ke-hoach-noi-dung.csv (việc tiếp theo: 'máy hủy tài liệu'), wp-gia-lap.py, chay-hang-tuan.ps1")


if __name__ == "__main__":
    main()
