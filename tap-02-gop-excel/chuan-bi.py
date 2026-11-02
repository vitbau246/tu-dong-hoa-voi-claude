"""Tập 2 - Tạo 12 file Excel doanh thu năm 2025, mỗi file một kiểu "lộn xộn".

Chạy:  python chuan-bi.py
Kết quả: ./demo/du-lieu/*.xlsx (12 file) và ./dap-an.json (số liệu đúng sau khi làm sạch)

Các "bẫy" được gài (Claude cần phát hiện):
  - Tên và thứ tự cột khác nhau giữa T1-T6 và T7-T12
  - Tên chi nhánh viết nhiều kiểu: "Hà Nội", "Ha Noi", "HN", "hà nội " ...
  - T3, T9 có dòng tiêu đề phía trên bảng
  - T2, T11 ngày tháng lưu dạng chữ "dd/mm/yyyy"
  - T5, T10 số tiền lưu dạng chữ "1.250.000"
  - T8 có 15 dòng bị dán trùng
  - T1, T4, T6, T12 có dòng "TỔNG CỘNG" ở cuối (dễ bị cộng 2 lần)
"""
import json
import random
import shutil
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

from openpyxl import Workbook

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
rng = random.Random(25)

SAN_PHAM = {
    "Máy in laser": 4_850_000,
    "Hộp mực in": 690_000,
    "Giấy A4 (thùng)": 385_000,
    'Màn hình 24"': 3_290_000,
    "Bàn phím cơ": 1_150_000,
    "Chuột không dây": 320_000,
    "Ghế công thái học": 5_400_000,
    "Bàn làm việc": 2_750_000,
}
CHI_NHANH = {
    "Hà Nội": ["Hà Nội", "Ha Noi", "HN", "hà nội "],
    "TP.HCM": ["TP.HCM", "TP HCM", "Hồ Chí Minh", "HCM"],
    "Đà Nẵng": ["Đà Nẵng", "Da Nang"],
    "Cần Thơ": ["Cần Thơ"],
}
TRONG_SO_CN = {"Hà Nội": 0.36, "TP.HCM": 0.40, "Đà Nẵng": 0.15, "Cần Thơ": 0.09}
TEN_FILE = {
    1: "BC ban hang T1.xlsx", 2: "Thang 02 - ban hang.xlsx", 3: "BC T3 (final).xlsx",
    4: "doanh thu thang 4_v2.xlsx", 5: "T5_2025.xlsx", 6: "Ban hang T6 - gui chi Lan.xlsx",
    7: "BC_T07_2025.xlsx", 8: "thang 8.xlsx", 9: "BC T9 (final) (1).xlsx",
    10: "Doanh thu T10 - ban sua.xlsx", 11: "T11.xlsx", 12: "BC ban hang thang 12 FINAL.xlsx",
}
NGAY_TRONG_THANG = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
# Mùa vụ: cuối năm bán mạnh, Tết (T2) giảm
HE_SO_THANG = {1: 1.0, 2: 0.7, 3: 0.95, 4: 1.0, 5: 1.05, 6: 1.1, 7: 0.9, 8: 1.0, 9: 1.15, 10: 1.2, 11: 1.3, 12: 1.45}

def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def sinh_giao_dich(thang):
    so_dong = int(110 * HE_SO_THANG[thang]) + rng.randint(-8, 8)
    ds, da_co = [], set()
    while len(ds) < so_dong:
        cn = rng.choices(list(TRONG_SO_CN), weights=TRONG_SO_CN.values())[0]
        sp = rng.choice(list(SAN_PHAM))
        sl = rng.randint(1, 12) if SAN_PHAM[sp] < 1_000_000 else rng.randint(1, 5)
        ngay = date(2025, thang, rng.randint(1, NGAY_TRONG_THANG[thang]))
        if (ngay, cn, sp, sl) in da_co:  # đảm bảo dữ liệu gốc không có dòng trùng thật
            continue
        da_co.add((ngay, cn, sp, sl))
        ds.append({"ngay": ngay, "cn": cn, "sp": sp, "sl": sl, "gia": SAN_PHAM[sp]})
    ds.sort(key=lambda r: r["ngay"])
    return ds


def vn_so(x):
    return f"{x:,}".replace(",", ".")


def ghi_file(thang, ds):
    wb = Workbook()
    ws = wb.active
    ws.title = f"T{thang}"
    if thang in (3, 9):
        ws.append([f"BÁO CÁO BÁN HÀNG THÁNG {thang}/2025"])
        ws.append(["Người lập: Phòng Kinh doanh"])
        ws.append([])
    kieu_moi = thang >= 7
    if kieu_moi:
        ws.append(["Ngày bán", "Tên SP", "CN", "Số lượng", "Giá", "Doanh thu"])
    else:
        ws.append(["Ngày", "Chi nhánh", "Sản phẩm", "SL", "Đơn giá", "Thành tiền"])

    dong_ghi = list(ds)
    if thang == 8:  # dán trùng 15 dòng
        dong_ghi += rng.sample(ds, 15)
        dong_ghi.sort(key=lambda r: r["ngay"])

    for r in dong_ghi:
        cn = rng.choice(CHI_NHANH[r["cn"]])
        ngay = r["ngay"].strftime("%d/%m/%Y") if thang in (2, 11) else r["ngay"]
        tien = r["sl"] * r["gia"]
        gia, tt = (vn_so(r["gia"]), vn_so(tien)) if thang in (5, 10) else (r["gia"], tien)
        if kieu_moi:
            ws.append([ngay, r["sp"], cn, r["sl"], gia, tt])
        else:
            ws.append([ngay, cn, r["sp"], r["sl"], gia, tt])
        if not isinstance(ngay, str):
            ws.cell(ws.max_row, 1).number_format = "dd/mm/yyyy"

    if thang in (1, 4, 6, 12):
        tong = sum(r["sl"] * r["gia"] for r in dong_ghi)
        ws.append([])
        ws.append(["TỔNG CỘNG", None, None, sum(r["sl"] for r in dong_ghi), None, tong])

    for col, w in zip("ABCDEF", (12, 18, 20, 10, 12, 14)):
        ws.column_dimensions[col].width = w
    wb.save(DEMO / "du-lieu" / TEN_FILE[thang])


def main():
    lam_moi(DEMO)
    (DEMO / "du-lieu").mkdir(parents=True)

    tat_ca = []
    for thang in range(1, 13):
        ds = sinh_giao_dich(thang)
        ghi_file(thang, ds)
        tat_ca += [dict(r, thang=thang) for r in ds]

    # Đáp án tính từ dữ liệu sạch (trước khi gài lỗi)
    tong = sum(r["sl"] * r["gia"] for r in tat_ca)
    theo_thang = defaultdict(int)
    theo_cn = defaultdict(int)
    theo_sp = defaultdict(int)
    for r in tat_ca:
        tien = r["sl"] * r["gia"]
        theo_thang[r["thang"]] += tien
        theo_cn[r["cn"]] += tien
        theo_sp[r["sp"]] += tien
    top5 = sorted(theo_sp.items(), key=lambda kv: -kv[1])[:5]
    thang_cao_nhat = max(theo_thang, key=theo_thang.get)

    # Con số "sai" nếu cộng thẳng cột tiền bằng SUM trong Excel:
    # dính dòng trùng + dòng TỔNG CỘNG, và SUM bỏ qua ô chữ ở T5, T10
    from openpyxl import load_workbook
    tong_sai = 0
    for thang in range(1, 13):
        ws = load_workbook(DEMO / "du-lieu" / TEN_FILE[thang]).active
        tong_sai += sum(row[5] for row in ws.iter_rows(values_only=True) if isinstance(row[5], (int, float)))
    ws8 = load_workbook(DEMO / "du-lieu" / TEN_FILE[8]).active
    t8_trung = sum(row[5] for row in ws8.iter_rows(min_row=2, values_only=True) if isinstance(row[5], int)) - theo_thang[8]

    dap_an = {
        "so_giao_dich_sach": len(tat_ca),
        "tong_doanh_thu_2025": tong,
        "tong_doanh_thu_2025_doc": f"{tong / 1e9:.2f} tỷ đồng",
        "doanh_thu_theo_thang": {f"T{k}": v for k, v in sorted(theo_thang.items())},
        "thang_cao_nhat": f"T{thang_cao_nhat}",
        "doanh_thu_theo_chi_nhanh": dict(sorted(theo_cn.items(), key=lambda kv: -kv[1])),
        "top5_san_pham": dict(top5),
        "so_dong_trung_T8": 15,
        "gia_tri_dong_trung_T8": t8_trung,
        "cac_cach_viet_chi_nhanh": CHI_NHANH,
        "file_co_dong_tong_cong": [TEN_FILE[m] for m in (1, 4, 6, 12)],
        "tong_SAI_neu_cong_SUM_thang": tong_sai,
        "chenh_lech_neu_cong_SUM_thang": tong_sai - tong,
        "giai_thich_sai": "SUM cộng cả 15 dòng trùng T8 và 4 dòng TỔNG CỘNG, nhưng bỏ sót T5, T10 vì số lưu dạng chữ",
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dap_an, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
