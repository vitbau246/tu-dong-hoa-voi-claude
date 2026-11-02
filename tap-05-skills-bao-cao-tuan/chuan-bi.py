"""Tập 5 - Tạo nhật ký làm việc 2 tuần + bảng theo dõi công việc + mẫu báo cáo tuần.

Chạy:  python chuan-bi.py              -> demo/ ở trạng thái BAN ĐẦU (chưa có CLAUDE.md, chưa có skill)
       python chuan-bi.py --giai-phap  -> chép thêm CLAUDE.md và .claude/skills/bao-cao-tuan từ giai-phap/
"""
import shutil
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"

# Nhật ký viết vội, nhiều chữ viết tắt (đúng như ngoài đời). Tuần 43 và 44 năm 2026.
NHAT_KY = {
    "2026-10-19": """- sáng họp giao ban, a Hùng nhắc bc Q3 phải xong trước 23/10
- rà soát dự thảo HĐ bảo trì với NCC Minh An, còn vướng điều khoản phạt chậm SLA
- QLVB: test luồng trình ký văn bản đi, lỗi ko hiện chữ ký số trên bản PDF -> báo IT
""",
    "2026-10-20": """- làm số liệu bc Q3, xong phần chi phí, còn phần doanh thu chờ P.KD gửi
- hỗ trợ c Lan (HCNS) gộp file chấm công T10 -> xong
- họp online với NCC Minh An 30p, họ đồng ý giảm phạt SLA còn 0.5%/ngày
""",
    "2026-10-21": """- P.KD gửi số liệu muộn 1 ngày, đã nhắc
- QLVB: IT fix xong lỗi chữ ký số, test lại OK 12/12 case
- viết tờ trình mua 15 màn hình cho P.KT, tổng dự toán 49,35tr
""",
    "2026-10-22": """- hoàn thành bc Q3, gửi a Hùng duyệt
- a Hùng góp ý: thêm so sánh cùng kỳ 2025 -> đã bổ sung
- đào tạo QLVB cho 8 người P.HCNS, phản hồi tốt
""",
    "2026-10-23": """- bc Q3 đã được duyệt, gửi BGĐ
- tờ trình mua màn hình: chờ P.TC thẩm định giá
- tuần sau: chốt HĐ bảo trì, đào tạo QLVB cho P.KD
""",
    "2026-10-26": """- giao ban: a Hùng giao thêm việc chuẩn bị KH năm 2027 phần CNTT, hạn 13/11
- chốt HĐ bảo trì với NCC Minh An: giá 186tr/năm, phạt SLA 0.5%/ngày -> trình ký
- QLVB: phát hiện văn bản đến >20MB upload bị treo, báo IT
""",
    "2026-10-27": """- đào tạo QLVB cho P.KD (11 người), 2 người chưa có tk -> nhờ IT cấp
- P.TC trả lời: giá màn hình cao hơn khảo sát 6%, yêu cầu lấy thêm 1 báo giá
- bắt đầu khung KH 2027: thu thập nhu cầu các phòng qua form
""",
    "2026-10-28": """- xin thêm báo giá màn hình từ NCC Phương Nam -> rẻ hơn 4,2%
- QLVB: IT nâng giới hạn upload lên 50MB, đã test OK
- KH 2027: mới có 3/7 phòng gửi nhu cầu, đã nhắc lần 1
""",
    "2026-10-29": """- HĐ bảo trì đã ký, lưu bản scan vào QLVB
- họp với a Hùng về KH 2027: ưu tiên số 1 là thay 40 máy tính đời cũ (>6 năm)
- vướng: P.KT và P.KD chưa gửi nhu cầu KH 2027, có nguy cơ trễ hạn 13/11
""",
    "2026-10-30": """- cập nhật tờ trình màn hình theo báo giá mới: 47,28tr, gửi lại P.TC
- tổng hợp nhu cầu KH 2027: 5/7 phòng, dự kiến tổng 1,2 tỷ
- đề xuất: xin a Hùng nhắc trực tiếp P.KT, P.KD trong giao ban thứ 2
""",
}

CONG_VIEC = [
    ("Báo cáo Q3/2026", "a Hùng", "23/10/2026", "Hoàn thành", 100),
    ("Hợp đồng bảo trì hệ thống (NCC Minh An)", "a Hùng", "31/10/2026", "Hoàn thành", 100),
    ("Triển khai phần mềm QLVB", "IT + P.KH-TH", "30/11/2026", "Đang làm", 70),
    ("Tờ trình mua 15 màn hình cho P.KT", "P.TC", "06/11/2026", "Đang làm", 80),
    ("Kế hoạch CNTT năm 2027", "a Hùng", "13/11/2026", "Đang làm", 35),
    ("Đào tạo QLVB các phòng", "P.KH-TH", "20/11/2026", "Đang làm", 45),
]

MAU = """# BÁO CÁO CÔNG VIỆC TUẦN {so_tuan} ({tu_ngay} – {den_ngay})

**Người báo cáo:** {ho_ten} – {chuc_danh}
**Kính gửi:** {nguoi_nhan}

## 1. Kết quả nổi bật
(2–3 gạch đầu dòng, mỗi dòng có con số cụ thể)

## 2. Công việc đã hoàn thành
| STT | Công việc | Kết quả |
|---|---|---|

## 3. Công việc đang thực hiện
| STT | Công việc | Tiến độ | Hạn | Ghi chú |
|---|---|---|---|---|

## 4. Khó khăn, vướng mắc và đề xuất
(Mỗi vướng mắc đi kèm một đề xuất cụ thể, ai cần làm gì)

## 5. Kế hoạch tuần tới
"""

def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    (DEMO / "nhat-ky").mkdir(parents=True)
    (DEMO / "mau").mkdir()
    (DEMO / "bao-cao").mkdir()

    for ngay, nd in NHAT_KY.items():
        thu = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"][date.fromisoformat(ngay).weekday()]
        (DEMO / "nhat-ky" / f"{ngay}.md").write_text(f"# {thu} {ngay}\n{nd}", encoding="utf-8")

    wb = Workbook()
    ws = wb.active
    ws.title = "Cong-viec"
    ws.append(["Công việc", "Người giao / phối hợp", "Hạn", "Trạng thái", "% hoàn thành"])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E79")
    for r in CONG_VIEC:
        ws.append(list(r))
    for col, w in zip("ABCDE", (44, 22, 12, 13, 13)):
        ws.column_dimensions[col].width = w
    wb.save(DEMO / "cong-viec.xlsx")

    (DEMO / "mau" / "mau-bao-cao-tuan.md").write_text(MAU, encoding="utf-8")

    if "--giai-phap" in sys.argv:
        shutil.copy(GOC / "giai-phap" / "CLAUDE.md", DEMO / "CLAUDE.md")
        shutil.copytree(GOC / "giai-phap" / ".claude", DEMO / ".claude")
        print("Đã chép CLAUDE.md và skill bao-cao-tuan vào demo/")

    print(f"Đã tạo demo/: {len(NHAT_KY)} file nhật ký (tuần 43, 44/2026), cong-viec.xlsx, mau/mau-bao-cao-tuan.md")


if __name__ == "__main__":
    main()
