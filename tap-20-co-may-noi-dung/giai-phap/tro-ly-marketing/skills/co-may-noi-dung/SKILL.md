---
name: co-may-noi-dung
description: Cỗ máy nội dung hằng tuần - lấy chủ đề tiếp theo trong kế hoạch, lập brief SEO, viết bài (tự chấm điểm, tự sửa), đăng BẢN NHÁP lên WordPress, tạo nội dung 4 kênh, rồi lập phiếu chờ duyệt cho con người. Dùng khi chạy quy trình nội dung định kỳ hoặc khi người dùng muốn "làm bài tuần này".
argument-hint: "[chủ đề / từ khóa - bỏ trống = lấy dòng 'Chưa làm' đầu tiên trong ke-hoach-noi-dung.csv]"
allowed-tools: Read Write Edit Glob WebSearch WebFetch Skill Bash(python *) PowerShell(python *)
---

# Cỗ máy nội dung hằng tuần

Đầu vào: **$ARGUMENTS**. Bắt buộc có `CLAUDE.md` (giọng văn, sự thật, điều cấm) và `san-pham.csv` trong thư mục dự án. Thiếu thì DỪNG và báo.

## 1. Chọn chủ đề
Nếu không có tham số: đọc `ke-hoach-noi-dung.csv`, lấy dòng đầu tiên có `trang_thai = Chưa làm`. Ghi nhận `tu_khoa`, `loai_viec`.
Nếu `loai_viec` không phải "Viết mới" (ví dụ "Viết lại tiêu đề"): chỉ đề xuất 3 phương án tiêu đề + 2 mô tả vào phiếu duyệt, bỏ qua bước 2–5.

## 2. Brief
Làm theo skill `brief-seo` cho từ khóa đó, lưu `brief/<slug>.md`. Không có URL top từ người dùng thì ghi rõ nguồn đối thủ là công cụ tìm kiếm của Claude.

## 3. Viết bài
Làm theo skill `viet-bai-seo` với brief vừa tạo. Hook của plugin tự chấm điểm, sửa tới ≥ 90.
Kiểm tra lại: không có số liệu nào ngoài brief và `CLAUDE.md`. Không có khẳng định nằm trong "Điều cấm".

## 4. Đăng bản nháp
- Có biến môi trường `WP_URL`: chạy `python "${CLAUDE_SKILL_DIR}/scripts/dang-wordpress.py" bai-viet/<slug>.md --chuyen-muc "Kinh nghiệm chọn mua" --the "<từ khóa>"`.
- Không có: chạy với `--thu` và ghi "Chưa đăng: thiếu cấu hình WordPress" vào phiếu duyệt.
- TUYỆT ĐỐI không đổi trạng thái sang xuất bản.

## 5. Đa kênh
Làm theo skill `da-kenh` cho bài vừa viết.

## 6. Phiếu chờ duyệt `cho-duyet/<yyyy-mm-dd>-<slug>.md`
- Tóm tắt 3 dòng: chủ đề, điểm SEO, số từ.
- Link bản nháp WordPress (hoặc lý do chưa đăng).
- ☐ Danh sách việc NGƯỜI phải làm: ảnh thật cần chụp, câu/chỗ cần xác nhận, chọn câu mở đầu Facebook A/B, bấm Xuất bản.
- Những điểm Claude không chắc chắn (nếu có).

## 7. Cập nhật kế hoạch
Đổi `trang_thai` của dòng đã làm thành `Chờ duyệt` và ghi ngày. Không sửa các dòng khác.

## Bàn giao
4 dòng: đường dẫn phiếu duyệt · điểm SEO · trạng thái WordPress · việc người cần làm đầu tiên.
