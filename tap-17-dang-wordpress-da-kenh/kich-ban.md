# Tập 17: Một lệnh đưa bài lên WordPress (đủ chuẩn SEO) + nội dung cho 4 kênh

| | |
|---|---|
| **Mục tiêu người xem** | Đăng bài lên WordPress qua REST API (ảnh bìa, chuyên mục, thẻ, meta SEO Yoast, schema FAQ), **luôn ở dạng bản nháp**; chuyển 1 bài thành Facebook / LinkedIn / Email / Zalo OA có UTM |
| **Tính năng dạy** | Claude viết công cụ gọi API web, Application Password (không dùng mật khẩu thật), mu-plugin mở meta SEO cho REST API, skill `/da-kenh`, nguyên tắc "AI soạn – người bấm Xuất bản" |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/` (bài 100/100 từ tập 16, CLAUDE.md, `wp-gia-lap.py`). `--giai-phap` chép `dang-wordpress.py`, `seo-meta-rest.php`, skill `da-kenh` |
| **Đã kiểm thử** | Với **WordPress giả lập** (`wp-gia-lap.py`, cùng endpoint và JSON như WordPress thật): tạo bản nháp có ảnh bìa 1200×630 (tiếng Việt chuẩn), chuyên mục + thẻ tự tạo, meta Yoast, bảng, 7 H2, schema FAQPage, 2 ô "ẢNH CẦN CHỤP", không lặp H1; sai mật khẩu báo lỗi rõ ràng trước khi tải gì lên. **Chưa thử trên WordPress thật**: tập dượt một lần trên site thử nghiệm trước khi quay |

## Chuẩn bị

1. **Site WordPress thử nghiệm** (KHÔNG dùng site thật khi quay lần đầu): staging của hosting, hoặc cài **LocalWP** (miễn phí) trên máy.
2. Tạo **Application Password**: WordPress → Người dùng → Hồ sơ → *Application Passwords* → đặt tên "Claude" → copy chuỗi 24 ký tự. WordPress yêu cầu HTTPS cho tính năng này (LocalWP/môi trường `local` thì không cần).
3. Tài khoản cần quyền **Quản trị viên** để chèn schema FAQ (quyền `unfiltered_html`). Biên tập viên vẫn đăng được, nhưng khối schema có thể bị lọc.
4. Muốn ghi meta Yoast qua API: chép `seo-meta-rest.php` vào `wp-content/mu-plugins/` của site thử nghiệm.
5. Không có WordPress: `python wp-gia-lap.py` rồi dùng `WP_URL=http://localhost:8080`, `WP_USER=bientap`, `WP_APP_PASSWORD="demo demo demo demo"`. Xem bài tại http://localhost:8080.
6. `pip install markdown pyyaml pillow requests`.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Terminal: `python dang-wordpress.py bai-viet/ghe-cong-thai-hoc-cach-chon.md` → "✅ Đã tạo BẢN NHÁP #… · ⚠️ Còn 2 ảnh cần chụp" → cắt sang WordPress admin: bài nháp có ảnh bìa, chuyên mục, thẻ, khung Yoast đã điền | Một lệnh. Bài viết lên WordPress với ảnh bìa, chuyên mục, thẻ, tiêu đề và mô tả SEO đã điền sẵn. |
| 0:08 | Thư mục `da-kenh/`: 5 file Facebook, LinkedIn, email, Zalo, lịch đăng | Kèm nội dung cho bốn kênh, mỗi kênh một góc nhìn riêng. |
| 0:13 | Người dẫn | Viết xong bài chuẩn SEO mới được một nửa. Nửa còn lại là copy sang WordPress, chọn ảnh, điền Yoast, rồi viết lại cho Facebook, email… mất thêm một tiếng. Hôm nay mình biến cả nửa đó thành hai lệnh, với một nguyên tắc: **AI soạn, người bấm Xuất bản**. |
| 0:30 | Thanh 3 bước: `① Kết nối an toàn ② Đăng bản nháp ③ Một bài, bốn kênh` | |
| **0:33** | **① KẾT NỐI AN TOÀN** — WordPress → Hồ sơ → Application Passwords → tạo "Claude" → chuỗi 24 ký tự (làm mờ) | Bước một: **không** đưa mật khẩu đăng nhập cho AI. WordPress có "mật khẩu ứng dụng": một chuỗi riêng, chỉ dùng cho API, thu hồi được bất cứ lúc nào mà không ảnh hưởng tài khoản chính. |
| 0:50 | Terminal: `$env:WP_URL=…; $env:WP_USER=…; $env:WP_APP_PASSWORD=…` · `TEXT: Lưu trong biến môi trường, KHÔNG viết vào code, KHÔNG dán vào chat` | Và mật khẩu ứng dụng đặt trong biến môi trường. Không viết vào code, không dán vào khung chat. |
| 1:00 | Dán PROMPT 1 → Claude viết `dang-wordpress.py` `[TUA x8]`. Zoom `"status": "draft"`, `kiem_tra_dang_nhap`, `--thu` | Mình nhờ Claude viết công cụ đăng bài. Ba chi tiết an toàn: trạng thái luôn là **bản nháp**; kiểm tra đăng nhập trước khi tải gì lên; và chế độ "chạy thử" để xem trước dữ liệu sẽ gửi. |
| **1:20** | **② ĐĂNG BẢN NHÁP** — Chạy `--thu` → in tiêu đề, slug, chuyên mục, 5 FAQ, 2 ảnh cần chụp, meta SEO | Chạy thử trước. Nó in ra mọi thứ sẽ gửi, chưa đăng gì. Ổn. |
| 1:35 | Chạy thật → "✅ Đã tạo BẢN NHÁP" → mở link wp-admin | Chạy thật. Bản nháp đã nằm trên WordPress. |
| 1:45 | WordPress editor: ảnh đại diện = ảnh bìa xanh có tiêu đề · Chuyên mục "Kinh nghiệm chọn mua" · Thẻ · khung Yoast: tiêu đề SEO + mô tả + từ khóa đã điền | Ảnh bìa tự tạo đúng kích thước chia sẻ Facebook. Chuyên mục và thẻ được tìm, chưa có thì tự tạo. Khung Yoast đã điền sẵn tiêu đề, mô tả, từ khóa từ bài viết. |
| 2:05 | Zoom khung viền cam "ẢNH CẦN CHỤP: Nhân viên An Phát hướng dẫn khách…" | Và đây là lý do phải là bản nháp: hai chỗ cần ảnh thật được đánh dấu màu cam. Biên tập viên chụp ảnh, thay vào, đọc lại một lượt, rồi **người** bấm Xuất bản. |
| 2:20 | Công cụ Google Rich Results Test (cảnh dựng) với schema FAQPage hợp lệ | Ngoài ra, phần câu hỏi thường gặp được gắn dữ liệu có cấu trúc FAQPage, giúp Google hiểu nội dung rõ hơn. |
| 2:32 | `TEXT: Yoast không cho ghi qua API mặc định → mu-plugin 15 dòng` · mở `seo-meta-rest.php` | Một chi tiết kỹ thuật dân làm WordPress hay vấp: Yoast mặc định không cho ghi mô tả SEO qua API. Claude viết sẵn một plugin mười lăm dòng để mở đúng ba trường đó, chỉ cho người có quyền sửa bài. |
| **2:48** | **③ MỘT BÀI, BỐN KÊNH** — Gõ `/da-kenh bai-viet/ghe-cong-thai-hoc-cach-chon.md` `[TUA x6]` | Bước ba. Gọi lệnh đa-kênh với bài vừa đăng. |
| 3:00 | Lần lượt: `facebook.md` (2 phương án câu mở đầu A/B) · `linkedin.md` (mở bằng kinh nghiệm thực tế) · `email.md` (3 tiêu đề + preheader) · `zalo-oa.md` (60 chữ) | Facebook: câu mở đầu đánh vào nỗi đau, kèm hai phương án để chạy thử. LinkedIn: giọng chuyên gia, mở bằng kinh nghiệm thực tế. Email: ba phương án tiêu đề. Zalo: sáu mươi chữ, thân mật. Mỗi kênh một góc, không cắt dán. |
| 3:22 | Zoom liên kết: `?utm_source=facebook&utm_medium=social&utm_campaign=ghe-cong-thai-hoc-cach-chon` | Mọi liên kết đều gắn mã UTM. Một tuần sau, mở Google Analytics là biết kênh nào thực sự mang khách về. |
| 3:35 | Highlight trong `facebook.md`: "hỗ trợ tư thế ngồi đúng" (không phải "chữa đau lưng") | Và bộ sự thật ở tập trước vẫn có hiệu lực: bài Facebook viết "hỗ trợ tư thế ngồi đúng", không viết "chữa đau lưng". |
| **3:48** | **MẸO PRO** — Sơ đồ: `Việc đảo ngược được (nháp, file) → AI làm` · `Xuất bản / đăng mạng xã hội / gửi email → NGƯỜI bấm` | Nhắc lại nguyên tắc từ tập bốn, giờ quan trọng hơn bao giờ hết: đăng bài là việc **công khai**, có thể bị người khác chụp lại trước khi bạn kịp gỡ. AI soạn đến bản nháp. Con người bấm Xuất bản. |
| 4:08 | `TEXT: Không WordPress? Cùng công thức cho Haravan, Shopify, Ghost, Strapi… (đều có API)` | Không dùng WordPress? Haravan, Shopify, Ghost hay hầu hết hệ thống quản trị nội dung đều có API. Cùng một công thức, chỉ đổi địa chỉ API. |
| 4:20 | Tóm tắt: `Mật khẩu ứng dụng + biến môi trường` · `Luôn là bản nháp` · `Một bài → 4 kênh có UTM` | |
| 4:30 | `TEXT: BÀI TẬP: tạo Application Password trên site thử nghiệm, đăng 1 bài nháp` | Bài tập: tạo mật khẩu ứng dụng trên site thử nghiệm và đăng một bài nháp bằng công cụ hôm nay. |
| 4:38 | Teaser: báo cáo audit "robots.txt đang chặn /san-pham/" khung đỏ | Bài mới thì đẹp rồi. Nhưng nếu cả website đang mắc một lỗi kỹ thuật khiến Google **không đọc được** trang sản phẩm thì sao? Tập sau: khám SEO kỹ thuật toàn website, và để Claude tự sửa. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1**
```text
Viết dang-wordpress.py đăng bài Markdown (frontmatter như tập 16) lên WordPress REST API:
- Thông tin đăng nhập từ biến môi trường WP_URL, WP_USER, WP_APP_PASSWORD (Application Password). Gọi /wp/v2/users/me kiểm tra trước.
- Markdown → HTML (bảng); bỏ H1 khỏi nội dung (H1 = tiêu đề bài); ảnh chưa có file → khối viền cam "ẢNH CẦN CHỤP: <alt>".
- Tạo ảnh bìa 1200×630 bằng Pillow (font Arial có tiếng Việt), tải lên /wp/v2/media kèm alt_text, đặt làm featured_media.
- Tìm hoặc tạo chuyên mục/thẻ. Thêm schema FAQPage JSON-LD từ faq. excerpt = meta_description.
- meta: _yoast_wpseo_title, _yoast_wpseo_metadesc, _yoast_wpseo_focuskw. status LUÔN là "draft".
- Địa chỉ localhost không đi qua proxy. Tham số --thu để chỉ in dữ liệu, --chuyen-muc, --the.
```

**PROMPT 2** `/da-kenh bai-viet/ghe-cong-thai-hoc-cach-chon.md`

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| `401 rest_not_logged_in` dù mật khẩu đúng | Dùng mật khẩu **ứng dụng**, không phải mật khẩu đăng nhập. Một số hosting chặn header Authorization: thêm vào `.htaccess` dòng `SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1` |
| Khung Yoast trống | Chưa cài `seo-meta-rest.php` vào `mu-plugins`. Dùng RankMath thì đổi tên meta (xem chú thích trong file) |
| Schema FAQ biến mất khỏi nội dung | Tài khoản thiếu quyền `unfiltered_html`. Dùng tài khoản Quản trị viên, hoặc dùng khối FAQ của Yoast/RankMath |
| Máy công ty có proxy | Script đã cho địa chỉ localhost đi thẳng. Site staging nội bộ thì thêm tên miền vào biến `NO_PROXY` |

## Gói đăng tải

- **Tiêu đề:** A: `Đăng bài WordPress chuẩn SEO bằng 1 lệnh + nội dung 4 kênh | Claude nâng cao #17` · B: `AI soạn, người bấm Xuất bản: tự động hóa WordPress an toàn`
- **Thumbnail:** WordPress admin + 4 icon kênh. Chữ: **"1 LỆNH → 5 KÊNH"**.
- **Shorts:** (1) 0:33–1:00 "Đừng bao giờ đưa mật khẩu WordPress cho AI", (2) 3:22–3:48 "UTM: biết kênh nào ra tiền".
