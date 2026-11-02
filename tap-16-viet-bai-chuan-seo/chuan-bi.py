"""Tập 16 - Dự án viết bài chuẩn SEO: giọng văn thương hiệu, brief, bài nháp cũ, trình chấm điểm.

Chạy:  python chuan-bi.py              -> demo/ (CLAUDE.md, san-pham.csv, brief/, bai-viet/ban-nhap-cu.md, cham-diem-seo.py)
       python chuan-bi.py --giai-phap  -> chép thêm .claude/settings.json (hook chấm điểm) + skill viet-bai-seo
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    du_lieu = GOC / "du-lieu"
    for d in ("brief", "bai-viet", "anh"):
        (DEMO / d).mkdir()
    shutil.copy(du_lieu / "CLAUDE.md", DEMO / "CLAUDE.md")
    shutil.copy(du_lieu / "san-pham.csv", DEMO / "san-pham.csv")
    shutil.copy(du_lieu / "brief-ghe-cong-thai-hoc.md", DEMO / "brief" / "ghe-cong-thai-hoc.md")
    shutil.copy(du_lieu / "ban-nhap-cu.md", DEMO / "bai-viet" / "ban-nhap-cu.md")
    shutil.copy(GOC / "giai-phap" / "cham-diem-seo.py", DEMO / "cham-diem-seo.py")
    if "--giai-phap" in sys.argv:
        shutil.copytree(GOC / "giai-phap" / ".claude", DEMO / ".claude")
        print("Đã chép hook chấm điểm + skill viet-bai-seo vào demo/.claude/")
    print("Đã tạo demo/: CLAUDE.md, san-pham.csv, brief/, bai-viet/ban-nhap-cu.md (14/100 điểm), cham-diem-seo.py")


if __name__ == "__main__":
    main()
