---
name: bao-cao-tuan
description: Lập báo cáo công việc tuần theo mẫu của phòng từ nhật ký hằng ngày và bảng theo dõi công việc, xuất ra Markdown và Word. Dùng khi người dùng muốn làm, viết hoặc cập nhật báo cáo tuần.
argument-hint: "[số tuần ISO, bỏ trống = tuần hiện tại]"
allowed-tools: Read Glob Write Bash(python *) PowerShell(python *)
---

# Lập báo cáo tuần

Tuần cần báo cáo: **$ARGUMENTS** (nếu trống: tuần ISO hiện tại theo ngày hôm nay).

## Các bước

1. **Xác định khoảng ngày**: từ Thứ 2 đến Thứ 6 của tuần ISO đó, năm hiện tại.
2. **Đọc dữ liệu**:
   - Mọi file `nhat-ky/YYYY-MM-DD.md` nằm trong khoảng ngày trên. Nếu thiếu ngày nào, ghi chú ở cuối báo cáo.
   - `cong-viec.xlsx` để lấy hạn, trạng thái, % hoàn thành.
3. **Viết báo cáo** đúng cấu trúc của `mau/mau-bao-cao-tuan.md`:
   - Viết đầy đủ mọi chữ viết tắt theo bảng trong `CLAUDE.md`.
   - *Kết quả nổi bật*: 2–3 ý, ưu tiên ý có con số (tiền, số người, %, số case).
   - *Đã hoàn thành*: chỉ những việc nhật ký ghi rõ là xong / đã duyệt / đã ký.
   - *Đang thực hiện*: lấy % và hạn từ `cong-viec.xlsx`. Việc nào có hạn trong 14 ngày tới thì in đậm hạn.
   - *Vướng mắc*: mỗi vướng mắc kèm một đề xuất cụ thể.
   - *Kế hoạch tuần tới*: suy ra từ các ghi chú "tuần sau", việc dang dở và hạn sắp tới.
4. **Lưu file**: `bao-cao/bao-cao-tuan-<so_tuan>-<nam>.md`, rồi chuyển sang Word:
   `python "${CLAUDE_SKILL_DIR}/scripts/md_sang_docx.py" bao-cao/bao-cao-tuan-<so_tuan>-<nam>.md`
5. **Tự kiểm tra trước khi báo xong**:
   - Mọi con số trong báo cáo đều có trong nhật ký hoặc bảng công việc (không bịa).
   - Không còn chữ viết tắt nào trong bảng viết tắt.
   - Trả lời người dùng bằng 3 dòng: đường dẫn file Word, 1 câu tóm tắt tuần, và các mục "(cần bổ sung)" nếu có.
