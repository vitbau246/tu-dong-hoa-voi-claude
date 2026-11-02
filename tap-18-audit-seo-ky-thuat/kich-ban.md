# Tập 18: Khám SEO kỹ thuật toàn website trong 1 phút, và để Claude tự sửa

| | |
|---|---|
| **Mục tiêu người xem** | Phát hiện các lỗi kỹ thuật "chết người" mà mắt thường không thấy (robots.txt, noindex, canonical, link gãy, trang mồ côi…), xếp ưu tiên, sửa tự động, đo lại |
| **Tính năng dạy** | Claude viết crawler (WebFetch không mở được localhost), xếp mức độ nghiêm trọng, sửa hàng loạt file HTML, tạo sitemap.xml, nén ảnh, Lighthouse có sẵn trong Edge DevTools để đo trước/sau |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/website/` (15 trang hư cấu, gài **12 loại lỗi**, tổng 31 lỗi). `--giai-phap` chép `kiem-tra-ky-thuat.py` |
| **Đã kiểm thử** | Crawler bắt đủ **31/31 lỗi** (6 nghiêm trọng · 7 cao · 9 trung bình · 9 thấp), điểm **0/100** · Sau khi sửa trên bản sao: **100/100, 0 báo nhầm** · Ảnh hero 2,2 MB → 235 KB (WebP) |

## Chuẩn bị

1. `python chuan-bi.py --giai-phap`, mở `tap-18-audit-seo-ky-thuat/demo`. Terminal: `python -m http.server 8002 -d website`.
2. Đo Lighthouse "trước": Edge → http://localhost:8002 → F12 → tab **Lighthouse** → chọn SEO + Performance → Analyze. Chụp màn hình điểm. Lưu ý: Lighthouse chỉ chấm **trang đang mở**, còn crawler quét **toàn website** (link gãy, trang mồ côi, trùng title giữa các trang). Đó là lý do cần cả hai.
3. Có thể dùng thêm prompt viết crawler (PROMPT phụ) nếu muốn quay cảnh Claude tự viết.
4. Quay lại cảnh: `python chuan-bi.py --giai-phap` để khôi phục site đầy lỗi.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Mở `robots.txt`: dòng `Disallow: /san-pham/` phát sáng đỏ | Một dòng. Chỉ một dòng này khiến Google **không đọc được bất kỳ trang sản phẩm nào** của website. |
| 0:07 | Terminal: `ĐIỂM SỨC KHỎE: 0/100 · 6 NGHIÊM TRỌNG …` → tua → `100/100` | Website này có ba mươi mốt lỗi kỹ thuật. Một phút để tìm, vài phút để Claude sửa hết. |
| 0:14 | Người dẫn | Bạn có thể viết bài hay nhất thế giới, nhưng nếu website mắc lỗi kỹ thuật thì Google không thấy, hoặc thấy sai. Những lỗi này thường do một lần cập nhật website, một plugin, hay một bạn lập trình viên "tạm chặn" rồi quên mở lại. Hôm nay mình khám toàn bộ, và để Claude chữa. |
| 0:30 | Thanh 3 bước: `① Khám ② Xếp ưu tiên ③ Chữa & đo lại` | |
| **0:33** | **① KHÁM** — `TEXT: WebFetch không mở được localhost → Claude viết crawler riêng` | Website đang chạy trên máy mình, ở localhost. Công cụ đọc web của Claude từ chối địa chỉ nội bộ, nên mình bảo Claude viết một con bọ: bò từ trang chủ qua mọi liên kết, kiểm tra từng trang. |
| 0:48 | Chạy `python kiem-tra-ky-thuat.py http://localhost:8002 --thu-muc website` `[TUA x4]` → bảng tóm tắt đỏ | Mười lăm giây. Ba mươi mốt lỗi. Điểm sức khỏe: không. |
| **1:00** | **② XẾP ƯU TIÊN** — Mở `bao-cao-audit.md`, khối NGHIÊM TRỌNG | Quan trọng là không sửa lung tung, mà sửa theo mức độ nghiêm trọng. |
| 1:08 | Zoom: 5 dòng "Bị robots.txt chặn" (5 trang sản phẩm) | Nghiêm trọng số một: năm trang sản phẩm, toàn bộ hàng hóa của công ty, bị robots.txt chặn. Tức là sáu tháng qua, mọi công sức tối ưu các trang này đều vô nghĩa. |
| 1:22 | Zoom: "/ghe-cong-thai-hoc/: Có thẻ noindex" | Nghiêm trọng số hai: danh mục ghế công thái học, nhóm lãi cao nhất ở tập mười lăm, mang thẻ "noindex", tức là tự xin Google **đừng hiển thị** trang này. |
| 1:35 | Khối CAO: canonical của Ergo Lite trỏ về trang chủ · 3 link gãy · 2 trang trùng title · không có sitemap | Mức cao: trang Ergo Lite tự nói với Google "bản chính của tôi là trang chủ", nên Google sẽ bỏ qua nó. Ba liên kết gãy. Hai sản phẩm trùng tiêu đề. Không có sơ đồ trang. |
| 1:52 | Khối TRUNG BÌNH: "Trang mồ côi" ×3 · ảnh hero 2.160 KB | Mức trung bình có một lỗi rất hay gặp: **trang mồ côi**, tức trang có tồn tại nhưng không trang nào liên kết tới. Google gần như không tìm thấy chúng. Và một ảnh nặng hơn hai megabyte trên trang chủ. |
| **2:05** | **③ CHỮA** — Dán PROMPT 1 → Claude trình bày kế hoạch sửa theo thứ tự ưu tiên, **hỏi** 2 việc cần người quyết: "trang khuyen-mai-cu.html đã xóa: chuyển hướng hay bỏ link?" và "tiêu đề mới cho Ergo Lite?" | Mình bảo Claude sửa theo thứ tự ưu tiên. Để ý: nó **hỏi lại** hai việc cần người quyết, như trang khuyến mãi cũ nên chuyển hướng đi đâu. Không phải lỗi nào cũng sửa máy móc được. |
| 2:25 | Claude sửa `[TUA x10]`: robots.txt, gỡ noindex, sửa canonical, gỡ 3 link gãy, viết title/mô tả riêng, thêm H1, viewport, alt ảnh, liên kết tới 3 trang mồ côi, nén hero sang WebP, tạo `sitemap.xml` | Rồi nó sửa: mở robots.txt, gỡ noindex, sửa canonical, gỡ liên kết gãy, viết tiêu đề và mô tả riêng cho từng trang, thêm mô tả ảnh, đưa liên kết tới ba trang mồ côi, nén ảnh, và tạo sơ đồ trang. Mười lăm file trong một lượt. |
| 2:50 | Chạy lại crawler → **100/100 · 0 lỗi** `SFX: ding` | Chạy lại. Một trăm điểm. |
| 3:00 | Edge DevTools → Lighthouse chạy lại: điểm SEO và Performance trước/sau đặt cạnh nhau | Đo bằng Lighthouse có sẵn trong Edge: điểm tốc độ tăng rõ nhờ ảnh nhẹ hơn mười lần. |
| 3:12 | `git diff --stat` (hoặc danh sách file đã sửa) | Và vì mọi thay đổi đều là sửa file, bạn xem lại từng dòng được, hoàn tác được. Đừng bao giờ để AI sửa thẳng trên website đang chạy thật. Hãy sửa mã nguồn, xem lại, rồi mới triển khai. |
| **3:28** | **MẸO PRO 1** — `TEXT: Website WordPress? Audit vẫn chạy được trên URL thật (requests + tôn trọng robots)` | Website của bạn là WordPress? Crawler vẫn chạy được trên địa chỉ thật. Phần sửa thì làm trong trang quản trị, hoặc qua API như tập trước. |
| 3:42 | **MẸO PRO 2** — `TEXT: Gắn audit vào lịch hằng tuần (tập 8) → lỗi mới xuất hiện là biết ngay` | Mẹo hai: cho crawler chạy mỗi tuần bằng Task Scheduler. Lỗi robots.txt lần sau xuất hiện, bạn biết trong vòng bảy ngày, không phải sáu tháng. |
| 3:58 | `⚠️ TEXT: 100 điểm kỹ thuật = Google ĐỌC ĐƯỢC. Lên top còn cần nội dung tốt (tập 15–16)` | Một trăm điểm kỹ thuật nghĩa là Google đọc được website của bạn. Còn lên top hay không vẫn do nội dung, như hai tập trước. |
| 4:12 | Tóm tắt: `Khám bằng crawler` · `Sửa theo mức nghiêm trọng` · `Người quyết việc cần quyết` · `Đo lại + theo dõi hằng tuần` | |
| 4:25 | `TEXT: BÀI TẬP: mở robots.txt website của bạn (tenmien.vn/robots.txt). Có dòng Disallow nào lạ không?` | Bài tập ba mươi giây: gõ tên miền của bạn, gạch chéo robots.txt. Có dòng Disallow nào lạ không? |
| 4:35 | Teaser: landing page mới tinh hiện trên điện thoại, Lighthouse 4 vòng tròn xanh 100 | Tập sau: làm luôn một landing page mới từ con số không, chuẩn SEO, tải nhanh, điểm Lighthouse xanh, và đưa lên Internet. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (chữa)
```text
Đọc bao-cao-audit.md. Sửa mã nguồn trong website/ theo thứ tự NGHIÊM TRỌNG → CAO → TRUNG BÌNH → THẤP.
Trước khi sửa, liệt kê những việc cần tôi quyết định (ví dụ trang đã xóa nên chuyển hướng đi đâu, tiêu đề mới) và HỎI tôi.
Tạo sitemap.xml (khai báo trong robots.txt), nén ảnh quá nặng sang WebP và cập nhật đường dẫn.
Viết title và meta description RIÊNG cho từng trang theo nội dung trang, không dùng câu chung chung.
Sửa xong chạy lại: python kiem-tra-ky-thuat.py http://localhost:8002 --thu-muc website cho tới khi không còn lỗi.
```

**PROMPT phụ** (viết crawler)
```text
Viết kiem-tra-ky-thuat.py: crawl website từ trang chủ theo liên kết nội bộ (requests, bỏ proxy cho localhost, BeautifulSoup).
Kiểm tra: robots.txt chặn (urllib.robotparser, Googlebot), noindex, canonical thiếu/trỏ sai, link nội bộ 4xx, trùng title,
title > 60 ký tự, thiếu meta description, số H1 ≠ 1, thiếu viewport, ảnh thiếu alt, ảnh > 300 KB, thiếu sitemap.xml,
trang mồ côi (so với file trên đĩa qua --thu-muc, và vẫn quét nội dung trang mồ côi).
Xếp mức NGHIÊM TRỌNG/CAO/TRUNG BÌNH/THẤP, điểm sức khỏe /100, xuất bao-cao-audit.md + loi-seo.csv.
```

## Đối chiếu (dap-an.json)

Nghiêm trọng: robots.txt chặn `/san-pham/` (5 trang) · noindex `/ghe-cong-thai-hoc/` — Cao: canonical Ergo Lite → trang chủ · 3 link gãy · trùng title Ergo Pro/Lite · thiếu sitemap — Trung bình: 2 thiếu mô tả · 1 trang 2 H1 · 1 trang 0 H1 · 3 trang mồ côi · 1 thiếu viewport · ảnh hero 2,2 MB — Thấp: 2 title dài · 3 thiếu canonical · 4 ảnh thiếu alt.

## Gói đăng tải

- **Tiêu đề:** A: `1 dòng robots.txt giết chết SEO cả website: audit & tự sửa bằng AI | Claude nâng cao #18` · B: `Khám SEO kỹ thuật toàn website: 0 → 100 điểm trong 5 phút`
- **Thumbnail:** `Disallow: /san-pham/` chữ đỏ khổng lồ. Chữ: **"1 DÒNG = MẤT HẾT"**.
- **Shorts:** (1) 0:00–0:14 + 1:08–1:22 "Một dòng chặn toàn bộ sản phẩm", (2) 1:52–2:05 "Trang mồ côi là gì".
