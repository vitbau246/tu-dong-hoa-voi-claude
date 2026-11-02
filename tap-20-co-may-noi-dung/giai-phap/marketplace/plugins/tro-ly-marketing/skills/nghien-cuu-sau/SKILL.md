---
name: nghien-cuu-sau
description: Nghiên cứu chuyên sâu một đề tài lớn bằng một ĐỘI - chia đề tài thành nhiều góc, giao cho các subagent nha-nghien-cuu chạy song song, cho kiem-chung-vien kiểm chứng mọi trích dẫn, rồi tổng hợp thành báo cáo chiến lược có ma trận độ tin cậy. Dùng cho câu hỏi chiến lược, phân tích thị trường, đánh giá cơ hội kinh doanh cần nhiều nguồn.
argument-hint: "<đề tài hoặc đường dẫn file đề bài>"
disable-model-invocation: true
---

# Nghiên cứu chuyên sâu bằng đội

Đề tài: **$ARGUMENTS**
Thư mục kết quả: `nghien-cuu/<slug-de-tai>/`

## Bước 1. Chia góc (trình bày cho người dùng, chờ đồng ý)
- Chia đề tài thành **3–5 góc độc lập**, mỗi góc một mã 2 chữ cái (ví dụ TT = thị trường, DT = đối thủ, KH = khách hàng, CS = chính sách & chi phí).
- Mỗi góc: 1 câu mô tả phạm vi + điều KHÔNG thuộc phạm vi (để các góc không chồng lấn).

## Bước 2. Nghiên cứu song song
- Gọi **đồng thời** một subagent `nha-nghien-cuu` (trong plugin: `tro-ly-marketing:nha-nghien-cuu`) cho mỗi góc (trong CÙNG một lượt, để chạy song song). Mỗi agent nhận: đề tài gốc, phạm vi góc, mã góc, thư mục kết quả.
- Chờ tất cả xong. Ghi lại thời gian bắt đầu/kết thúc.

## Bước 3. Kiểm chứng
- Gọi subagent `kiem-chung-vien` (trong plugin: `tro-ly-marketing:kiem-chung-vien`), đưa đường dẫn script: `${CLAUDE_SKILL_DIR}/scripts/kiem-chung-trich-dan.py` và thư mục kết quả.
- Không chuyển sang bước 4 khi còn trích dẫn `KHÔNG THẤY`.

## Bước 4. Tổng hợp `bao-cao-chien-luoc.md` (tối đa 2 trang)
1. **Trả lời ngắn** câu hỏi gốc (3 câu).
2. **Phát hiện chính** theo từng góc, giữ nguyên mã nguồn `[TT3]`.
3. **Ma trận độ tin cậy**: mỗi kết luận quan trọng | số nguồn ủng hộ | loại nguồn | mức tin cậy (Cao: ≥ 2 nguồn gốc độc lập / Trung bình / Thấp: 1 nguồn hoặc chưa kiểm chứng tự động).
4. **Điểm vênh giữa các nguồn**: gộp từ các góc, ghi đủ các con số khác nhau.
5. **Rủi ro và câu hỏi còn bỏ ngỏ** → đề xuất cách trả lời (khảo sát, hỏi chuyên gia, mua dữ liệu…).
6. **Phụ lục**: gộp mọi `nguon-*.csv` thành `nguon-tong-hop.csv`.

## Bước 5. Bàn giao
4 dòng: đường dẫn báo cáo · số góc / số nguồn / số trích dẫn (đã gỡ bao nhiêu) · thời gian chạy · câu trả lời ngắn nhất.
