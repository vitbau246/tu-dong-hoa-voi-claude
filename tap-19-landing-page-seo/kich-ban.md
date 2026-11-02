# Tập 19: Landing page chuẩn SEO, tải dưới 1 giây, lên Internet trong 15 phút

| | |
|---|---|
| **Mục tiêu người xem** | Từ một bản brief, để Claude dựng landing page **một file**, chuẩn SEO (dữ liệu có cấu trúc, Open Graph), tối ưu ảnh, đạt chuẩn truy cập, kiểm tra trên điện thoại, rồi đưa lên Internet |
| **Tính năng dạy** | Claude viết HTML/CSS, tối ưu ảnh hàng loạt (Pillow → WebP + srcset), JSON-LD (LocalBusiness, Product/Offer, FAQPage), kiểm tra bằng Playwright (chụp màn hình điện thoại) + Lighthouse trong Edge, triển khai bằng kéo thả (Netlify Drop) hoặc GitHub Pages |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/yeu-cau-landing.md` (brief đầy đủ), `CLAUDE.md` (bộ sự thật), `anh-goc/` (3 ảnh 4000px, mỗi ảnh khoảng 3 MB). `--giai-phap` chép `toi-uu-anh.py` + `landing/` tham chiếu |
| **Đã kiểm thử (bản tham chiếu)** | JSON-LD hợp lệ (LocalBusiness, 2 Product, FAQPage 4 câu) · title 44 / mô tả 150 ký tự · 1 H1 · 100% ảnh có alt + width/height · 100% ô form có label · tương phản màu ≥ 5:1 (WCAG AA) · không cuộn ngang ở 390px và 1366px · **Lưu ý:** ảnh demo là ảnh tổng hợp nên nén cực mạnh (9,3 MB → 28 KB). Ảnh chụp thật thường giảm khoảng 85–95%. Lời thoại không dùng số 99,7% |

## Chuẩn bị

1. `python chuan-bi.py`, mở `tap-19-landing-page-seo/demo`. **Nên thay 3 ảnh trong `anh-goc/` bằng ảnh chụp thật** (văn phòng, ghế, cảnh ngồi thử), để con số nén ảnh là thật.
2. Xem trang: `python -m http.server 8004 -d landing`.
3. Cảnh 2:38 ("chữ dính mép trái") là lỗi thật mình gặp khi làm bản mẫu. Khi quay, Claude có thể tìm ra lỗi **khác** hoặc không có lỗi. Hãy quay đúng lỗi nó tìm được và sửa lời thoại cho khớp, đừng dựng lại lỗi giả.
4. Triển khai: tài khoản Netlify (miễn phí) cho cách kéo thả, hoặc GitHub + repo public cho GitHub Pages. **Chỉ dùng tên miền / nội dung demo**: trang này có form, đừng để form demo nhận dữ liệu thật.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Điện thoại mở landing page, cuộn mượt; Edge DevTools → Lighthouse: 4 vòng tròn xanh | Một landing page cho khách hàng doanh nghiệp: chuẩn SEO, tải gần như tức thì trên điện thoại, điểm Lighthouse xanh. |
| 0:07 | `TEXT: Brief → Online: 15 phút` | Từ bản brief tới lúc có đường link chia sẻ: mười lăm phút. Không cần biết lập trình, không cần thuê thiết kế. |
| 0:14 | Người dẫn | Bốn tập vừa rồi mình làm SEO cho website có sẵn. Hôm nay làm mới hoàn toàn một trang đích cho chiến dịch: viết, tối ưu ảnh, kiểm tra, và đưa lên mạng. |
| 0:26 | Thanh 3 bước: `① Ảnh nhẹ ② Trang chuẩn ③ Kiểm tra & đưa lên mạng` | |
| **0:30** | **① ẢNH NHẸ** — Thư mục `anh-goc/`: 3 ảnh, mỗi ảnh khoảng 3 MB, 4000px | Lỗi số một khiến landing page chậm: ảnh chụp từ điện thoại hay máy ảnh, mỗi ảnh vài megabyte, tải thẳng lên web. |
| 0:42 | Dán PROMPT 1 → Claude viết `toi-uu-anh.py` → chạy: bảng trước/sau từng ảnh + đoạn `<img srcset>` mẫu | Claude viết công cụ: mỗi ảnh tạo hai bản WebP, một cho máy tính, một cho điện thoại, kèm sẵn đoạn mã ảnh có kích thước chuẩn để trang không bị "giật" khi tải. Ảnh thật thường nhẹ đi chín mươi phần trăm. |
| **1:00** | **② TRANG CHUẨN** — Mở `yeu-cau-landing.md`: 7 khối nội dung + yêu cầu kỹ thuật | Bản brief có bảy khối nội dung và một danh sách yêu cầu kỹ thuật: một file duy nhất, dưới năm trăm kilobyte, dữ liệu có cấu trúc, chuẩn truy cập cho người khiếm thị. |
| 1:15 | Dán PROMPT 2 → Claude **hỏi lại**: "Brief có 'ngồi thử miễn phí tại văn phòng khách' nhưng CLAUDE.md chỉ có 'ngồi thử tại showroom'. Dùng câu nào?" `SFX: ding` | Và đây: Claude dừng lại hỏi. Brief viết "ngồi thử miễn phí tại văn phòng khách", nhưng bộ sự thật chỉ có "ngồi thử tại showroom". Một lời hứa sai trên landing page là lời hứa với **mọi** khách hàng đọc nó. Mình chọn theo bộ sự thật. |
| 1:35 | Claude viết `landing/index.html` `[TUA x8]` → mở trình duyệt: hero, 3 lợi ích, 2 gói giá, 4 bước, FAQ, form | Kết quả: một trang gọn gàng, đủ bảy khối, đúng thứ tự. |
| 1:50 | Zoom mã nguồn: `<script type="application/ld+json">` với LocalBusiness, Product + Offer (giá VND), FAQPage | Phần người xem không thấy nhưng Google thấy: dữ liệu có cấu trúc. Thông tin doanh nghiệp, hai sản phẩm kèm giá, và bộ câu hỏi thường gặp. |
| 2:05 | Zoom: không có `aggregateRating` · `TEXT: KHÔNG bịa đánh giá sao` | Và chú ý một thứ **không có**: đánh giá năm sao. Nhiều hướng dẫn trên mạng dạy chèn điểm đánh giá vào dữ liệu có cấu trúc cho đẹp. Không có đánh giá thật thì đó là bịa đặt, vi phạm chính sách của Google và có thể bị phạt. |
| **2:20** | **③ KIỂM TRA** — Dán PROMPT 3 → Claude dùng Playwright chụp trang ở 390px và 1366px, kiểm tra cuộn ngang, đo dung lượng, kiểm tra tương phản màu | Bước ba: đừng tin mắt mình trên màn hình máy tính. Claude mở trang ở kích thước điện thoại, chụp lại, kiểm tra có bị tràn ngang không, đo dung lượng, và đo độ tương phản màu. |
| 2:38 | Ảnh chụp điện thoại **trước khi sửa**: chữ hero dính sát mép trái → Claude tự phát hiện, sửa CSS → chụp lại: lề 20px | Lần đầu, nó phát hiện chữ trên điện thoại dính sát mép màn hình, một lỗi CSS rất nhỏ. Sửa, chụp lại, ổn. Chính mình cũng gặp lỗi này khi làm bản mẫu cho video. |
| 2:55 | Edge → F12 → Lighthouse → Mobile → Analyze → kết quả | Đo bằng Lighthouse có sẵn trong Edge, chế độ điện thoại. |
| 3:08 | Kéo thư mục `landing` vào trang **app.netlify.com/drop** → 10 giây → đường link `https://….netlify.app` mở trên điện thoại | Đưa lên mạng: cách đơn giản nhất là kéo thả. Kéo thư mục vào trang Netlify Drop. Mười giây sau, bạn có đường link mở được trên mọi điện thoại. |
| 3:25 | `TEXT: Dân kỹ thuật: GitHub Pages / Cloudflare Pages + tên miền riêng` | Nếu công ty có quy trình riêng, cùng thư mục này đưa lên GitHub Pages hay Cloudflare Pages, gắn tên miền công ty, đều được. |
| **3:38** | **MẸO PRO 1** — `⚠️ TEXT: Form demo → thay bằng form thật (Google Forms / Formspree / CRM) TRƯỚC khi chạy quảng cáo` | Lưu ý quan trọng: form trong bản demo trỏ tới một địa chỉ giả. Trước khi chạy quảng cáo, hãy nối nó với nơi thật sự nhận dữ liệu, như Google Forms, Formspree hay CRM của công ty, và bấm thử gửi một lần. |
| 3:55 | **MẸO PRO 2** — `TEXT: Thử A/B: nhờ Claude làm phương án B (tiêu đề / nút khác), đo bằng UTM (tập 17)` | Mẹo hai: nhờ Claude làm luôn phương án B với tiêu đề hoặc nút bấm khác, chạy song song, đo bằng mã UTM như tập trước. Bản nào ra nhiều khách hơn thì giữ. |
| 4:10 | Tóm tắt: `Ảnh: WebP + srcset` · `Dữ liệu có cấu trúc: thật, không bịa` · `Kiểm tra trên điện thoại` · `Form thật trước khi chạy quảng cáo` | |
| 4:25 | `TEXT: BÀI TẬP: 1 trang giới thiệu dịch vụ của bạn → Netlify Drop` | Bài tập: làm một trang giới thiệu dịch vụ của bạn, hay của phòng bạn, rồi kéo lên Netlify Drop. |
| 4:35 | Teaser: lịch Thứ 2 7:00 → chuỗi: nghiên cứu → brief → viết → chấm → nháp WordPress → 4 kênh → thông báo "Chờ duyệt" | Tập cuối của phần nâng cao: ghép mọi thứ từ tập mười một đến giờ thành một **cỗ máy nội dung** tự chạy mỗi tuần. Bạn chỉ còn một việc: đọc và bấm duyệt. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1**
```text
Viết toi-uu-anh.py: với mọi ảnh JPG/PNG trong anh-goc/, xoay đúng chiều theo EXIF, tạo 2 bản WebP rộng 1600px và 800px
(quality 72) vào landing/anh/, in bảng dung lượng trước/sau và đoạn <img> mẫu có srcset, sizes, width, height. Chạy luôn.
```

**PROMPT 2**
```text
Dựng landing/index.html theo đúng @yeu-cau-landing.md. Mọi cam kết phải có trong @CLAUDE.md: thông tin nào trong brief
không có trong CLAUDE.md thì HỎI tôi trước. Một file HTML, CSS nhúng, không framework. Dùng ảnh trong landing/anh/ (srcset,
lazy cho ảnh dưới màn hình đầu, fetchpriority=high cho ảnh hero). JSON-LD: LocalBusiness, Product + Offer cho 2 gói, FAQPage
(nội dung FAQ trên trang và trong JSON-LD phải giống nhau). KHÔNG thêm aggregateRating hay đánh giá. Kèm robots.txt và sitemap.xml.
```

**PROMPT 3**
```text
Kiểm tra landing/index.html bằng Playwright (Edge): chụp màn hình ở 390×844 và 1366×768, kiểm tra có cuộn ngang không,
đo tổng dung lượng ở chế độ điện thoại (HTML + ảnh 800w), kiểm tra JSON-LD parse được, title/mô tả đúng độ dài,
mọi ảnh có alt + width/height, mọi ô form có label, tương phản màu chữ/nền ≥ 4.5:1. Có lỗi thì sửa rồi kiểm tra lại.
```

## Gói đăng tải

- **Tiêu đề:** A: `Landing page chuẩn SEO, tải dưới 1 giây, lên mạng trong 15 phút | Claude nâng cao #19` · B: `Làm landing page bằng AI mà không bịa: dữ liệu có cấu trúc, ảnh nhẹ, kéo thả lên mạng`
- **Thumbnail:** Điện thoại hiển thị landing + 4 vòng tròn Lighthouse xanh. Chữ: **"15 PHÚT · ONLINE"**.
- **Shorts:** (1) 1:15–1:35 "AI hỏi lại trước khi hứa với khách hàng", (2) 2:05–2:20 "Đừng bịa đánh giá 5 sao trong schema".
