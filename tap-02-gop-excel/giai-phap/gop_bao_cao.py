"""Gộp các file Excel doanh thu tháng thành một file tổng hợp (không sửa file gốc).

HƯỚNG DẪN SỬ DỤNG
    python gop_bao_cao.py                      # đọc du-lieu/ cạnh script
    python gop_bao_cao.py "D:\\BC 2025"         # đọc thư mục khác
    python gop_bao_cao.py "D:\\BC 2025" -o "D:\\ket-qua.xlsx"

    Tham số:
      thu_muc      Thư mục chứa các file .xlsx (mặc định: du-lieu/ cạnh script)
      -o, --output File kết quả (mặc định: tong-hop-2025.xlsx cạnh script)

    Kết quả gồm 4 sheet: Du-lieu-sach, Tong-hop, Top-san-pham, Nhat-ky-lam-sach.

    Lưu ý:
      - Mỗi file 1 sheet; dòng tên cột được tự tìm (có thể nằm dưới vài dòng tiêu đề).
      - Gặp tên chi nhánh lạ, script dừng với KeyError -> thêm cách viết đó vào CHI_NHANH.
      - File đang mở trong Excel (file ~$...) được bỏ qua.
"""
import argparse
import glob
import os
from collections import Counter, defaultdict
from datetime import datetime

import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, PatternFill

THU_MUC = os.path.dirname(os.path.abspath(__file__))
NGUON = os.path.join(THU_MUC, "du-lieu")
DICH = os.path.join(THU_MUC, "tong-hop-2025.xlsx")

# Tên cột gốc -> tên chuẩn (2 bộ tên cột đã gặp khi khảo sát)
COT = {
    "Ngày": "ngay", "Ngày bán": "ngay",
    "Chi nhánh": "cn", "CN": "cn",
    "Sản phẩm": "sp", "Tên SP": "sp",
    "SL": "sl", "Số lượng": "sl",
    "Đơn giá": "gia", "Giá": "gia",
    "Thành tiền": "tien", "Doanh thu": "tien",
}
CHI_NHANH = {
    "hà nội": "Hà Nội", "hn": "Hà Nội", "ha noi": "Hà Nội",
    "hồ chí minh": "TP.HCM", "tp.hcm": "TP.HCM", "tp hcm": "TP.HCM", "hcm": "TP.HCM",
    "đà nẵng": "Đà Nẵng", "da nang": "Đà Nẵng",
    "cần thơ": "Cần Thơ",
}
THU_TU_CN = ["Hà Nội", "TP.HCM", "Đà Nẵng", "Cần Thơ"]
DINH_DANG_SO = "#,##0"  # Excel tiếng Việt hiển thị 1.000.000


def so(v):
    """Số thật hoặc chữ kiểu '4.850.000' -> int."""
    if isinstance(v, str):
        return int(v.strip().replace(".", "").replace(",", ""))
    return int(v)


def doc_file(duong_dan, nhat_ky):
    ten = os.path.basename(duong_dan)
    ws = openpyxl.load_workbook(duong_dan, read_only=True).active
    hang = list(ws.iter_rows(values_only=True))

    # 1. Tìm dòng tên cột (không mặc định là dòng 1)
    i_hdr = next(i for i, r in enumerate(hang) if sum(v in COT for v in r) >= 4)
    if i_hdr:
        nhat_ky.append((ten, "Bỏ dòng tiêu đề thừa phía trên tên cột", i_hdr))
    hdr = [COT.get(v) for v in hang[i_hdr]]
    if hdr[1] == "sp":
        nhat_ky.append((ten, "Cột đặt tên/thứ tự khác (bộ Ngày bán/Tên SP/CN...) -> ánh xạ theo tên", 1))

    dem = Counter()
    da_thay = set()
    ket_qua = []
    for r in hang[i_hdr + 1:]:
        if all(v is None for v in r):
            dem["Bỏ dòng trống"] += 1
            continue
        d = dict(zip(hdr, r))
        if isinstance(d["ngay"], str) and "TỔNG" in d["ngay"].upper():
            dem["Bỏ dòng TỔNG CỘNG"] += 1
            continue
        ngay = d["ngay"]
        if isinstance(ngay, str):
            ngay = datetime.strptime(ngay.strip(), "%d/%m/%Y")
            dem["Đổi ngày dạng chữ -> ngày thật"] += 1
        if isinstance(d["gia"], str) or isinstance(d["tien"], str):
            dem["Đổi số dạng chữ '4.850.000' -> số"] += 1
        cn_goc = d["cn"]
        cn = CHI_NHANH[cn_goc.strip().lower()]
        if cn_goc != cn:
            dem["Chuẩn hóa tên chi nhánh"] += 1
        sl, gia, tien = so(d["sl"]), so(d["gia"]), so(d["tien"])
        if sl * gia != tien:
            dem["CẢNH BÁO: SL x Đơn giá ≠ Thành tiền (giữ nguyên)"] += 1
        dong = [ngay.date(), ngay.month, cn, d["sp"].strip(), sl, gia, tien]
        # So trùng SAU khi chuẩn hóa: "HN" và "Hà Nội" cùng giao dịch vẫn là trùng
        if tuple(dong) in da_thay:
            dem["Bỏ dòng trùng lặp (nhập trùng, so sau chuẩn hóa)"] += 1
            continue
        da_thay.add(tuple(dong))
        ket_qua.append(dong)

    nhat_ky.extend((ten, loi, n) for loi, n in dem.items())
    return ket_qua


def tieu_de(ws, cot):
    ws.append(cot)
    for c in ws[ws.max_row]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E78")


def do_rong(ws, rong):
    for i, w in enumerate(rong):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w


def main():
    ap = argparse.ArgumentParser(description="Gộp file Excel doanh thu tháng thành file tổng hợp.")
    ap.add_argument("thu_muc", nargs="?", default=NGUON, help="thư mục chứa các file .xlsx")
    ap.add_argument("-o", "--output", default=DICH, help="đường dẫn file kết quả")
    args = ap.parse_args()

    files = [f for f in sorted(glob.glob(os.path.join(args.thu_muc, "*.xlsx")))
             if not os.path.basename(f).startswith("~$")]
    if not files:
        raise SystemExit(f"Không tìm thấy file .xlsx nào trong: {args.thu_muc}")
    dich = os.path.abspath(args.output)
    if any(os.path.abspath(f) == dich for f in files):
        raise SystemExit("File kết quả không được trùng với một file nguồn.")

    nhat_ky, du_lieu = [], []
    for f in files:
        du_lieu += doc_file(f, nhat_ky)
    du_lieu.sort(key=lambda r: (r[0], r[2], r[3]))

    wb = openpyxl.Workbook()

    # 1. Du-lieu-sach
    ws = wb.active
    ws.title = "Du-lieu-sach"
    tieu_de(ws, ["Ngày", "Tháng", "Chi nhánh", "Sản phẩm", "SL", "Đơn giá", "Thành tiền"])
    for r in du_lieu:
        ws.append(r)
        ws.cell(ws.max_row, 1).number_format = "dd/mm/yyyy"
        for c in (6, 7):
            ws.cell(ws.max_row, c).number_format = DINH_DANG_SO
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    do_rong(ws, [12, 8, 12, 20, 6, 14, 16])

    # 2. Tong-hop: tháng x chi nhánh
    bang = defaultdict(int)
    for r in du_lieu:
        bang[(r[1], r[2])] += r[6]
    ws = wb.create_sheet("Tong-hop")
    tieu_de(ws, ["Tháng"] + THU_TU_CN + ["Tổng"])
    for t in range(1, 13):
        dong = [bang[(t, cn)] for cn in THU_TU_CN]
        ws.append([f"T{t}"] + dong + [sum(dong)])
    tong_cot = [sum(bang[(t, cn)] for t in range(1, 13)) for cn in THU_TU_CN]
    tong_nam = sum(tong_cot)
    ws.append(["Tổng"] + tong_cot + [tong_nam])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=2, min_col=2):
        for c in row:
            c.number_format = DINH_DANG_SO
    for c in ws["F"]:
        c.font = Font(bold=True)
    do_rong(ws, [8, 16, 16, 16, 16, 18])

    # 3. Top-san-pham + biểu đồ 12 tháng
    theo_sp = defaultdict(lambda: [0, 0])
    for r in du_lieu:
        theo_sp[r[3]][0] += r[4]
        theo_sp[r[3]][1] += r[6]
    ws = wb.create_sheet("Top-san-pham")
    tieu_de(ws, ["Hạng", "Sản phẩm", "SL", "Doanh thu", "Tỷ trọng"])
    for i, (sp, (sl, dt)) in enumerate(sorted(theo_sp.items(), key=lambda x: -x[1][1])[:5], 1):
        ws.append([i, sp, sl, dt, dt / tong_nam])
        ws.cell(ws.max_row, 4).number_format = DINH_DANG_SO
        ws.cell(ws.max_row, 5).number_format = "0.0%"
    ws.append([])
    tieu_de(ws, ["Tháng", "Doanh thu"])
    dau = ws.max_row
    for t in range(1, 13):
        ws.append([f"T{t}", sum(bang[(t, cn)] for cn in THU_TU_CN)])
        ws.cell(ws.max_row, 2).number_format = DINH_DANG_SO
    bd = BarChart()
    bd.title = "Doanh thu 12 tháng 2025"
    bd.y_axis.title = "VNĐ"
    bd.y_axis.numFmt = DINH_DANG_SO
    bd.legend = None
    bd.add_data(Reference(ws, min_col=2, min_row=dau, max_row=dau + 12), titles_from_data=True)
    bd.set_categories(Reference(ws, min_col=1, min_row=dau + 1, max_row=dau + 12))
    bd.width, bd.height = 22, 10
    ws.add_chart(bd, "G2")
    do_rong(ws, [8, 20, 8, 16, 10])

    # 4. Nhat-ky-lam-sach
    ws = wb.create_sheet("Nhat-ky-lam-sach")
    tieu_de(ws, ["File", "Lỗi đã xử lý", "Số dòng"])
    for dong in nhat_ky:
        ws.append(list(dong))
    ws.append(["TỔNG", "Số dòng dữ liệu sạch", len(du_lieu)])
    ws[ws.max_row][0].font = Font(bold=True)
    do_rong(ws, [32, 62, 10])

    wb.save(dich)
    print(f"Đã tạo {dich}: {len(files)} file, {len(du_lieu)} dòng sạch")
    for t in range(1, 13):
        print(f"  T{t:>2}: {sum(bang[(t, cn)] for cn in THU_TU_CN):>15,}".replace(",", "."))
    print(f"TỔNG DOANH THU 2025: {tong_nam:,} đ".replace(",", "."))


if __name__ == "__main__":
    main()
