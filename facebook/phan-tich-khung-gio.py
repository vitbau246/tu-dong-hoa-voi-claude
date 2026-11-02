"""Chốt khung giờ đăng sau giai đoạn thử A/B (4 tuần đầu).

1. Sau mỗi bài 24 giờ, mở Meta Business Suite → Nội dung, ghi số liệu vào theo-doi-hieu-qua.csv
   (cột: ma, tiep_can, tuong_tac, tg_xem_tb_giay, chia_se). Script tự điền loai/khung từ lich-dang.csv.
2. Chạy: python phan-tich-khung-gio.py
Quy tắc chốt: khung giờ hơn ≥ 20% ở CẢ tiếp cận và (với video) thời gian xem trung bình → chốt. Không thì thử tiếp.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
NGUONG = 0.20


def so(x):
    try:
        return float(str(x).replace(".", "").replace(",", ".")) if x not in ("", None) else None
    except ValueError:
        return None


def main():
    with open(GOC / "lich-dang.csv", encoding="utf-8-sig") as f:
        lich = {r["ma"]: r for r in csv.DictReader(f)}
    f_td = GOC / "theo-doi-hieu-qua.csv"
    if not f_td.exists():
        with open(f_td, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["ma", "loai", "khung", "tiep_can", "tuong_tac", "tg_xem_tb_giay", "chia_se"])
            for r in lich.values():
                if "(A/B)" in r["khung"]:
                    w.writerow([r["ma"], r["loai"], r["khung"], "", "", "", ""])
        sys.exit(f"Đã tạo {f_td.name} cho các bài thử A/B. Điền số liệu từ Meta Business Suite rồi chạy lại.")

    nhom = defaultdict(lambda: defaultdict(list))
    with open(f_td, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if so(r["tiep_can"]) is None:
                continue
            loai = lich.get(r["ma"], r)["loai"]
            khung = lich.get(r["ma"], r)["khung"].replace(" (A/B)", "")
            nhom[loai][khung].append(r)

    if not nhom:
        sys.exit("Chưa có dòng nào có số liệu trong theo-doi-hieu-qua.csv.")
    for loai, cac_khung in nhom.items():
        print(f"\n■ {loai.upper()}")
        tb = {}
        for khung, ds in cac_khung.items():
            tb[khung] = {k: sum(so(r[k]) or 0 for r in ds) / len(ds) for k in ("tiep_can", "tuong_tac", "tg_xem_tb_giay", "chia_se")}
            t = tb[khung]
            print(f"  {khung:<12} {len(ds)} bài · tiếp cận TB {t['tiep_can']:,.0f} · tương tác {t['tuong_tac']:,.0f} · "
                  f"xem TB {t['tg_xem_tb_giay']:.0f}s · chia sẻ {t['chia_se']:.1f}")
        if len(tb) < 2:
            print("  → Chỉ có 1 khung giờ, chưa so sánh được.")
            continue
        (k1, a), (k2, b) = sorted(tb.items(), key=lambda kv: -kv[1]["tiep_can"])[:2]
        hon_tc = a["tiep_can"] / b["tiep_can"] - 1 if b["tiep_can"] else 0
        hon_xem = (a["tg_xem_tb_giay"] / b["tg_xem_tb_giay"] - 1) if b["tg_xem_tb_giay"] else hon_tc
        it_bai = min(len(cac_khung[k1]), len(cac_khung[k2])) < 2
        if hon_tc >= NGUONG and hon_xem >= NGUONG and not it_bai:
            print(f"  → CHỐT {k1}: hơn {hon_tc:.0%} tiếp cận, {hon_xem:.0%} thời gian xem. Cập nhật cau-hinh.json rồi chạy lap-lich.py.")
        else:
            ly_do = "chưa đủ 2 bài mỗi khung" if it_bai else f"chênh lệch chưa đủ {NGUONG:.0%} (tiếp cận {hon_tc:+.0%}, xem {hon_xem:+.0%})"
            print(f"  → CHƯA CHỐT: {ly_do}. Thử thêm 4 tuần.")


if __name__ == "__main__":
    main()
