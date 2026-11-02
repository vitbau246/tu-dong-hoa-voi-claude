"""Thu thập trang CẦN ĐĂNG NHẬP bằng Playwright (Python) + Microsoft Edge có sẵn trên Windows.

- Mật khẩu KHÔNG viết trong code: đọc từ biến môi trường WEB_USER / WEB_PASS.
- Lần đầu đăng nhập xong, lưu phiên vào phien-dang-nhap.json (storage state) để lần sau không phải đăng nhập lại.
  Thêm phien-dang-nhap.json vào .gitignore: file này tương đương "chìa khóa" tài khoản.
- Chỉ khi đã đăng nhập, mỗi trích dẫn mới hiện liên kết "(Goodreads page)" -> dùng để kiểm chứng đăng nhập thành công.

Dùng (PowerShell):
    $env:WEB_USER = "demo"; $env:WEB_PASS = "demo"     # trang luyện tập chấp nhận mọi tài khoản
    python thu-thap-dang-nhap.py            # chạy ẩn
    python thu-thap-dang-nhap.py --hien     # hiện cửa sổ trình duyệt để xem
"""
import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = "https://quotes.toscrape.com"
PHIEN = Path("phien-dang-nhap.json")


def dang_nhap(page):
    user, pw = os.environ.get("WEB_USER"), os.environ.get("WEB_PASS")
    if not user or not pw:
        sys.exit("Thiếu biến môi trường WEB_USER / WEB_PASS")
    page.goto(f"{GOC}/login")
    page.fill("#username", user)
    page.fill("#password", pw)
    page.click("input[type=submit]")
    page.wait_for_selector("a[href='/logout']", timeout=15000)


def main():
    bat_dau = time.time()
    with sync_playwright() as p:
        trinh_duyet = p.chromium.launch(channel="msedge", headless="--hien" not in sys.argv)
        ngu_canh = trinh_duyet.new_context(storage_state=str(PHIEN) if PHIEN.exists() else None)
        page = ngu_canh.new_page()

        page.goto(GOC)
        if not page.query_selector("a[href='/logout']"):
            dang_nhap(page)
            ngu_canh.storage_state(path=str(PHIEN))
            print("Đăng nhập mới, đã lưu phiên vào", PHIEN)
        else:
            print("Dùng lại phiên đã lưu (không cần đăng nhập)")

        du_lieu, trang = [], 1
        while True:
            page.goto(f"{GOC}/page/{trang}/")
            for q in page.query_selector_all(".quote"):
                gr = q.query_selector("a[href*='goodreads.com']")
                du_lieu.append({
                    "text": q.query_selector(".text").inner_text().strip("“”"),
                    "author": q.query_selector(".author").inner_text(),
                    "goodreads": gr.get_attribute("href") if gr else "",
                })
            if not page.query_selector("li.next a"):
                break
            trang += 1
            time.sleep(0.5)  # lịch sự với máy chủ
        trinh_duyet.close()

    Path("trich-dan-dang-nhap.json").write_text(json.dumps(du_lieu, ensure_ascii=False, indent=1), encoding="utf-8")
    co_link = sum(1 for d in du_lieu if d["goodreads"])
    print(f"{len(du_lieu)} trích dẫn · {trang} trang · {co_link} có liên kết Goodreads (chỉ hiện khi đã đăng nhập) · "
          f"{time.time() - bat_dau:.1f} giây")


if __name__ == "__main__":
    main()
