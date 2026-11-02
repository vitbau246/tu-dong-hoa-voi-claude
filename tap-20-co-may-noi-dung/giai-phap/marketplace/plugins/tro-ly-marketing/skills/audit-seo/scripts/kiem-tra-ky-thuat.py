"""Audit SEO kỹ thuật: bò (crawl) toàn website từ trang chủ, kiểm tra 14 loại lỗi, xếp theo mức độ nghiêm trọng.

Dùng:  python kiem-tra-ky-thuat.py http://localhost:8002 [--thu-muc website]
       --thu-muc: so với file trên đĩa để tìm trang MỒ CÔI (có file nhưng không trang nào liên kết tới)
Kết quả: bao-cao-audit.md + loi-seo.csv, in điểm sức khỏe /100. Thoát mã 1 nếu còn lỗi NGHIÊM TRỌNG.
(Lưu ý: WebFetch của Claude không mở được localhost, nên audit site nội bộ phải dùng script như thế này.)
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
MUC = {"NGHIÊM TRỌNG": 25, "CAO": 8, "TRUNG BÌNH": 3, "THẤP": 1}  # điểm trừ cho mỗi lỗi


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    goc = sys.argv[1].rstrip("/") + "/"
    thu_muc = Path(sys.argv[sys.argv.index("--thu-muc") + 1]) if "--thu-muc" in sys.argv else None
    s = requests.Session()
    s.trust_env = False if re.match(r"https?://(localhost|127\.)", goc) else True  # bỏ qua proxy cho site nội bộ
    loi = []

    def them(muc, trang, loai, chi_tiet=""):
        loi.append({"muc_do": muc, "trang": trang, "loai": loai, "chi_tiet": chi_tiet})

    # robots.txt + sitemap
    rp = RobotFileParser()
    r = s.get(urljoin(goc, "robots.txt"), timeout=15)
    rp.parse(r.text.splitlines() if r.ok else [])
    if s.get(urljoin(goc, "sitemap.xml"), timeout=15).status_code != 200:
        them("CAO", "/sitemap.xml", "Không có sitemap.xml", "Google khó phát hiện đủ trang")

    hang_doi, da_tham, link_toi = [urljoin(goc, "index.html")], set(), defaultdict(set)
    titles = defaultdict(list)
    mo_coi = []
    for luot in (1, 2):  # lượt 2: quét nội dung các trang mồ côi (có file nhưng không ai liên kết tới)
      if luot == 2 and thu_muc:
        for f in thu_muc.rglob("*.html"):
            url = urljoin(goc, f.relative_to(thu_muc).as_posix())
            if url not in da_tham:
                mo_coi.append(url)
                them("TRUNG BÌNH", "/" + f.relative_to(thu_muc).as_posix(), "Trang mồ côi", "Không trang nào liên kết tới")
        hang_doi = list(mo_coi)
      while hang_doi:
          url = hang_doi.pop(0)
          if url in da_tham:
              continue
          da_tham.add(url)
          duong = urlparse(url).path
          r = s.get(url, timeout=15)
          if r.status_code >= 400:
              them("CAO", duong, f"Link nội bộ gãy ({r.status_code})", "Được liên kết từ: " + ", ".join(sorted(link_toi[url])))
              continue
          if not rp.can_fetch("Googlebot", url):
              them("NGHIÊM TRỌNG", duong, "Bị robots.txt chặn", "Googlebot không được đọc trang này")
          soup = BeautifulSoup(r.content, "lxml")
          title = soup.title.get_text(strip=True) if soup.title else ""
          titles[title].append(duong)
          if not title:
              them("CAO", duong, "Thiếu title")
          elif len(title) > 60:
              them("THẤP", duong, f"Title quá dài ({len(title)} ký tự)", "Google sẽ cắt bớt khi hiển thị")
          md = soup.find("meta", attrs={"name": "description"})
          if not md or not md.get("content", "").strip():
              them("TRUNG BÌNH", duong, "Thiếu meta description")
          rb = soup.find("meta", attrs={"name": "robots"})
          if rb and "noindex" in rb.get("content", "").lower():
              them("NGHIÊM TRỌNG", duong, "Có thẻ noindex", "Trang bị loại khỏi kết quả Google")
          can = soup.find("link", rel="canonical")
          if not can:
              them("THẤP", duong, "Thiếu canonical")
          elif urlparse(can["href"]).path.rstrip("/") not in (duong.rstrip("/"), duong.rstrip("/").removesuffix("/index.html")):
              them("CAO", duong, "Canonical trỏ sang trang khác", f"canonical = {can['href']}")
          h1 = soup.find_all("h1")
          if len(h1) != 1:
              them("TRUNG BÌNH", duong, f"Có {len(h1)} thẻ H1", "Mỗi trang nên có đúng 1 H1")
          if not soup.find("meta", attrs={"name": "viewport"}):
              them("TRUNG BÌNH", duong, "Thiếu meta viewport", "Hiển thị kém trên điện thoại")
          for img in soup.find_all("img"):
              if not img.get("alt", "").strip():
                  them("THẤP", duong, "Ảnh thiếu alt", img.get("src", ""))
              src = urljoin(url, img.get("src", ""))
              ri = s.head(src, timeout=15)
              kb = int(ri.headers.get("Content-Length", 0)) // 1024
              if kb > 300 and not any(l["chi_tiet"].startswith(urlparse(src).path) for l in loi if l["loai"].startswith("Ảnh quá nặng")):
                  them("TRUNG BÌNH", urlparse(src).path, f"Ảnh quá nặng ({kb:,} KB)", f"{urlparse(src).path} - nén/đổi sang WebP, mục tiêu < 200 KB")
          for a in soup.find_all("a", href=True):
              dich = urljoin(url, a["href"]).split("#")[0]
              if dich.startswith(goc):
                  link_toi[dich].add(duong)
                  if dich not in da_tham:
                      hang_doi.append(dich)

    for title, ds in titles.items():
        if title and len(ds) > 1:
            for d in ds:
                them("CAO", d, "Trùng title với trang khác", " · ".join(x for x in ds if x != d))

    diem = max(0, 100 - sum(MUC[l["muc_do"]] for l in loi))
    thu_tu = list(MUC)
    loi.sort(key=lambda l: (thu_tu.index(l["muc_do"]), l["loai"], l["trang"]))
    with open("loi-seo.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["muc_do", "trang", "loai", "chi_tiet"])
        w.writeheader()
        w.writerows(loi)
    dem = {m: sum(1 for l in loi if l["muc_do"] == m) for m in MUC}
    with open("bao-cao-audit.md", "w", encoding="utf-8") as f:
        f.write(f"# Audit SEO kỹ thuật: {goc}\n\n**Điểm sức khỏe: {diem}/100** · {len(da_tham)} URL đã quét · "
                + " · ".join(f"{v} {k}" for k, v in dem.items()) + "\n\n| Mức độ | Trang | Lỗi | Chi tiết |\n|---|---|---|---|\n")
        for l in loi:
            f.write(f"| {l['muc_do']} | {l['trang']} | {l['loai']} | {l['chi_tiet']} |\n")
    print(f"ĐIỂM SỨC KHỎE: {diem}/100 · {len(da_tham)} URL · " + " · ".join(f"{v} {k}" for k, v in dem.items()))
    for l in loi:
        if l["muc_do"] in ("NGHIÊM TRỌNG", "CAO"):
            print(f"  [{l['muc_do']}] {l['trang']}: {l['loai']} {l['chi_tiet']}")
    print("→ bao-cao-audit.md, loi-seo.csv")
    sys.exit(1 if dem["NGHIÊM TRỌNG"] else 0)


if __name__ == "__main__":
    main()
