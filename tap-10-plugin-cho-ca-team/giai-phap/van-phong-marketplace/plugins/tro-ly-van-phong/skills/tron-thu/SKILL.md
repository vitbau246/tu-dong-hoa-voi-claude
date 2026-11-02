---
name: tron-thu
description: Trộn thư (mail merge) từ danh sách Excel và mẫu Word có ô {{...}}, xuất Word + PDF cho từng người và tạo email nháp .eml có đính kèm. KHÔNG bao giờ tự gửi email. Dùng khi cần tạo thư mời, giấy xác nhận, thông báo hàng loạt cá nhân hóa.
argument-hint: "<file-danh-sach.xlsx> <file-mau.docx>"
disable-model-invocation: true
---

# Trộn thư an toàn

Đầu vào: $ARGUMENTS

## Bước 1. Soát danh sách (bắt buộc, chưa tạo file nào)
- Tìm: dòng trùng người, thiếu thông tin cho các ô `{{...}}` trong mẫu, email sai định dạng.
- Mọi điểm **mơ hồ** (ví dụ thiếu danh xưng, tên trung tính) thì **HỎI người dùng**. Không đoán giới tính, không đoán dữ liệu.
- Báo kết quả soát và chờ người dùng quyết định.

## Bước 2. Trộn thư
- Viết script Python (python-docx) thay các ô `{{...}}`, **giữ nguyên định dạng** của mẫu.
- Lưu `thu-moi/<STT> - <Họ tên>.docx`, rồi xuất PDF bằng Microsoft Word (COM). Không có Word thì giữ .docx.
- Người thiếu hoặc sai email: vẫn tạo thư, ghi vào `can-bo-sung.xlsx` kèm lý do.

## Bước 3. Email nháp
- Với mỗi người có email hợp lệ: tạo `email-nhap/<STT> - <Họ tên>.eml` có header `X-Unsent: 1` (Outlook mở dạng thư soạn mới), tiêu đề và lời chào cá nhân hóa, đính kèm PDF của người đó.
- **KHÔNG gửi email.** Gửi là việc không thể rút lại, nên con người phải bấm nút cuối.

## Kết thúc
Báo: số thư đã tạo, số email nháp, danh sách cần bổ sung, và 3 thư ngẫu nhiên để người dùng tự kiểm tra.
