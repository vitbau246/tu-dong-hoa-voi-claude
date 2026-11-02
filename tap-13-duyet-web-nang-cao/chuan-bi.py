"""Tập 13 - Duyệt web nâng cao trên trang luyện tập quotes.toscrape.com (được làm ra để luyện thu thập dữ liệu).

Chạy:  python chuan-bi.py              -> demo/nhiem-vu.md, demo/.gitignore, dap-an.json
       python chuan-bi.py --giai-phap  -> chép thêm .mcp.json (Playwright + Edge) và 2 script mẫu
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
MCP = GOC.parent / "tap-07-trinh-duyet-mcp" / "giai-phap" / ".mcp.json"

NHIEM_VU = """# Nhiệm vụ: thu thập toàn bộ trích dẫn từ quotes.toscrape.com

Trang luyện tập này có 3 "kiểu khó" thường gặp ngoài đời:
1. **Cuộn vô hạn:** https://quotes.toscrape.com/scroll (HTML gốc không có dữ liệu)
2. **Cần đăng nhập:** https://quotes.toscrape.com/login (chỉ khi đăng nhập mới thấy liên kết Goodreads của tác giả)
3. **Nội dung do JavaScript tạo:** https://quotes.toscrape.com/js/

Kết quả cần có: toàn bộ trích dẫn (nội dung, tác giả, thẻ, liên kết Goodreads) trong Excel + thống kê top tác giả.
Quy tắc: nghỉ ít nhất 0,5 giây giữa các yêu cầu. Không ghi mật khẩu vào code hay vào chat.
"""
GITIGNORE = """# Phiên đăng nhập trình duyệt = chìa khóa tài khoản, KHÔNG đưa lên git
phien-dang-nhap.json
.env
"""


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    (DEMO / "nhiem-vu.md").write_text(NHIEM_VU, encoding="utf-8")
    (DEMO / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    if "--giai-phap" in sys.argv:
        shutil.copy(MCP, DEMO / ".mcp.json")
        for f in ("thu-thap-api.py", "thu-thap-dang-nhap.py"):
            shutil.copy(GOC / "giai-phap" / f, DEMO / f)
        print("Đã chép .mcp.json + thu-thap-api.py + thu-thap-dang-nhap.py vào demo/")
    dap_an = {
        "tong_trich_dan": 100, "so_trang": 10, "so_tac_gia": 50,
        "top3_tac_gia": {"Albert Einstein": 10, "J.K. Rowling": 9, "Marilyn Monroe": 7},
        "lien_ket_goodreads": {"chua_dang_nhap": 0, "da_dang_nhap": 100},
        "html_goc_trang_scroll_co_bao_nhieu_trich_dan": 0,
        "api_cua_sau": "https://quotes.toscrape.com/api/quotes?page=N (JSON, has_next)",
        "do_thoi_gian_30_10_2026": {"goi_API": "7,6 giây", "script_Playwright_co_dang_nhap": "20,5 giây"},
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Đã tạo demo/nhiem-vu.md, demo/.gitignore, dap-an.json")


if __name__ == "__main__":
    main()
