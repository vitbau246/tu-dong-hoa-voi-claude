"""Tập 9 - Tạo 3 báo giá phần mềm CRM (docx, pdf, docx) + yêu cầu dự án để "đội AI" phân tích song song.

Chạy:  python chuan-bi.py              -> demo/bao-gia/*, demo/yeu-cau-du-an.md, dap-an.json
       python chuan-bi.py --giai-phap  -> chép thêm .claude/agents/ (2 subagent mẫu)

Bẫy: Báo giá B ghi to "189.000.000 đ trọn gói 3 năm" nhưng chú thích chữ nhỏ + phụ lục có:
  - giá chỉ cho 30 người dùng, thêm người 1.500.000 đ/người/năm
  - phí triển khai + chuyển đổi dữ liệu 45.000.000 đ (Phụ lục 2)
  - phí bảo trì từ năm 2: 18% giá trị hợp đồng/năm
  - dữ liệu lưu tại Singapore (yêu cầu: tại Việt Nam), phí xuất dữ liệu khi chấm dứt 25.000.000 đ
=> Tổng chi phí 3 năm cho 50 người: B đắt nhất.
"""
import json
import shutil
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-B", "C:/Windows/Fonts/arialbd.ttf"))

YEU_CAU = """# Yêu cầu dự án: Phần mềm Quản lý khách hàng (CRM)

- **Đơn vị:** Công ty CP Demo Việt
- **Số người dùng:** 50 (Phòng Kinh doanh 35, Chăm sóc khách hàng 15)
- **Thời gian tính chi phí:** 3 năm

## Yêu cầu bắt buộc
1. Dữ liệu khách hàng **lưu trữ tại Việt Nam**.
2. Có ứng dụng di động cho nhân viên kinh doanh.
3. Tích hợp email (Outlook/Microsoft 365).
4. Giao diện và hỗ trợ kỹ thuật bằng tiếng Việt.
5. Chuyển đổi dữ liệu từ file Excel hiện có (~12.000 khách hàng).

## Ưu tiên
- Tổng chi phí sở hữu 3 năm (TCO) thấp.
- Cam kết chất lượng dịch vụ (SLA) và thời gian phản hồi sự cố rõ ràng.
- Điều khoản thoát hợp đồng (xuất dữ liệu) không bất lợi.
"""


def docx_bao_gia(path, ncc, dong):
    d = Document()
    d.styles["Normal"].font.name = "Arial"
    d.styles["Normal"].font.size = Pt(11)
    h = d.add_heading(f"BÁO GIÁ GIẢI PHÁP CRM - {ncc}", 0)
    for r in h.runs:
        r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    d.add_paragraph("Kính gửi: Công ty CP Demo Việt")
    for loai, nd in dong:
        if loai == "h":
            d.add_heading(nd, 2)
        elif loai == "p":
            d.add_paragraph(nd)
        elif loai == "t":
            t = d.add_table(rows=len(nd), cols=len(nd[0]))
            t.style = "Table Grid"
            for i, hang in enumerate(nd):
                for j, o in enumerate(hang):
                    t.cell(i, j).text = o
    d.add_paragraph("Tài liệu hư cấu phục vụ video hướng dẫn.").runs[0].font.size = Pt(8)
    d.save(path)


def pdf_bao_gia_B(path):
    W, H = A4
    c = canvas.Canvas(str(path), pagesize=A4)

    def chan_trang(so):
        c.setFont("Arial", 7)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawCentredString(W / 2, 22, f"Công ty CP Phần mềm Sao Việt Demo · Tài liệu hư cấu phục vụ video hướng dẫn · Trang {so}/3")
        c.setFillColorRGB(0, 0, 0)

    # Trang 1: quảng cáo
    c.setFillColorRGB(0.95, 0.45, 0.1)
    c.rect(0, H - 120, W, 120, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Arial-B", 22)
    c.drawString(40, H - 60, "SAO VIỆT CRM - GÓI BUSINESS")
    c.setFont("Arial", 12)
    c.drawString(40, H - 85, "Báo giá dành riêng cho Công ty CP Demo Việt")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Arial-B", 40)
    c.setFillColorRGB(0.8, 0.1, 0.1)
    c.drawCentredString(W / 2, H - 230, "189.000.000 đ *")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Arial-B", 16)
    c.drawCentredString(W / 2, H - 262, "TRỌN GÓI 3 NĂM - TIẾT KIỆM ĐẾN 40%")
    c.setFont("Arial", 12)
    y = H - 320
    for dong in ["• Ứng dụng di động iOS/Android", "• Tích hợp Microsoft 365 / Outlook",
                 "• Giao diện tiếng Việt 100%", "• Hạ tầng đám mây chuẩn quốc tế",
                 "• Hỗ trợ kỹ thuật tận tâm", "• Triển khai nhanh trong 2 tuần"]:
        c.drawString(90, y, dong)
        y -= 24
    c.setFont("Arial", 6.5)
    c.setFillColorRGB(0.45, 0.45, 0.45)
    c.drawString(40, 70, "* Giá áp dụng cho tối đa 30 người dùng. Người dùng bổ sung: 1.500.000 đ/người/năm. Chưa bao gồm phí triển khai")
    c.drawString(40, 61, "và chuyển đổi dữ liệu (xem Phụ lục 2). Phí hỗ trợ & bảo trì từ năm thứ 2 theo Điều 5. Giá chưa gồm VAT.")
    c.setFillColorRGB(0, 0, 0)
    chan_trang(1)
    c.showPage()

    # Trang 2: điều khoản
    c.setFont("Arial-B", 14)
    c.drawString(40, H - 60, "ĐIỀU KHOẢN THƯƠNG MẠI")
    c.setFont("Arial", 10)
    y = H - 90
    for dong in [
        "Điều 1. Phạm vi: cung cấp quyền sử dụng phần mềm Sao Việt CRM gói Business dạng thuê bao (SaaS).",
        "Điều 2. Thời hạn: 36 tháng kể từ ngày nghiệm thu triển khai.",
        "Điều 3. Hạ tầng: dữ liệu được lưu trữ tại trung tâm dữ liệu của đối tác tại Singapore.",
        "Điều 4. Thanh toán: 100% giá trị gói trong 15 ngày kể từ ngày ký hợp đồng.",
        "Điều 5. Hỗ trợ & bảo trì: miễn phí năm đầu (giờ hành chính 8x5). Từ năm thứ 2, phí hỗ trợ & bảo trì",
        "            bằng 18% giá trị gói/năm, thanh toán đầu mỗi năm.",
        "Điều 6. Chấm dứt: khi chấm dứt hợp đồng, bên mua có thể yêu cầu xuất toàn bộ dữ liệu với phí",
        "            25.000.000 đ/lần. Dữ liệu bị xóa sau 30 ngày kể từ ngày chấm dứt.",
        "Điều 7. SLA: mục tiêu sẵn sàng 99,0%/tháng. Không áp dụng bồi hoàn.",
    ]:
        c.drawString(40, y, dong)
        y -= 18
    chan_trang(2)
    c.showPage()

    # Trang 3: phụ lục
    c.setFont("Arial-B", 14)
    c.drawString(40, H - 60, "PHỤ LỤC")
    c.setFont("Arial-B", 11)
    c.drawString(40, H - 90, "Phụ lục 1. Danh sách tính năng gói Business")
    c.setFont("Arial", 10)
    c.drawString(55, H - 108, "Quản lý khách hàng, cơ hội bán hàng, báo cáo, ứng dụng di động, tích hợp email.")
    c.setFont("Arial-B", 11)
    c.drawString(40, H - 140, "Phụ lục 2. Phí triển khai")
    c.setFont("Arial", 10)
    c.drawString(55, H - 158, "Cấu hình, đào tạo 2 buổi, chuyển đổi dữ liệu từ Excel (tối đa 20.000 bản ghi): 45.000.000 đ (một lần).")
    chan_trang(3)
    c.save()


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    (DEMO / "bao-gia").mkdir()
    (DEMO / "yeu-cau-du-an.md").write_text(YEU_CAU, encoding="utf-8")

    docx_bao_gia(DEMO / "bao-gia" / "A - Dong A Digital - bao gia CRM.docx", "ĐÔNG Á DIGITAL (DEMO)", [
        ("h", "1. Chi phí"),
        ("t", [["Hạng mục", "Đơn giá", "Số lượng", "Thành tiền"],
               ["Thuê bao phần mềm (người dùng/năm)", "1.200.000 đ", "50 người × 3 năm", "180.000.000 đ"],
               ["Triển khai, cấu hình, chuyển đổi dữ liệu, đào tạo 4 buổi", "60.000.000 đ", "1", "60.000.000 đ"],
               ["Hỗ trợ & bảo trì 3 năm", "Đã bao gồm", "", "0 đ"],
               ["TỔNG CỘNG 3 NĂM (chưa VAT)", "", "", "240.000.000 đ"]]),
        ("h", "2. Điều khoản chính"),
        ("p", "• Dữ liệu lưu trữ tại trung tâm dữ liệu ở Hà Nội và TP.HCM (sao lưu chéo)."),
        ("p", "• Ứng dụng di động iOS/Android. Tích hợp Microsoft 365."),
        ("p", "• Hỗ trợ giờ hành chính 8x5 qua điện thoại, email; phản hồi sự cố nghiêm trọng trong 4 giờ."),
        ("p", "• SLA sẵn sàng 99,5%/tháng; vi phạm hoàn 5% phí tháng."),
        ("p", "• Chấm dứt hợp đồng: xuất dữ liệu miễn phí định dạng Excel/CSV."),
        ("p", "• Hạn chế: ứng dụng di động chưa hỗ trợ làm việc ngoại tuyến (dự kiến Q2/2027)."),
        ("p", "• Thanh toán theo năm, đơn giá cố định trong 3 năm."),
    ])
    pdf_bao_gia_B(DEMO / "bao-gia" / "B - Sao Viet - bao gia CRM.pdf")
    docx_bao_gia(DEMO / "bao-gia" / "C - Hoan Cau Enterprise - bao gia CRM.docx", "HOÀN CẦU ENTERPRISE (DEMO)", [
        ("h", "1. Gói Enterprise Premium cho 50 người dùng, 3 năm"),
        ("t", [["Hạng mục", "Thành tiền"],
               ["Bản quyền 50 người dùng × 3 năm", "255.000.000 đ"],
               ["Triển khai trọn gói + chuyển đổi dữ liệu không giới hạn + đào tạo 6 buổi", "75.000.000 đ"],
               ["Hỗ trợ 24/7, quản lý tài khoản riêng", "Đã bao gồm"],
               ["TỔNG CỘNG (chưa VAT)", "330.000.000 đ"]]),
        ("h", "2. Cam kết"),
        ("p", "• Dữ liệu lưu tại Việt Nam (TP.HCM), đạt chứng nhận ISO 27001."),
        ("p", "• SLA 99,9%/tháng; vi phạm hoàn 10–25% phí tháng; phản hồi sự cố nghiêm trọng trong 1 giờ, 24/7."),
        ("p", "• Ứng dụng di động có chế độ ngoại tuyến. Tích hợp Microsoft 365, Zalo OA."),
        ("p", "• Xuất dữ liệu miễn phí bất kỳ lúc nào qua API hoặc file."),
        ("p", "• Thanh toán 3 đợt theo năm. Đơn giá cố định 3 năm."),
    ])

    if "--giai-phap" in sys.argv:
        shutil.copytree(GOC / "giai-phap" / ".claude", DEMO / ".claude")
        print("Đã chép .claude/agents/ vào demo/")

    b_tco = 189_000_000 + 20 * 1_500_000 * 3 + 45_000_000 + int(189_000_000 * 0.18) * 2
    dap_an = {
        "TCO_3_nam_50_nguoi": {
            "A - Đông Á Digital": 240_000_000,
            "B - Sao Việt": b_tco,
            "C - Hoàn Cầu Enterprise": 330_000_000,
        },
        "chi_tiet_B": {
            "gia_quang_cao_30_nguoi": 189_000_000,
            "them_20_nguoi_x_1.5tr_x_3_nam": 90_000_000,
            "phi_trien_khai_phu_luc_2": 45_000_000,
            "bao_tri_nam_2_va_3_(18%/nam)": int(189_000_000 * 0.18) * 2,
            "rui_ro_ngoai_TCO": "Phí xuất dữ liệu khi chấm dứt 25.000.000 đ; dữ liệu lưu tại Singapore (VI PHẠM yêu cầu bắt buộc 1); SLA 99,0% không bồi hoàn; hỗ trợ 8x5; trả trước 100%",
        },
        "xep_hang_TCO": ["A (240tr)", "C (330tr)", f"B ({b_tco / 1e6:.2f}tr)"],
        "khuyen_nghi": "A nếu ưu tiên chi phí (đáp ứng đủ 5 yêu cầu bắt buộc; điểm yếu: app chưa offline, hỗ trợ 8x5). "
                       "C nếu cần SLA 99,9% và hỗ trợ 24/7 (đắt hơn A 90tr). B bị loại do vi phạm yêu cầu lưu trữ dữ liệu tại Việt Nam.",
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dap_an, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
