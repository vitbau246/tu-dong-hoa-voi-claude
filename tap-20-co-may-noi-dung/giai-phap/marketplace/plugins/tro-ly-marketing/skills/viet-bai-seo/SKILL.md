---
name: viet-bai-seo
description: Viết bài chuẩn SEO từ một content brief, đúng giọng văn và chỉ dùng sự thật thương hiệu trong CLAUDE.md, lưu vào bai-viet/ để hook chấm điểm tự động, sửa tới khi đạt ngưỡng. Dùng khi cần viết bài blog/hướng dẫn chuẩn SEO.
argument-hint: "<file brief>"
allowed-tools: Read Write Edit Bash(python *) PowerShell(python *)
---

# Viết bài chuẩn SEO

Brief: **$ARGUMENTS**

1. Đọc brief, `CLAUDE.md` (giọng văn, **sự thật duy nhất được phép nêu**, điều cấm) và `san-pham.csv` (liên kết nội bộ).
2. Chọn 1 tiêu đề, 1 mô tả trong brief (được chỉnh cho đúng độ dài). Slug không dấu chứa từ khóa chính.
3. Viết theo đúng dàn ý brief, ưu tiên các mục ★ (khoảng trống so với đối thủ):
   - Mở bài nhắc từ khóa chính trong 2 câu đầu, nói ngay bài giúp người đọc điều gì.
   - Mỗi mục có ví dụ hoặc con số cụ thể. Con số về An Phát chỉ lấy từ `CLAUDE.md`.
   - Có ít nhất 1 bảng so sánh, ít nhất 2 ảnh (giữ chỗ, alt mô tả cụ thể), 3–5 liên kết nội bộ đặt tự nhiên.
   - FAQ đưa vào frontmatter `faq:` (sẽ thành schema FAQPage khi đăng) và lặp lại ở mục H2 "Câu hỏi thường gặp".
   - Không nhồi từ khóa: dùng biến thể và từ khóa phụ.
4. Lưu `bai-viet/<slug>.md`. Hook của plugin sẽ tự chấm điểm (chấm tay: `python "${CLAUDE_SKILL_DIR}/scripts/cham-diem-seo.py" <file>`). Nếu nhận được danh sách ✗, sửa đúng các mục đó (không độn chữ) rồi lưu lại, lặp tới khi ≥ 90.
5. Tự rà soát lần cuối với `CLAUDE.md`: không khẳng định công dụng y tế, không có chính sách hay số liệu ngoài danh sách sự thật.
6. Bàn giao: đường dẫn bài · điểm SEO cuối · số từ · danh sách ảnh thật cần chụp.
