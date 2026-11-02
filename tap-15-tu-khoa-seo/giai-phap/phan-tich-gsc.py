"""Tìm "mỏ vàng" SEO trong dữ liệu Google Search Console (file truy vấn × trang).

Dùng: python phan-tich-gsc.py gsc/truy-van-theo-trang.csv   -> co-hoi-seo.xlsx (3 sheet) + tóm tắt
  1. Sat-trang-1  : vị trí 8–20 và hiển thị >= 2.000 (đẩy nhẹ là lên trang 1)
  2. CTR-thap     : vị trí <= 5 nhưng CTR < 40% mức chuẩn của vị trí -> viết lại tiêu đề/mô tả
  3. Tu-canh-tranh: >= 2 trang cùng 1 truy vấn, mỗi trang >= 500 hiển thị -> gộp/phân vai nội dung
Số click tiềm năng = hiển thị × (CTR chuẩn vị trí mục tiêu − CTR hiện tại).
"""
import csv
import sys
from collections import defaultdict

from openpyxl import Workbook
from openpyxl.styles import Font

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
CTR_CHUAN = {1: 0.28, 2: 0.16, 3: 0.11, 4: 0.08, 5: 0.065, 6: 0.05, 7: 0.04, 8: 0.032, 9: 0.027, 10: 0.024}


def doc(path):
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            yield {"q": r["Query"], "page": r["Page"], "click": int(r["Clicks"]), "ht": int(r["Impressions"]),
                   "ctr": float(r["CTR"].rstrip("%")) / 100, "vt": float(r["Position"])}


def main(path):
    dong = list(doc(path))
    theo_q = defaultdict(list)
    for d in dong:
        theo_q[d["q"]].append(d)
    gop = []
    for q, ds in theo_q.items():
        ht = sum(d["ht"] for d in ds)
        gop.append({"q": q, "ht": ht, "click": sum(d["click"] for d in ds),
                    "vt": sum(d["vt"] * d["ht"] for d in ds) / ht, "page": max(ds, key=lambda d: d["ht"])["page"]})
    for g in gop:
        g["ctr"] = g["click"] / g["ht"]

    sat = sorted([g for g in gop if 8 <= g["vt"] <= 20 and g["ht"] >= 2000], key=lambda g: -g["ht"])
    for g in sat:
        g["tiem_nang"] = round(g["ht"] * (CTR_CHUAN[5] - g["ctr"]))  # nếu lên được vị trí 5
    thap = [g for g in gop if g["vt"] <= 5 and g["ctr"] < 0.4 * CTR_CHUAN[max(1, round(g["vt"]))]]
    for g in thap:
        g["tiem_nang"] = round(g["ht"] * (CTR_CHUAN[max(1, round(g["vt"]))] - g["ctr"]))
    canh = {q: ds for q, ds in theo_q.items() if len([d for d in ds if d["ht"] >= 500]) >= 2}

    wb = Workbook()
    ws = wb.active
    ws.title = "Sat-trang-1"
    ws.append(["Truy vấn", "Trang", "Hiển thị", "Click", "CTR", "Vị trí TB", "Click tiềm năng/3 tháng (lên vị trí 5)"])
    for g in sat:
        ws.append([g["q"], g["page"], g["ht"], g["click"], f"{g['ctr']:.1%}", round(g["vt"], 1), g["tiem_nang"]])
    ws2 = wb.create_sheet("CTR-thap")
    ws2.append(["Truy vấn", "Trang", "Hiển thị", "CTR hiện tại", "CTR chuẩn vị trí", "Vị trí TB", "Click tiềm năng/3 tháng"])
    for g in thap:
        ws2.append([g["q"], g["page"], g["ht"], f"{g['ctr']:.1%}", f"{CTR_CHUAN[max(1, round(g['vt']))]:.0%}", round(g["vt"], 1), g["tiem_nang"]])
    ws3 = wb.create_sheet("Tu-canh-tranh")
    ws3.append(["Truy vấn", "Trang", "Hiển thị", "Vị trí TB"])
    for q, ds in canh.items():
        for d in sorted(ds, key=lambda d: d["vt"]):
            ws3.append([q, d["page"], d["ht"], d["vt"]])
    for s in wb.worksheets:
        for c in s[1]:
            c.font = Font(bold=True)
        s.column_dimensions["A"].width = 32
        s.column_dimensions["B"].width = 50
    wb.save("co-hoi-seo.xlsx")

    print(f"{len(gop)} truy vấn · {len(dong)} dòng truy vấn-trang")
    print(f"\nSát trang 1 ({len(sat)}):")
    for g in sat:
        print(f"  {g['q']:30} vị trí {g['vt']:5.1f} · {g['ht']:>6,} hiển thị · +{g['tiem_nang']:,} click tiềm năng")
    print(f"\nTop 5 nhưng CTR thấp ({len(thap)}):")
    for g in thap:
        print(f"  {g['q']:30} vị trí {g['vt']:4.1f} · CTR {g['ctr']:.1%} (chuẩn ~{CTR_CHUAN[max(1, round(g['vt']))]:.0%}) · +{g['tiem_nang']:,} click")
    print(f"\nTự cạnh tranh ({len(canh)}):")
    for q, ds in canh.items():
        print(f"  {q}: " + " vs ".join(f"{d['page'].split('.example')[1]} (vị trí {d['vt']})" for d in ds))
    print("\n→ co-hoi-seo.xlsx")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gsc/truy-van-theo-trang.csv")
