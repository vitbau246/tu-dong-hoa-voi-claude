---
name: brief-seo
description: Lập bản định hướng nội dung (content brief) SEO cho một từ khóa - phân tích ý định tìm kiếm và 5 trang đang đứng top, tìm khoảng trống nội dung, đề xuất dàn ý, câu hỏi FAQ, tiêu đề và mô tả. Dùng khi chuẩn bị viết bài chuẩn SEO hoặc tối ưu lại một trang.
argument-hint: "<từ khóa chính> [URL top 1..5 cách nhau bởi dấu cách]"
allowed-tools: WebSearch WebFetch Read Write
---

# Content brief SEO

Đầu vào: **$ARGUMENTS**

## 0. Nguồn kết quả tìm kiếm
- Nếu người dùng đã dán URL top (lấy từ Google ở chế độ ẩn danh): dùng **đúng các URL đó**. Đây là dữ liệu đáng tin nhất.
- Nếu không: dùng WebSearch để tìm 5 trang tiếng Việt liên quan nhất, và **ghi rõ** trong brief: "Danh sách đối thủ lấy từ công cụ tìm kiếm của Claude, có thể khác thứ hạng Google tại Việt Nam".
- Đọc thêm `website.md` / `CLAUDE.md` nếu có để biết website, sản phẩm, khách hàng mục tiêu.

## 1. Phân tích từng trang top (WebFetch, yêu cầu trích nguyên văn các tiêu đề H1/H2/H3)
Bảng: URL | loại trang (sản phẩm / danh mục / bài hướng dẫn / so sánh) | số từ ước tính | các H2 | điểm mạnh | điểm thiếu.

## 2. Ý định tìm kiếm
Kết luận 1 trong: Tìm hiểu (informational) / Cân nhắc (commercial) / Mua (transactional) / Điều hướng. Dựa vào **loại trang** đang chiếm top, không đoán theo cảm tính. Nếu top lẫn lộn thì nói rõ tỉ lệ.

## 3. Khoảng trống nội dung
Những câu hỏi / thông tin người tìm cần mà **≤ 1** trang top trả lời tốt (đây là cơ hội vượt mặt).

## 4. Brief (lưu `brief/<slug-tu-khoa>.md`)
- Từ khóa chính, 5–10 từ khóa phụ / biến thể (lấy từ chính nội dung các trang top và dữ liệu Search Console nếu có).
- Loại trang nên làm + độ dài khuyến nghị (theo trung vị các trang top, không tự đặt).
- 3 phương án **tiêu đề SEO** (≤ 60 ký tự, có từ khóa chính ở đầu) và 2 phương án **mô tả** (140–160 ký tự, có lời kêu gọi hành động).
- Dàn ý H2/H3 chi tiết, đánh dấu ★ các mục lấp khoảng trống.
- 5 câu hỏi FAQ.
- Liên kết nội bộ nên đặt (tới trang sản phẩm/danh mục của website).
- Yếu tố tin cậy (E-E-A-T) cần có: số liệu thực tế, ảnh thật, kinh nghiệm, chính sách bảo hành...

## 5. Bàn giao
3 dòng: đường dẫn brief · ý định tìm kiếm · 1 khoảng trống lớn nhất.
