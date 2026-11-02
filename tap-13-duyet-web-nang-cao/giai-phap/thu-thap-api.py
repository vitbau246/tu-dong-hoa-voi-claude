"""Thu thập qua "cửa sau": gọi thẳng API JSON mà trang cuộn vô hạn dùng (tìm được trong tab Network).

Trang https://quotes.toscrape.com/scroll có HTML gốc TRỐNG; trình duyệt tải dữ liệu từ /api/quotes?page=N.
Gọi thẳng API: không cần trình duyệt, nhanh hơn hàng chục lần, kết quả ổn định.

Dùng: python thu-thap-api.py   -> trich-dan.xlsx
"""
import sys
import time
from collections import Counter

import requests
from openpyxl import Workbook
from openpyxl.styles import Font

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
API = "https://quotes.toscrape.com/api/quotes?page={}"
NGHI_GIUA_CAC_LAN = 0.5  # lịch sự với máy chủ: không gửi dồn dập


def main():
    bat_dau = time.time()
    du_lieu, trang = [], 1
    with requests.Session() as s:
        s.headers["User-Agent"] = "Mozilla/5.0 (video huong dan tu dong hoa)"
        while True:
            r = s.get(API.format(trang), timeout=30)
            r.raise_for_status()
            j = r.json()
            for q in j["quotes"]:
                du_lieu.append({"text": q["text"].strip("“”"), "author": q["author"]["name"], "tags": ", ".join(q["tags"])})
            if not j["has_next"]:
                break
            trang += 1
            time.sleep(NGHI_GIUA_CAC_LAN)

    wb = Workbook()
    ws = wb.active
    ws.title = "Trich-dan"
    ws.append(["STT", "Trích dẫn", "Tác giả", "Thẻ"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for i, d in enumerate(du_lieu, 1):
        ws.append([i, d["text"], d["author"], d["tags"]])
    ws.column_dimensions["B"].width = 90
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 40

    tk = wb.create_sheet("Thong-ke")
    tk.append(["Tác giả", "Số trích dẫn"])
    for ten, so in Counter(d["author"] for d in du_lieu).most_common(10):
        tk.append([ten, so])
    wb.save("trich-dan.xlsx")

    tac_gia = Counter(d["author"] for d in du_lieu)
    print(f"{len(du_lieu)} trích dẫn · {trang} trang API · {len(tac_gia)} tác giả · {time.time() - bat_dau:.1f} giây")
    print("Top 3 tác giả:", ", ".join(f"{t} ({n})" for t, n in tac_gia.most_common(3)))


if __name__ == "__main__":
    main()
