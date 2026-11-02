"""Tập 6 - Tạo dự án có "dữ liệu gốc" cần bảo vệ, để gắn hooks an toàn.

Chạy:  python chuan-bi.py              -> demo/ ban đầu (chưa có hooks)
       python chuan-bi.py --giai-phap  -> chép thêm .claude/settings.json + .claude/hooks/ từ giai-phap/
"""
import random
import shutil
import sys
from pathlib import Path

from openpyxl import Workbook

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
rng = random.Random(6)


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def bang(path, tieu_de, so_dong):
    wb = Workbook()
    ws = wb.active
    ws.append(tieu_de)
    for i in range(so_dong):
        ws.append([i + 1] + [rng.randint(1, 50_000_000) for _ in tieu_de[1:]])
    wb.save(path)


def main():
    lam_moi(DEMO)
    goc = DEMO / "du-lieu-goc"
    goc.mkdir(parents=True)
    (DEMO / "lam-viec").mkdir()

    bang(goc / "so-cai-2025.xlsx", ["STT", "Phát sinh Nợ", "Phát sinh Có"], 300)
    bang(goc / "bang-luong-T10-2026.xlsx", ["STT", "Lương cơ bản", "Phụ cấp", "Thực lĩnh"], 85)
    bang(goc / "cong-no-khach-hang.xlsx", ["STT", "Phải thu", "Đã thu"], 120)
    # Rác thường gặp: file khóa tạm của Excel, bản sao, file log
    (goc / "~$so-cai-2025.xlsx").write_bytes(b"\x00" * 165)
    shutil.copy(goc / "bang-luong-T10-2026.xlsx", goc / "Copy of bang-luong-T10-2026.xlsx")
    (goc / "export_tmp.log").write_text("temp\n", encoding="utf-8")
    (DEMO / "DOC-KY-TRUOC-KHI-SUA.txt").write_text(
        "Thư mục du-lieu-goc là số liệu kế toán CHÍNH THỨC. Chỉ được đọc.\n"
        "Mọi xử lý thực hiện trên bản sao trong lam-viec/.\n", encoding="utf-8")

    if "--giai-phap" in sys.argv:
        shutil.copytree(GOC / "giai-phap" / ".claude", DEMO / ".claude")
        # Windows PowerShell 5.1 cần UTF-8 có BOM để đọc đúng tiếng Việt trong .ps1
        ps1 = DEMO / ".claude" / "hooks" / "chuong-bao.ps1"
        ps1.write_text(ps1.read_text(encoding="utf-8-sig"), encoding="utf-8-sig")
        print("Đã chép hooks từ giai-phap/ vào demo/.claude/")

    print("Đã tạo demo/: du-lieu-goc/ (3 file chính + 3 file rác), lam-viec/ (trống)")


if __name__ == "__main__":
    main()
