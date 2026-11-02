# Công thức một tập 5 phút và quy chuẩn series

## 1. Cấu trúc cố định (mọi tập đều theo khung này)

| Mốc | Phần | Mục tiêu | Quy tắc |
|---|---|---|---|
| 0:00–0:10 | **HOOK** | Giữ người xem không lướt đi | Cho thấy **kết quả cuối** hoặc con số trước/sau. Câu đầu tiên ≤ 12 chữ. Không chào hỏi |
| 0:10–0:35 | **NỖI ĐAU + LỜI HỨA** | "Đây là chuyện của tôi" | Mô tả việc lặp lại người xem đang làm tay. Hứa 1 kết quả và 1 "bí mật cuối video" (vòng lặp mở) |
| 0:35–3:45 | **DEMO 3 BƯỚC** | Giá trị thật | Đúng 3 bước, mỗi bước có tiêu đề trên màn hình. Mỗi bước kết thúc bằng một khoảnh khắc "wow" |
| 3:45–4:30 | **MẸO PRO / BẪY CẦN TRÁNH** | Chiều sâu, độ tin cậy | Một mẹo an toàn hoặc mở rộng. Trả lời vòng lặp mở |
| 4:30–5:00 | **CHỐT + BÀI TẬP + TEASER** | Hành động và xem tiếp | Tóm 3 ý bằng một câu. Giao một bài tập 5 phút. Hé lộ tập sau bằng một hình ảnh |

**Độ dài lời thoại:** 550–700 âm tiết, tương đương 3–3,6 phút nói (tiếng Việt đọc khoảng 180–200 âm tiết/phút). Khoảng 1,5 phút còn lại dành cho **khoảng lặng có chủ đích**: kết quả hiện ra, đoạn tua nhanh, người xem kịp đọc bảng Excel. 10 kịch bản hiện tại nằm trong khoảng 568–681 âm tiết.

## 2. Định dạng kịch bản (2 cột)

Mỗi kịch bản trong `tap-xx/kich-ban.md` dùng bảng:

| Thời gian | HÌNH (màn hình / chữ trên màn hình) | LỜI (đọc) |
|---|---|---|

- **HÌNH** ghi rõ: thao tác, đoạn tua nhanh (`[TUA x6]`), chữ nổi trên màn hình (`TEXT:`), phóng to (`ZOOM:`), hiệu ứng âm thanh (`SFX:`).
- **LỜI** viết để **nói**: câu ngắn, có nhịp, dùng "bạn" và "mình".
- Prompt cần gõ nằm trong khối riêng `PROMPT`. Người dẫn **dán** prompt (không gõ trực tiếp khi quay) rồi đọc lướt ý chính.

## 3. Giọng điệu và quy chuẩn ngôn ngữ

- **Xưng hô:** "mình" và "bạn". Thân thiện, thẳng vào việc, không màu mè.
- **Thuật ngữ:** lần đầu nhắc thì Việt hóa kèm tiếng Anh trong ngoặc, ví dụ "kỹ năng (Skill)", "móc sự kiện (Hook)". Từ lần sau giữ tên tiếng Anh cho khớp với giao diện.
- **Không phóng đại.** Nói "trong lần chạy này mất 40 giây" thay vì "chỉ 1 giây". Con số trong video phải khớp với đồng hồ thật trên màn hình.
- **Luôn có một câu an toàn**: làm trên bản sao, kiểm tra kết quả, dữ liệu nhạy cảm theo quy định công ty.
- **Câu chốt thương hiệu (cuối mỗi tập):** *"Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm."*

## 4. Ngân hàng hook (mẫu để tái sử dụng)

| Kiểu | Mẫu câu |
|---|---|
| Trước/Sau | "Bên trái: 3 tiếng làm tay. Bên phải: 40 giây. Cùng một kết quả." |
| Câu hỏi đâm trúng | "Thư mục Downloads của bạn đang có bao nhiêu file? Mình cá là hơn 500." |
| Lỗi ẩn | "Trong 30 hóa đơn này có 3 cái sai. Mắt người mất 2 tiếng. Claude mất 90 giây." |
| Thách thức | "Mình sẽ tạo 40 thư mời Word, tên ai người nấy, mà không gõ một chữ nào." |
| Hé lộ | "Sáng nay lúc 7 giờ 30, máy tính đã tự làm báo cáo cho mình khi mình còn ngủ." |

## 5. Danh sách tập (lộ trình 3 chặng)

**Chặng 1: Làm được ngay (người mới, chỉ cần biết gõ yêu cầu)**

| Tập | Tiêu đề làm việc | Việc thật được giải quyết | Tính năng dạy | Khoảnh khắc "wow" |
|---|---|---|---|---|
| 1 | Dọn 300 file lộn xộn trong 1 phút | Thư mục Downloads hỗn loạn | Cài đặt, chế độ Plan, file hoàn tác | Claude tìm ra 27 file trùng nội dung dù khác tên |
| 2 | Gộp 12 file Excel thành báo cáo có biểu đồ | Tổng hợp doanh thu năm | Gọi file bằng @, cho Claude tự viết và chạy script | 4 cách viết "Hà Nội" + dòng trùng được tự phát hiện |
| 3 | 30 hóa đơn PDF vào Excel trong 2 phút | Nhập liệu kế toán | Trích xuất có kiểm tra chéo | Bắt 2 hóa đơn cộng sai và 1 hóa đơn nhập trùng |
| 4 | Tạo 40 thư mời cá nhân hóa, không gõ một chữ | Trộn thư (mail merge) | Mẫu Word, xử lý hàng loạt, tạo thư nháp | Thư nháp Outlook kèm file đính kèm hiện ra sẵn |

**Chặng 2: Dạy Claude làm theo cách của bạn**

| Tập | Tiêu đề làm việc | Việc thật | Tính năng | "Wow" |
|---|---|---|---|---|
| 5 | Báo cáo tuần chỉ bằng MỘT lệnh | Báo cáo định kỳ | CLAUDE.md và Skills | Gõ `/bao-cao-tuan` là ra báo cáo đúng mẫu |
| 6 | Gắn phanh an toàn cho AI | Sợ AI xóa nhầm, sửa hỏng | Hooks (chặn, sao lưu, thông báo) | Claude định xóa thì bị chặn ngay trên màn hình |
| 7 | Cho Claude tự lái trình duyệt | Thu thập dữ liệu web, điền form | MCP Playwright | Trình duyệt tự điền 5 form, tự phát hiện số điện thoại sai |

**Chặng 3: Tự động hoàn toàn và nhân rộng**

| Tập | Tiêu đề làm việc | Việc thật | Tính năng | "Wow" |
|---|---|---|---|---|
| 8 | Máy tự làm bản tin lúc 7:30 sáng | Tổng hợp tin, việc trong ngày | `claude -p` + Task Scheduler | Bật máy lên là bản tin đã nằm sẵn |
| 9 | Đội 3 trợ lý AI làm song song | So sánh 3 báo giá nhà cung cấp | Subagents | Lộ ra phương án "rẻ nhất" thực chất đắt nhất sau 3 năm |
| 10 | Đóng gói thành "trợ lý văn phòng" cho cả team | Nhân rộng cách làm | Plugin + marketplace | Đồng nghiệp chạy 2 lệnh là có đủ mọi skill |

## 6. Bộ nhận diện trên màn hình

- **Thanh tiến trình 3 bước** ở cạnh trên: `① ... ② ... ③ ...`, sáng dần theo bước.
- **Đồng hồ thời gian thật** ở góc phải khi Claude chạy (để chứng minh con số).
- **Hộp "PROMPT"** nền tối, chữ lớn khi dán prompt (giữ trên màn hình ≥ 3 giây để người xem dừng hình chụp lại).
- **Thẻ "⚠️ An toàn"** màu cam cho các câu an toàn.
- **Màn hình kết:** "Tập sau: …" + nút đăng ký + đường dẫn tải file mẫu.
