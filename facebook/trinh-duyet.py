"""Điều khiển Edge (profile riêng) để thao tác Facebook trên web. Người dùng TỰ đăng nhập, script không bao giờ nhận mật khẩu.

Lệnh:
  python trinh-duyet.py dang-nhap            # mở Edge, chờ bạn đăng nhập (tối đa 15 phút), lưu phiên
  python trinh-duyet.py chup <url> [ten]     # mở url bằng phiên đã lưu, chụp màn hình vào anh-chup/<ten>.png
Phiên đăng nhập lưu NGOÀI dự án: %LOCALAPPDATA%\\FoxFlow\\edge-facebook (xóa thư mục này = đăng xuất).
"""
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
PROFILE = Path(os.environ["LOCALAPPDATA"]) / "FoxFlow" / "edge-facebook"
ANH = GOC / "anh-chup"


def mo(p, headless=False):
    PROFILE.mkdir(parents=True, exist_ok=True)
    return p.chromium.launch_persistent_context(str(PROFILE), channel="msedge", headless=headless,
                                                viewport={"width": 1366, "height": 860}, locale="vi-VN")


def da_dang_nhap(ctx):
    return any(c["name"] == "c_user" for c in ctx.cookies("https://www.facebook.com"))


def main():
    lenh = sys.argv[1] if len(sys.argv) > 1 else ""
    ANH.mkdir(exist_ok=True)
    with sync_playwright() as p:
        if lenh == "dang-nhap":
            ctx = mo(p)
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto("https://www.facebook.com/")
            if da_dang_nhap(ctx):
                print("ĐÃ ĐĂNG NHẬP SẴN (phiên cũ còn hiệu lực).")
            else:
                print("Cửa sổ Edge đã mở: hãy TỰ đăng nhập profile FoxFlow (kể cả mã 2FA). Đang chờ tối đa 15 phút...", flush=True)
                han = time.time() + 900
                while time.time() < han and not da_dang_nhap(ctx):
                    try:
                        page.wait_for_timeout(3000)
                    except Exception:
                        sys.exit("Cửa sổ Edge đã bị đóng trước khi đăng nhập xong. Chạy lại lệnh và ĐỪNG đóng cửa sổ, script sẽ tự đóng khi xong.")
                if not da_dang_nhap(ctx):
                    ctx.close()
                    sys.exit("Hết 15 phút mà chưa đăng nhập. Chạy lại lệnh khi sẵn sàng.")
                print("ĐÃ ĐĂNG NHẬP. Phiên được lưu, lần sau không cần đăng nhập lại.", flush=True)
                page.wait_for_timeout(4000)
            page.screenshot(path=str(ANH / "sau-dang-nhap.png"))
            ctx.close()
        elif lenh == "chup":
            ctx = mo(p, headless=True)
            if not da_dang_nhap(ctx):
                sys.exit("Chưa đăng nhập: chạy 'python trinh-duyet.py dang-nhap' trước.")
            page = ctx.new_page()
            page.goto(sys.argv[2])
            page.wait_for_timeout(5000)
            ten = sys.argv[3] if len(sys.argv) > 3 else "trang"
            page.screenshot(path=str(ANH / f"{ten}.png"))
            print(f"Đã chụp: anh-chup/{ten}.png · URL hiện tại: {page.url}")
            ctx.close()
        else:
            sys.exit(__doc__)


if __name__ == "__main__":
    main()
