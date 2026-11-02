import csv, sys
sys.stdout.reconfigure(encoding="utf-8")
def ghi(ma, trang_thai, ghi_chu, cach="FoxFlow · Business Suite (hẹn giờ)"):
    rows = list(csv.DictReader(open("lich-dang.csv", encoding="utf-8-sig")))
    for r in rows:
        if r["ma"] == ma:
            r["trang_thai"], r["ghi_chu"] = trang_thai, ghi_chu
            tg = r["thoi_gian"]
    with open("lich-dang.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    with open("da-dang.csv", "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([tg, ma, cach, "", ghi_chu])
    print("da ghi", ma, tg)
if __name__ == "__main__":
    ghi(sys.argv[1], sys.argv[2], sys.argv[3])
