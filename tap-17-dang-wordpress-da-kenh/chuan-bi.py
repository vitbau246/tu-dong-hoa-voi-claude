"""Tập 17 - Đăng bài lên WordPress (bản nháp) + chuyển thành nội dung đa kênh.

Chạy:  python chuan-bi.py              -> demo/ (bài đạt 100/100 từ tập 16, CLAUDE.md, wp-gia-lap.py)
       python chuan-bi.py --giai-phap  -> chép thêm dang-wordpress.py, seo-meta-rest.php, skill da-kenh
Tập dượt không cần WordPress thật:  python wp-gia-lap.py  (WordPress GIẢ LẬP ở http://localhost:8080)
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
TAP16 = GOC.parent / "tap-16-viet-bai-chuan-seo"


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    (DEMO / "bai-viet").mkdir()
    shutil.copy(TAP16 / "giai-phap" / "ket-qua-mau" / "ghe-cong-thai-hoc-cach-chon.md", DEMO / "bai-viet")
    shutil.copy(TAP16 / "du-lieu" / "CLAUDE.md", DEMO / "CLAUDE.md")
    shutil.copy(GOC / "wp-gia-lap.py", DEMO / "wp-gia-lap.py")
    (DEMO / ".gitignore").write_text(".env\nwp-gia-lap-media/\n", encoding="utf-8")
    if "--giai-phap" in sys.argv:
        for f in ("dang-wordpress.py", "seo-meta-rest.php"):
            shutil.copy(GOC / "giai-phap" / f, DEMO / f)
        shutil.copytree(GOC / "giai-phap" / ".claude", DEMO / ".claude")
        print("Đã chép dang-wordpress.py, seo-meta-rest.php, skill da-kenh vào demo/")
    print("Đã tạo demo/: bai-viet/ghe-cong-thai-hoc-cach-chon.md (100/100), CLAUDE.md, wp-gia-lap.py")


if __name__ == "__main__":
    main()
