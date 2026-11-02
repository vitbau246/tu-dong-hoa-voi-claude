"""Tập 10 - Gom các "mảnh" đã làm ở tập 4, 5, 6, 9 vào demo/da-co/ để Claude đóng gói thành plugin.

Chạy:  python chuan-bi.py              -> demo/da-co/ (skills, agents, hooks rời rạc như trên máy người dùng)
       python chuan-bi.py --giai-phap  -> chép thêm demo/van-phong-marketplace/ (plugin + marketplace hoàn chỉnh)
Thử cài (không ảnh hưởng cài đặt thật):
       set CLAUDE_CONFIG_DIR=%TEMP%\claude-thu  &&  claude plugin marketplace add ./van-phong-marketplace
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
SERIES = GOC.parent
DEMO = GOC / "demo"

NGUON = {
    "skills/bao-cao-tuan": SERIES / "tap-05-skills-bao-cao-tuan/giai-phap/.claude/skills/bao-cao-tuan",
    "agents/phan-tich-bao-gia.md": SERIES / "tap-09-subagents-doi-ai/giai-phap/.claude/agents/phan-tich-bao-gia.md",
    "agents/tham-dinh-doc-lap.md": SERIES / "tap-09-subagents-doi-ai/giai-phap/.claude/agents/tham-dinh-doc-lap.md",
    "hooks/phanh-an-toan.py": SERIES / "tap-06-hooks-an-toan/giai-phap/.claude/hooks/phanh-an-toan.py",
    "hooks/chuong-bao.ps1": SERIES / "tap-06-hooks-an-toan/giai-phap/.claude/hooks/chuong-bao.ps1",
    "hooks/settings-tap-6.json": SERIES / "tap-06-hooks-an-toan/giai-phap/.claude/settings.json",
    "kich-ban-tap/tap-01-don-dep.md": SERIES / "tap-01-don-dep-downloads/kich-ban.md",
    "kich-ban-tap/tap-03-hoa-don.md": SERIES / "tap-03-hoa-don-pdf/kich-ban.md",
    "kich-ban-tap/tap-04-tron-thu.md": SERIES / "tap-04-tron-thu/kich-ban.md",
}


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    for dich, nguon in NGUON.items():
        d = DEMO / "da-co" / dich
        d.parent.mkdir(parents=True, exist_ok=True)
        if nguon.is_dir():
            shutil.copytree(nguon, d)
        else:
            shutil.copy(nguon, d)

    if "--giai-phap" in sys.argv:
        shutil.copytree(GOC / "giai-phap" / "van-phong-marketplace", DEMO / "van-phong-marketplace")
        print("Đã chép van-phong-marketplace/ vào demo/")

    print("Đã tạo demo/da-co/:", ", ".join(NGUON))


if __name__ == "__main__":
    main()
