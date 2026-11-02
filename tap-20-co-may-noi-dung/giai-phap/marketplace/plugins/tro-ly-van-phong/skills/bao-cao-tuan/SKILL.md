---
name: bao-cao-tuan
description: Lập báo cáo công việc tuần từ nhật ký hằng ngày (nhat-ky/YYYY-MM-DD.md) và bảng theo dõi công việc, theo mẫu của phòng nếu có, xuất Markdown và Word. Dùng khi người dùng muốn làm, viết hoặc cập nhật báo cáo tuần.
argument-hint: "[số tuần ISO, bỏ trống = tuần hiện tại]"
allowed-tools: Read Glob Write Bash(python *) PowerShell(python *)
---

# Lập báo cáo tuần

Tuần cần báo cáo: **$ARGUMENTS** (nếu trống: tuần ISO hiện tại).

1. Xác định Thứ 2 – Thứ 6 của tuần đó.
2. Đọc các file `nhat-ky/YYYY-MM-DD.md` trong khoảng ngày, và bảng công việc (`cong-viec.xlsx` hoặc `.csv`) nếu có.
   Không tìm thấy nhật ký: hỏi người dùng nhật ký nằm ở đâu, KHÔNG bịa nội dung.
3. Dùng mẫu báo cáo trong `mau/` nếu có. Nếu không có, dùng cấu trúc:
   *1. Kết quả nổi bật (có số liệu) · 2. Đã hoàn thành · 3. Đang thực hiện (tiến độ, hạn) · 4. Vướng mắc + đề xuất · 5. Kế hoạch tuần tới*.
4. Viết đầy đủ chữ viết tắt theo bảng trong `CLAUDE.md` (nếu có). Số tiền dạng 1.000.000 đồng, ngày dd/mm/yyyy.
5. Lưu `bao-cao/bao-cao-tuan-<tuan>-<nam>.md`, rồi chuyển sang Word:
   `python "${CLAUDE_SKILL_DIR}/scripts/md_sang_docx.py" bao-cao/bao-cao-tuan-<tuan>-<nam>.md`
6. Tự kiểm tra: mọi con số đều có trong nguồn, không còn chữ viết tắt. Trả lời 3 dòng: đường dẫn file Word, 1 câu tóm tắt tuần, các mục "(cần bổ sung)".
