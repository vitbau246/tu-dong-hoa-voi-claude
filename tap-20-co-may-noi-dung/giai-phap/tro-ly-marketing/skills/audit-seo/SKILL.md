---
name: audit-seo
description: Khám SEO kỹ thuật toàn website - crawl từ trang chủ, kiểm tra robots.txt, noindex, canonical, link gãy, trùng title, thiếu mô tả, H1, viewport, ảnh nặng/thiếu alt, sitemap, trang mồ côi; xếp theo mức độ nghiêm trọng. Dùng khi cần kiểm tra sức khỏe SEO của website hoặc sau mỗi lần cập nhật website.
argument-hint: "<URL website> [thư mục mã nguồn để tìm trang mồ côi]"
allowed-tools: Read Write Bash(python *) PowerShell(python *)
---

# Audit SEO kỹ thuật

Đầu vào: **$ARGUMENTS**

1. Chạy: `python "${CLAUDE_SKILL_DIR}/scripts/kiem-tra-ky-thuat.py" <URL> [--thu-muc <thư mục>]`
   (WebFetch không mở được localhost/mạng nội bộ, nên luôn dùng script này.)
2. Đọc `bao-cao-audit.md`. Giải thích bằng ngôn ngữ dễ hiểu 3 lỗi nghiêm trọng nhất: vì sao nguy hiểm, ảnh hưởng gì tới doanh thu.
3. Đề xuất kế hoạch sửa theo thứ tự NGHIÊM TRỌNG → CAO → TRUNG BÌNH → THẤP. Việc nào cần người quyết (chuyển hướng đi đâu, nội dung tiêu đề) thì liệt kê để hỏi.
4. Chỉ sửa khi người dùng đồng ý và khi có mã nguồn trong thư mục dự án. KHÔNG sửa trực tiếp website đang chạy thật.
5. Sửa xong chạy lại script và báo điểm trước/sau.
