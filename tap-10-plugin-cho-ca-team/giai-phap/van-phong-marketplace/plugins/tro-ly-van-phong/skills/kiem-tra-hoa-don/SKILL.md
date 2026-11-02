---
name: kiem-tra-hoa-don
description: Trích xuất hàng loạt hóa đơn PDF (nhiều bố cục) vào Excel bằng script, rồi kiểm tra chéo theo quy tắc kế toán (tiền hàng, thuế, tổng, hóa đơn trùng) và soát ngẫu nhiên. Dùng khi cần nhập liệu hoặc rà soát hóa đơn, chứng từ PDF.
argument-hint: "[thư mục chứa hóa đơn PDF]"
---

# Trích xuất và kiểm tra hóa đơn

Thư mục hóa đơn: **$ARGUMENTS** (trống: hỏi người dùng).

1. **Nhận diện bố cục**: mở thử vài file, liệt kê các kiểu bố cục và cách gọi các trường (ví dụ "Tổng cộng tiền thanh toán" / "TỔNG CỘNG" / "Phải thanh toán").
2. **Trích bằng script** (pdfplumber), KHÔNG đọc rồi gõ lại. Kết quả `hoa-don.xlsx`:
   - `Hoa-don`: Tên file | Nhà cung cấp | MST | Ký hiệu | Số HĐ | Ngày | Tiền hàng | Thuế suất | Tiền thuế | Tổng thanh toán
   - `Chi-tiet`: Số HĐ | Tên hàng | ĐVT | SL | Đơn giá | Thành tiền
3. **Kiểm tra chéo** (sheet `Can-kiem-tra`), mỗi vi phạm ghi rõ file, quy tắc, chênh lệch:
   1. Tiền hàng ≠ tổng các dòng hàng
   2. Tiền thuế ≠ Tiền hàng × Thuế suất (cho phép lệch làm tròn ≤ 1 đ)
   3. Tổng thanh toán ≠ Tiền hàng + Tiền thuế
   4. Trùng hóa đơn = trùng **cả** MST + Ký hiệu + Số HĐ (chỉ trùng số thì KHÔNG phải trùng)
4. **Soát ngẫu nhiên** 3 hóa đơn hợp lệ: bảng so sánh PDF gốc ↔ Excel theo từng trường.
5. File là **ảnh chụp/scan** (không có lớp chữ): đọc bằng hình ảnh, đánh dấu cột `Nguồn = Ảnh` và nhắc người dùng soát lại 100% các dòng này.
6. Báo cáo: số file, số hóa đơn duy nhất, tổng thanh toán, danh sách cần kiểm tra.
