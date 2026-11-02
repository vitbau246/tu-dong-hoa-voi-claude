# Kế hoạch xuất bản và đo lường

## 1. Lịch đăng (10 tuần + chiến dịch Shorts)

| Tuần | Video dài (5 phút), Thứ 3 lúc 20:00 | Shorts (Thứ 5 + Thứ 7, 12:00) | Ghi chú |
|---|---|---|---|
| 0 | **Trailer 60 giây**: dựng nhanh 10 cảnh "wow" | — | Đăng trước 1 tuần, ghim trên kênh |
| 1 | Tập 1: Dọn 300 file | Bẫy file giả bản sao · Rewind không cứu được bạn | Ghim bình luận: yêu cầu gói Pro |
| 2 | Tập 2: Gộp 12 file Excel | 4 cách viết Hà Nội · Sai 2,5 tỷ | Shorts "sai 2,5 tỷ" có tiềm năng lan truyền cao |
| 3 | Tập 3: 30 hóa đơn PDF | Lỗi che nhau còn 10 nghìn · Trùng số ≠ trùng HĐ | Chia sẻ vào các nhóm kế toán |
| 4 | Tập 4: Trộn thư | AI không đoán giới tính · Nguyên tắc bấm nút cuối | Chia sẻ vào các nhóm hành chính, nhân sự |
| 5 | Tập 5: Skills | AI không biết "a Hùng" là ai · Không cần nhớ tên lệnh | **Mốc chuyển chặng**: làm cộng đồng, hỏi người xem muốn skill gì |
| 6 | Tập 6: Hooks | Auto mà vẫn bị chặn · Hook không phải tường thành | |
| 7 | Tập 7: Trình duyệt | Trình duyệt tự điền form · AI không bịa số điện thoại | |
| 8 | Tập 8: Tự chạy 7:30 | Claude không cần cửa sổ · 3 cách hẹn giờ | |
| 9 | Tập 9: Subagents | Chữ nhỏ 200 triệu · Quy trình bốn mắt | |
| 10 | Tập 10: Plugin | 2 lệnh là có trợ lý · 10 tập trong 25 giây | Livestream hỏi đáp 30 phút sau tập cuối |

**Tổng phần 1:** 1 trailer + 10 video dài + 20 Shorts = 31 nội dung trong 11 tuần.

**Phần 2 (tuần 12–21):** lịch chi tiết ở `05-phan-2-nang-cao.md` mục 6. Tổng cả series: 2 trailer + 20 video dài + 40 Shorts + 2 livestream.

**Facebook (Fanpage "5 phút tự động hóa" · FoxFlow):** lịch riêng theo nghiên cứu giờ đăng tại `facebook/nghien-cuu-gio-dang.md`, 82 bài từ 13/11/2026 đến 17/04/2027 (bài mồi Thứ 2 07:45 · video Thứ 3 thử A/B 11:45/20:00 · Reel Thứ 5 12:15 + cuối tuần). Vận hành: `facebook/README.md`.

## 2. Playlist và điều hướng

- Playlist **"Tự động hóa mọi thứ với VS Code và Claude"**, đúng thứ tự 1 → 10.
- Màn hình kết: (trái) tập tiếp theo · (phải) playlist.
- Mỗi Short: dòng mô tả đầu "Xem bản đầy đủ 5 phút 👉", kèm liên kết video liên quan (Related video).
- Chương (chapters) trong mô tả theo đúng mốc 3 bước của kịch bản. Tên chương là **lợi ích**, ví dụ "1:50 Gộp & làm sạch", không đặt kiểu "Bước 2".

## 3. Tiêu đề, thumbnail, SEO

- **Công thức tiêu đề:** `[Kết quả cụ thể có con số] + [công cụ] | Tự động hóa với Claude #N`. Thử A/B bằng tính năng Test & Compare của YouTube cho tập 1–3, rồi chọn công thức thắng cho các tập sau.
- **Thumbnail:** tối đa 4 chữ to, 1 con số, nền tương phản. Bố cục trước/sau. Không đặt mặt người dẫn quá 30% diện tích.
- **Từ khóa chính:** claude code, claude code tiếng việt, tự động hóa văn phòng, AI cho dân văn phòng, VS Code AI, tự động hóa excel bằng AI, AI đọc hóa đơn, mail merge AI, MCP là gì, claude skills.
- **Mô tả:** 2 dòng đầu chứa lợi ích + từ khóa. Sau đó là chương, link tải file mẫu, yêu cầu hệ thống, phiên bản Claude Code (2.1.312), ghi chú "dữ liệu demo hư cấu".

## 4. File mẫu cho người xem

- Đóng gói `tap-xx/chuan-bi.py` + `kich-ban.md` (phần Prompt) + `giai-phap/` thành một repo công khai, ví dụ `tu-dong-hoa-voi-claude`. Mỗi tập một thư mục, người xem chạy `python chuan-bi.py` là có dữ liệu y hệt video.
- **Không** đưa `demo/` đã sinh sẵn lên repo (nặng, và dữ liệu luôn sinh lại được). Thêm `demo/` vào `.gitignore`.

## 5. KPI và cách đọc số liệu

| Chỉ số | Mục tiêu tham chiếu | Đọc thế nào |
|---|---|---|
| Giữ chân ở giây 30 | ≥ 70% | Thấp hơn thì hook hỏng. Đổi câu mở đầu/thumbnail ở tập sau |
| Thời lượng xem trung bình | ≥ 55% (khoảng 2:45/5:00) | Tìm điểm tụt sâu trên biểu đồ giữ chân. Thường do đoạn chờ Claude chạy chưa tua đủ nhanh |
| CTR thumbnail | ≥ 5% | Thấp hơn: thử thumbnail B sau 48 giờ |
| Tỉ lệ xem tiếp tập sau (playlist) | ≥ 25% | Thấp: teaser cuối chưa đủ hấp dẫn |
| Bình luận có prompt/câu hỏi | ≥ 2% số lượt xem | Đo mức độ người xem **làm theo**, chỉ số giá trị thật quan trọng nhất |
| Lượt tải file mẫu (repo) | Theo dõi hằng tuần | Tăng đều qua các tập là tín hiệu tốt nhất |

> Mục tiêu trên là điểm tham chiếu khởi đầu (nguồn bên thứ ba, xem `01-nghien-cuu.md`). Hãy điều chỉnh theo số liệu thật của kênh sau 3 tập đầu.

## 6. Tái sử dụng nội dung

- **Bài viết blog/Facebook** mỗi tập: 3 prompt + ảnh trước/sau + link video.
- **Carousel LinkedIn**: "7 lỗi dữ liệu Excel AI phát hiện" (tập 2), "4 quy tắc kiểm tra hóa đơn" (tập 3).
- **Bản nội bộ doanh nghiệp**: ghép 10 tập thành một khóa đào tạo 1 buổi (60 phút xem + 60 phút thực hành với `chuan-bi.py`).
