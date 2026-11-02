---
name: don-thu-muc
description: Dọn dẹp thư mục lộn xộn an toàn - xếp file theo loại và năm, tìm file trùng NỘI DUNG bằng hash, không xóa gì, có nhật ký và script hoàn tác. Dùng khi người dùng muốn sắp xếp, dọn dẹp, phân loại file trong một thư mục.
argument-hint: "[thư mục cần dọn]"
disable-model-invocation: true
---

# Dọn thư mục theo công thức an toàn

Thư mục: **$ARGUMENTS** (trống: thư mục hiện tại).

## Nguyên tắc bất di bất dịch
- **Không xóa** bất kỳ file nào. Chỉ di chuyển.
- **Lập kế hoạch trước**, trình bày cho người dùng duyệt rồi mới thực hiện.
- Mọi thao tác ghi vào `nhat-ky-don-dep.csv` (ten_cu, duong_dan_moi, ly_do) và tạo `hoan-tac.ps1` đảo ngược toàn bộ.
  (Lưu ý: nút Rewind của Claude KHÔNG hoàn tác thao tác di chuyển bằng lệnh, nên file hoàn tác là bắt buộc.)

## Kế hoạch đề xuất
1. Thống kê: số file theo đuôi, theo năm sửa đổi (LastWriteTime), tổng dung lượng.
2. Thư mục đích theo loại: Tai-lieu (pdf, docx, doc, txt), Bang-tinh (xlsx, xls, csv), Trinh-chieu (pptx), Hinh-anh (png, jpg, jpeg, gif), Nen (zip, rar, 7z), Cai-dat (exe, msi), Media (mp4, mp3, m4a), Khac. Bên trong chia theo năm.
3. File trùng: so **hash nội dung** (không dựa vào tên). Giữ bản tên gọn nhất, chuyển bản thừa vào `_Trung-lap`. File tên kiểu "(1)" nhưng nội dung khác thì **không** phải trùng.
4. Sau khi thực hiện: đối chiếu tổng số file trước = sau, báo 5 nhóm trùng làm ví dụ.
