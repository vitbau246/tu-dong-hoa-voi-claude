"""Tập 15 - Dữ liệu Google Search Console (hư cấu, đúng định dạng xuất file) để nghiên cứu từ khóa SEO.

Chạy:  python chuan-bi.py              -> demo/gsc/{Queries.csv, Pages.csv, truy-van-theo-trang.csv}, demo/website.md, dap-an.json
       python chuan-bi.py --giai-phap  -> chép thêm phan-tich-gsc.py + .claude/skills/brief-seo/

"Mỏ vàng" được gài (quy tắc ở dap-an.json):
  - Từ khóa sát trang 1 (vị trí 8-20, nhiều lượt hiển thị) -> đẩy nhẹ là lên trang 1
  - Top 3 nhưng CTR thấp bất thường -> chỉ cần viết lại tiêu đề / mô tả
  - Tự cạnh tranh (cannibalization): 2 trang cùng nhắm 1 từ khóa, chia nhau lượt hiển thị
"""
import csv
import json
import random
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
SITE = "https://vpp-anphat.example"
rng = random.Random(15)

# (truy vấn, trang, lượt hiển thị 3 tháng, vị trí TB, CTR ép buộc hoặc None = theo đường cong chuẩn)
GAI = [
    ("ghế công thái học", "/ghe-cong-thai-hoc", 18400, 11.2, None),
    ("ghế công thái học giá rẻ", "/ghe-cong-thai-hoc", 6200, 9.8, None),
    ("máy hủy tài liệu", "/may-huy-tai-lieu", 7300, 14.6, None),
    ("máy hủy tài liệu mini", "/may-huy-tai-lieu", 2100, 12.3, None),
    ("bảng trắng văn phòng", "/bang-trang", 3900, 17.4, None),
    ("giấy a4 double a giá", "/giay-a4-double-a", 9100, 2.8, 0.011),
    ("mua giấy a4 số lượng lớn", "/giay-a4-double-a", 2600, 3.4, 0.014),
    ("mực in hp 107a", "/muc-in-hp-107a", 5200, 1.9, None),
    ("văn phòng phẩm an phát", "/", 2400, 1.1, None),
]
TU_CANH_TRANH = ("bàn làm việc chân sắt", [("/ban-lam-viec-chan-sat", 3100, 9.6), ("/blog/cach-chon-ban-lam-viec", 2700, 12.9)])
DUOI = ["giá", "loại nào tốt", "chính hãng", "hà nội", "tphcm", "review", "mua ở đâu", "cách chọn", "2026", "giá rẻ"]
GOC_TU = [("bút ký parker", "/but-ky-parker"), ("tủ hồ sơ sắt", "/tu-ho-so"), ("đèn bàn chống cận", "/den-ban-led"),
          ("bìa còng", "/bia-cong"), ("máy in laser", "/may-in-laser"), ("chuột không dây", "/chuot-khong-day"),
          ("bàn phím cơ", "/ban-phim-co"), ("màn hình 24 inch", "/man-hinh-24-inch"), ("máy chiếu văn phòng", "/may-chieu")]
CTR_CHUAN = {1: 0.28, 2: 0.16, 3: 0.11, 4: 0.08, 5: 0.065, 6: 0.05, 7: 0.04, 8: 0.032, 9: 0.027, 10: 0.024}


def ctr(vt):
    return CTR_CHUAN.get(round(vt), 0.012 if vt < 20 else 0.004) * rng.uniform(0.8, 1.2)


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    (DEMO / "gsc").mkdir()
    dong = []  # (truy vấn, trang, hiển thị, click, vị trí)
    for q, trang, ht, vt, c in GAI:
        dong.append((q, trang, ht, round(ht * (c if c else ctr(vt))), vt))
    q, ds = TU_CANH_TRANH
    for trang, ht, vt in ds:
        dong.append((q, trang, ht, round(ht * ctr(vt)), vt))
    da_co = {d[0] for d in dong}
    for goc_tu, trang in GOC_TU:  # đuôi dài, ít hiển thị: nhiễu nền thực tế
        for duoi in rng.sample(DUOI, 7):
            q = f"{goc_tu} {duoi}"
            if q in da_co:
                continue
            ht, vt = rng.randint(20, 650), round(rng.uniform(4, 45), 1)
            dong.append((q, trang, ht, round(ht * ctr(vt)), vt))

    # truy-van-theo-trang.csv: kiểu xuất từ Search Console API / Looker Studio (có cả truy vấn và trang)
    with open(DEMO / "gsc" / "truy-van-theo-trang.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Query", "Page", "Clicks", "Impressions", "CTR", "Position"])
        for q, trang, ht, ck, vt in sorted(dong, key=lambda d: -d[2]):
            w.writerow([q, SITE + trang, ck, ht, f"{ck / ht * 100:.2f}%", vt])

    # Queries.csv: đúng kiểu nút "Export" trong giao diện Search Console (gộp theo truy vấn)
    gop = {}
    for q, trang, ht, ck, vt in dong:
        g = gop.setdefault(q, [0, 0, 0.0])
        g[0] += ck
        g[1] += ht
        g[2] += vt * ht
    with open(DEMO / "gsc" / "Queries.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Top queries", "Clicks", "Impressions", "CTR", "Position"])
        for q, (ck, ht, vtht) in sorted(gop.items(), key=lambda kv: -kv[1][1]):
            w.writerow([q, ck, ht, f"{ck / ht * 100:.2f}%", round(vtht / ht, 1)])
    trang_gop = {}
    for q, trang, ht, ck, vt in dong:
        g = trang_gop.setdefault(trang, [0, 0])
        g[0] += ck
        g[1] += ht
    with open(DEMO / "gsc" / "Pages.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Top pages", "Clicks", "Impressions", "CTR"])
        for trang, (ck, ht) in sorted(trang_gop.items(), key=lambda kv: -kv[1][1]):
            w.writerow([SITE + trang, ck, ht, f"{ck / ht * 100:.2f}%"])

    (DEMO / "website.md").write_text(
        "# Website: Văn phòng phẩm An Phát (hư cấu) - vpp-anphat.example\n\n"
        "- Bán văn phòng phẩm, thiết bị văn phòng cho doanh nghiệp và cá nhân tại Hà Nội, TP.HCM.\n"
        "- Mục tiêu 6 tháng: tăng lượt truy cập tự nhiên (organic) 50%, ưu tiên nhóm ghế/bàn công thái học (biên lợi nhuận cao).\n"
        "- Đội nội dung: 1 người, viết được 2 bài/tuần.\n"
        "- Dữ liệu: gsc/ = xuất Google Search Console 3 tháng gần nhất.\n", encoding="utf-8")

    if "--giai-phap" in sys.argv:
        shutil.copy(GOC / "giai-phap" / "phan-tich-gsc.py", DEMO / "phan-tich-gsc.py")
        shutil.copytree(GOC / "giai-phap" / ".claude", DEMO / ".claude")
        print("Đã chép phan-tich-gsc.py + skill brief-seo vào demo/")

    dap_an = {
        "so_dong_truy_van_theo_trang": len(dong), "so_truy_van": len(gop),
        "quy_tac": {"sat_trang_1": "vị trí 8–20 VÀ hiển thị ≥ 2.000", "ctr_thap": "vị trí ≤ 5 VÀ CTR < 40% CTR chuẩn của vị trí đó",
                    "tu_canh_tranh": "≥ 2 trang cùng 1 truy vấn, mỗi trang ≥ 500 hiển thị"},
        "sat_trang_1": ["ghế công thái học (11,2 · 18.400 · +934 click)", "máy hủy tài liệu (14,6 · 7.300)",
                        "ghế công thái học giá rẻ (9,8 · 6.200)", "bàn làm việc chân sắt (11,1 gộp · 5.800 - BỊ KẸT DO TỰ CẠNH TRANH)",
                        "bảng trắng văn phòng (17,4 · 3.900)", "máy hủy tài liệu mini (12,3 · 2.100)"],
        "ctr_thap_tiem_nang": "giấy a4 double a giá: +901 click/3 tháng chỉ nhờ viết lại tiêu đề + mô tả",
        "ctr_thap": ["giấy a4 double a giá (vị trí 2,8 · CTR 1,1%)", "mua giấy a4 số lượng lớn (vị trí 3,4 · CTR 1,4%)"],
        "tu_canh_tranh": {"bàn làm việc chân sắt": ["/ban-lam-viec-chan-sat (9,6)", "/blog/cach-chon-ban-lam-viec (12,9)"]},
        "uu_tien_so_1": "ghế công thái học: hiển thị lớn nhất + đúng nhóm biên lợi nhuận cao (website.md)",
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã tạo demo/gsc/ ({len(gop)} truy vấn, {len(dong)} dòng truy vấn-trang), demo/website.md, dap-an.json")


if __name__ == "__main__":
    main()
