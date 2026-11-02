"""Theo dõi website đối thủ: chụp dữ liệu → so với lần trước → CHỈ KHI có thay đổi mới gọi Claude viết nhận định.

Thiết kế "AI ở đúng chỗ":
  - Thu thập + so sánh: script thường (miễn phí, chính xác tuyệt đối, chạy bao nhiêu lần cũng được)
  - Nhận định + đề xuất hành động: Claude (chỉ chạy khi có thay đổi -> tiết kiệm hạn mức)

Dùng:
  python theo-doi.py http://localhost:8001            # chụp + so sánh + (nếu thay đổi) gọi Claude
  python theo-doi.py http://localhost:8001 --khong-ai # chỉ chụp + so sánh, in ra yêu cầu sẽ gửi cho Claude
Kết quả: anh-chup/<thời điểm>.json · thay-doi/<thời điểm>.json · bao-cao-doi-thu/<thời điểm>.md
"""
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
# Bộ chọn (CSS selector) cho website cần theo dõi. Đổi website thì chỉ cần sửa ở đây.
CHON = {"muc": "article.item", "ma": "data-sku", "ten": ".name", "gia": ".price", "kho": ".stock"}


def chup(url):
    # Máy văn phòng thường có proxy (HTTP_PROXY): địa chỉ nội bộ/localhost phải đi thẳng, không qua proxy
    noi_bo = re.match(r"https?://(localhost|127\.|10\.|192\.168\.)", url)
    r = requests.get(url, timeout=30, headers={"User-Agent": "theo-doi-gia (video huong dan)"},
                     proxies={"http": None, "https": None} if noi_bo else None)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "lxml")
    du_lieu = {}
    for el in soup.select(CHON["muc"]):
        gia = re.sub(r"\D", "", el.select_one(CHON["gia"]).get_text())
        du_lieu[el[CHON["ma"]]] = {
            "ten": el.select_one(CHON["ten"]).get_text(strip=True),
            "gia": int(gia) if gia else None,
            "con_hang": "hết" not in el.select_one(CHON["kho"]).get_text().lower(),
        }
    return du_lieu


def so_sanh(cu, moi):
    td = {"giam_gia": [], "tang_gia": [], "het_hang": [], "co_hang_lai": [], "moi": [], "ngung_ban": []}
    for ma, sp in moi.items():
        if ma not in cu:
            td["moi"].append({"ma": ma, **sp})
            continue
        c = cu[ma]
        if c["gia"] and sp["gia"] and sp["gia"] != c["gia"]:
            muc = {"ma": ma, "ten": sp["ten"], "truoc": c["gia"], "sau": sp["gia"],
                   "phan_tram": round((sp["gia"] - c["gia"]) / c["gia"] * 100, 1)}
            td["giam_gia" if sp["gia"] < c["gia"] else "tang_gia"].append(muc)
        if c["con_hang"] and not sp["con_hang"]:
            td["het_hang"].append({"ma": ma, "ten": sp["ten"]})
        if not c["con_hang"] and sp["con_hang"]:
            td["co_hang_lai"].append({"ma": ma, "ten": sp["ten"]})
    td["ngung_ban"] = [{"ma": ma, "ten": c["ten"]} for ma, c in cu.items() if ma not in moi]
    td["giam_gia"].sort(key=lambda x: x["phan_tram"])
    return td


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    url, khong_ai = sys.argv[1], "--khong-ai" in sys.argv
    luc = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    for d in ("anh-chup", "thay-doi", "bao-cao-doi-thu"):
        Path(d).mkdir(exist_ok=True)

    moi = chup(url)
    truoc = sorted(Path("anh-chup").glob("*.json"))
    Path(f"anh-chup/{luc}.json").write_text(json.dumps(moi, ensure_ascii=False, indent=1), encoding="utf-8")
    if not truoc:
        print(f"Lần chụp đầu tiên: {len(moi)} sản phẩm. Chưa có gì để so sánh.")
        return

    td = so_sanh(json.loads(truoc[-1].read_text(encoding="utf-8")), moi)
    tong = sum(len(v) for v in td.values())
    if tong == 0:
        print(f"Không có thay đổi ({len(moi)} sản phẩm). Không gọi AI → không tốn hạn mức.")
        return
    Path(f"thay-doi/{luc}.json").write_text(json.dumps(td, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{tong} thay đổi: " + " · ".join(f"{len(v)} {k}" for k, v in td.items() if v))

    yeu_cau = (f"Đọc thay-doi/{luc}.json (thay đổi trên website đối thủ so với lần trước) và bang-gia-cua-minh.csv. "
               f"Viết bao-cao-doi-thu/{luc}.md dài tối đa nửa trang cho Giám đốc kinh doanh: "
               "1) 3 thay đổi quan trọng nhất và vì sao quan trọng; 2) bảng các mặt hàng mà đối thủ giờ RẺ HƠN mình "
               "(giá đối thủ, giá mình, chênh lệch %); 3) 2-3 hành động đề xuất trong hôm nay. "
               "Không bịa số: chỉ dùng số có trong 2 file. Cuối cùng trả lời đúng 1 câu tóm tắt.")
    if khong_ai:
        print("\n[--khong-ai] Yêu cầu sẽ gửi cho Claude:\n" + yeu_cau)
        return
    claude = os.environ.get("CLAUDE_EXE") or shutil.which("claude") or str(Path.home() / ".local/bin/claude.exe")
    kq = subprocess.run([claude, "-p", yeu_cau, "--allowedTools", "Read,Write", "--max-budget-usd", "0.5"],
                        capture_output=True, text=True, encoding="utf-8", timeout=600)
    print("Claude:", kq.stdout.strip() or kq.stderr.strip())


if __name__ == "__main__":
    main()
