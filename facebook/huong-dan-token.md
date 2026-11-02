# Lấy Page access token cho trang "5 phút tự động hóa"

> Làm **một lần**, khoảng 15 phút. Người làm phải là **quản trị viên** (hoặc có quyền tạo nội dung) của trang trên profile FoxFlow.
> **Tuyệt đối không** dán token vào khung chat với AI, email hay tin nhắn. Token chỉ nằm trong file `.env` trên máy bạn.

## 1. Tạo ứng dụng Meta (miễn phí)
1. Vào https://developers.facebook.com → **My Apps** → **Create App**, đăng nhập bằng tài khoản FoxFlow.
2. Chọn trường hợp sử dụng liên quan đến **quản lý Trang** (tên mục có thể thay đổi theo giao diện Meta, ví dụ "Manage everything on your Page").
3. Đặt tên app, ví dụ `FoxFlow Lich Dang`. App ở chế độ **Development** là đủ, vì chỉ quản trị viên app dùng, không cần Meta duyệt app.

## 2. Lấy token có đúng quyền
1. Mở **Graph API Explorer** (Tools → Graph API Explorer), chọn app vừa tạo.
2. **User or Page** → chọn **Get Page Access Token** → chọn trang **5 phút tự động hóa**.
3. Tích các quyền: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `pages_manage_engagement` (để đăng bình luận ghim), `publish_video`.
4. Bấm **Generate Access Token**, đồng ý cấp quyền cho đúng trang.
5. Token này **chỉ sống khoảng 1–2 giờ**. Đổi sang token dài hạn:
   - Mở **Access Token Debugger** (Tools → Access Token Tool / Debugger) → dán token → **Extend Access Token** để có User token dài hạn.
   - Quay lại Graph API Explorer, dùng User token dài hạn gọi `GET /me/accounts`. Trong kết quả, `access_token` của trang "5 phút tự động hóa" là **Page token không hết hạn** (cho tới khi bạn đổi mật khẩu, gỡ quyền app, hoặc mất quyền quản trị trang). Ghi lại cả `id` của trang.

## 3. Lưu vào `.env` (cùng thư mục với dang-facebook.py)
```
FB_PAGE_ID=<id của trang>
FB_PAGE_TOKEN=<page access token dài hạn>
```
File `.env` đã nằm trong `.gitignore`. Kiểm tra:
```powershell
python dang-facebook.py --kiem-tra
# → Token hợp lệ · Trang: "5 phút tự động hóa" · ✅ ĐÚNG trang
```

## 4. Bảo mật
- Token có quyền **đăng bài lên trang**. Ai có nó là đăng được. Lộ token thì vào cài đặt app → **Reset App Secret**, hoặc gỡ quyền app trong Cài đặt Facebook → Doanh nghiệp tích hợp.
- Không chia sẻ thư mục `facebook/` kèm `.env`. Muốn chia sẻ thì xóa `.env` trước.

## Xử lý lỗi thường gặp
| Lỗi | Nguyên nhân / cách xử lý |
|---|---|
| `Invalid OAuth access token` | Token sai hoặc hết hạn (token ngắn hạn 1–2 giờ). Làm lại mục 2.5 để lấy token dài hạn |
| `(#200) ... permission` | Thiếu quyền ở mục 2.3, hoặc tài khoản không có quyền tạo nội dung trên trang |
| `❌ SAI trang` khi `--kiem-tra` | Token đang là của trang khác. Lấy lại `access_token` đúng dòng "5 phút tự động hóa" trong `/me/accounts` |
| Video tải lên lỗi / quá lâu | Video quá nặng. Xuất lại MP4 H.264, 1080p, ≤ 1 GB. Reels: 9:16, 3–90 giây |
| Bài hẹn giờ không thấy trên trang | Bình thường: bài hẹn giờ chỉ thấy trong **Meta Business Suite → Lịch / Nội dung đã lên lịch** |
