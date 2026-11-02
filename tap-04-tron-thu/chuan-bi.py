"""Tập 4 - Tạo danh sách khách mời (Excel) và mẫu thư mời (Word) để trộn thư.

Chạy:  python chuan-bi.py
Kết quả: ./demo/danh-sach-khach-moi.xlsx, ./demo/mau-thu-moi.docx, ./dap-an.json

Bẫy được gài:
  - 1 khách bị nhập 2 lần (41 dòng nhưng chỉ 40 người)
  - 2 khách thiếu email, 1 email sai định dạng
  - 1 khách thiếu danh xưng, tên trung tính "Trần Minh Anh" -> không được tự đoán Ông/Bà
"""
import json
import random
import shutil
import sys
import unicodedata
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
rng = random.Random(44)

HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đặng", "Bùi", "Đỗ", "Ngô"]
DEM_NAM = ["Văn", "Đức", "Minh", "Quang", "Hữu", "Thành"]
DEM_NU = ["Thị", "Thu", "Ngọc", "Thanh", "Phương", "Mai"]
TEN_NAM = ["Hùng", "Dũng", "Tuấn", "Long", "Nam", "Sơn", "Phong", "Khánh", "Trung", "Hiếu"]
TEN_NU = ["Lan", "Hương", "Hà", "Linh", "Trang", "Hạnh", "Yến", "Thảo", "Ngân", "Vy"]
CHUC_VU = ["Giám đốc", "Phó Giám đốc", "Trưởng phòng CNTT", "Trưởng phòng Kinh doanh", "Kế toán trưởng",
           "Chuyên viên", "Trưởng nhóm Dữ liệu"]
# Tên miền .example được dành riêng (RFC 2606): email nháp lỡ bấm gửi cũng không tới người thật
DON_VI = {"Công ty TNHH Sao Mai Demo": "saomai", "Công ty CP Thương mại Hòa Bình Demo": "hoabinh",
          "Ngân hàng Mẫu Thịnh Vượng": "thinhvuongbank", "Tập đoàn Demo Phát Đạt": "phatdat",
          "Công ty CP Logistics Đông Dương Demo": "dongduonglog", "Bệnh viện Đa khoa Demo An Khang": "ankhang",
          "Trường Đại học Demo Công nghệ": "dhcongnghe", "Công ty TNHH Phần mềm Demo Ánh Dương": "anhduongsoft"}

def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def khong_dau(s):
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def tao_khach():
    ds, ten_da_co = [], set()
    while len(ds) < 40:
        nam = rng.random() < 0.55
        ho_ten = f"{rng.choice(HO)} {rng.choice(DEM_NAM if nam else DEM_NU)} {rng.choice(TEN_NAM if nam else TEN_NU)}"
        if ho_ten in ten_da_co:
            continue
        ten_da_co.add(ho_ten)
        don_vi = rng.choice(list(DON_VI))
        p = khong_dau(ho_ten).lower().split()
        email = f"{p[-1]}.{''.join(x[0] for x in p[:-1])}{rng.randint(1, 99)}@{DON_VI[don_vi]}.example"
        ds.append({"danh_xung": "Ông" if nam else "Bà", "ho_ten": ho_ten, "chuc_vu": rng.choice(CHUC_VU),
                   "don_vi": don_vi, "email": email, "phien": rng.choice(["Sáng", "Chiều"]), "ban": rng.randint(1, 12)})
    return ds


def tao_mau():
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(13)

    def para(text="", bold=False, size=None, align=None, color=None, italic=False):
        p = d.add_paragraph()
        if align:
            p.alignment = align
        r = p.add_run(text)
        r.bold, r.italic = bold, italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor(*color)
        return p

    para("CÔNG TY CỔ PHẦN DEMO VIỆT", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=(0x1F, 0x4E, 0x79))
    para("Tầng 5, 18 Phố Mẫu, Q. Cầu Giấy, Hà Nội", size=10, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)
    para()
    para("THƯ MỜI", bold=True, size=22, align=WD_ALIGN_PARAGRAPH.CENTER, color=(0xC0, 0x00, 0x00))
    para("Hội nghị Khách hàng 2026: \"Làm việc thông minh cùng AI\"", bold=True, size=14,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para()
    p = d.add_paragraph()
    p.add_run("Kính gửi: ").bold = True
    p.add_run("{{danh_xung}} {{ho_ten}}").bold = True
    para("{{chuc_vu}} – {{don_vi}}", italic=True)
    para()
    para("Công ty Cổ phần Demo Việt trân trọng kính mời {{danh_xung}} tới tham dự Hội nghị Khách hàng 2026, "
         "nơi chúng tôi chia sẻ các giải pháp tự động hóa công việc văn phòng bằng trí tuệ nhân tạo.")
    para("Thời gian: {{thoi_gian}}, Thứ Sáu ngày 20/11/2026")
    para("Địa điểm: Trung tâm Hội nghị Demo, 99 Đường Mẫu, Hà Nội")
    para("Vị trí: Bàn số {{ban}}")
    para()
    para("Sự hiện diện của {{danh_xung}} là niềm vinh hạnh lớn đối với chúng tôi. "
         "Vui lòng xác nhận tham dự trước ngày 13/11/2026.")
    para()
    para("Trân trọng!", italic=True, align=WD_ALIGN_PARAGRAPH.RIGHT)
    para("BAN TỔ CHỨC", bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT)
    para()
    para("Tài liệu mẫu phục vụ video hướng dẫn. Mọi tên người, đơn vị đều hư cấu.", size=8, italic=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, color=(0x99, 0x99, 0x99))
    d.save(DEMO / "mau-thu-moi.docx")


def main():
    lam_moi(DEMO)
    DEMO.mkdir(parents=True, exist_ok=True)

    ds = tao_khach()
    # Bẫy
    ds[6]["email"] = None
    ds[23]["email"] = None
    ds[15]["email"] = ds[15]["email"].replace("@", ".at.")  # sai định dạng
    ds[31].update(danh_xung=None, ho_ten="Trần Minh Anh",  # tên trung tính, không có danh xưng
                  email=f"anh.tm{rng.randint(1, 99)}@{ds[31]['email'].split('@')[1]}")
    trung = dict(ds[12])
    ghi = ds[:28] + [trung] + ds[28:]  # dòng 29 trùng với dòng 13

    wb = Workbook()
    ws = wb.active
    ws.title = "Khach-moi"
    tieu_de = ["STT", "Danh xưng", "Họ và tên", "Chức vụ", "Đơn vị", "Email", "Phiên", "Bàn số"]
    ws.append(tieu_de)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E79")
    for i, k in enumerate(ghi, 1):
        ws.append([i, k["danh_xung"], k["ho_ten"], k["chuc_vu"], k["don_vi"], k["email"], k["phien"], k["ban"]])
    for col, w in zip("ABCDEFGH", (6, 11, 22, 26, 38, 42, 9, 8)):
        ws.column_dimensions[col].width = w
    wb.save(DEMO / "danh-sach-khach-moi.xlsx")
    tao_mau()

    dap_an = {
        "so_dong_trong_excel": len(ghi),
        "so_khach_duy_nhat": len(ds),
        "dong_trung": {"dong_excel": [13, 29], "ho_ten": trung["ho_ten"]},
        "thieu_email": [ds[6]["ho_ten"], ds[23]["ho_ten"]],
        "email_sai_dinh_dang": {"ho_ten": ds[15]["ho_ten"], "email": ds[15]["email"]},
        "thieu_danh_xung": "Trần Minh Anh (tên trung tính - KHÔNG được tự đoán Ông/Bà)",
        "so_thu_moi_can_tao": len(ds),
        "so_email_nhap_tao_duoc": len(ds) - 3,
        "phien": {"Sáng": "08:30 - 11:30", "Chiều": "13:30 - 16:30"},
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dap_an, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
