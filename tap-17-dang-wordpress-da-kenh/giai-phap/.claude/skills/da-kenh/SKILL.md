---
name: da-kenh
description: Chuyển một bài viết blog thành nội dung cho nhiều kênh - Facebook, LinkedIn, email bản tin, Zalo OA - đúng giọng thương hiệu, có liên kết gắn UTM để đo lường. Dùng sau khi có bài viết, khi cần đăng tải hoặc quảng bá bài lên mạng xã hội và email.
argument-hint: "<file bài viết .md> [đường dẫn bài sau khi đăng]"
allowed-tools: Read Write
---

# Một bài, bốn kênh

Đầu vào: **$ARGUMENTS**. Đọc bài viết, `CLAUDE.md` (giọng văn, sự thật, điều cấm).

## Quy tắc chung
- Mỗi kênh **một góc nhìn** khác, không cắt dán cùng một đoạn.
- Chỉ dùng thông tin có trong bài và trong `CLAUDE.md`. Không thêm khuyến mãi, giá hay cam kết mới.
- Liên kết về bài gắn UTM: `?utm_source=<kênh>&utm_medium=<social|email>&utm_campaign=<slug-bai>`. Chưa có đường dẫn thật thì dùng `https://vpp-anphat.example/<slug>`.

## Kết quả: `da-kenh/<slug>/`
1. `facebook.md`: câu mở đầu "chạm nỗi đau" ≤ 15 chữ, 60–120 chữ, 3–5 gạch đầu dòng giá trị, 1 lời kêu gọi, 3 hashtag. Kèm **2 phương án** câu mở đầu để chạy thử A/B.
2. `linkedin.md`: giọng chuyên gia, 150–220 chữ, mở bằng một nhận định/kinh nghiệm thực tế (không mở bằng câu hỏi), kết bằng câu hỏi mời thảo luận.
3. `email.md`: 3 phương án tiêu đề (≤ 50 ký tự), 1 câu preheader (≤ 90 ký tự), thân thư 100–150 chữ, 1 nút CTA.
4. `zalo-oa.md`: ≤ 60 chữ, thân mật, 1 liên kết.
5. `lich-dang.md`: bảng đề xuất giờ đăng cho từng kênh trong tuần tới + ghi chú lý do (dựa trên thói quen chung của người dùng văn phòng, ghi rõ đây là gợi ý cần kiểm chứng bằng số liệu của trang).

## Tự kiểm tra
Đếm chữ từng file cho đúng giới hạn, rà soát lại với điều cấm trong `CLAUDE.md` (nhất là khẳng định công dụng y tế). Bàn giao: danh sách 5 file + câu mở đầu Facebook bạn khuyên dùng.
