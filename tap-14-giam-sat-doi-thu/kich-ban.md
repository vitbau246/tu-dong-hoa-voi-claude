# Tập 14: Máy theo dõi đối thủ 24/7: phát hiện đổi giá và đề xuất hành động

| | |
|---|---|
| **Mục tiêu người xem** | Dựng hệ thống theo dõi website đối thủ: tự chụp dữ liệu theo lịch → so với lần trước → **chỉ khi có thay đổi** mới gọi Claude viết nhận định + so với bảng giá của mình |
| **Tính năng dạy** | Nguyên tắc **"AI ở đúng chỗ"** (script làm việc máy móc, AI làm việc cần suy nghĩ), `claude -p` gọi từ Python, Task Scheduler nhiều mốc giờ, xử lý proxy công ty |
| **Dữ liệu** | `python chuan-bi.py` tạo website đối thủ hư cấu (ngày 1) + `bang-gia-cua-minh.csv`. `python chuan-bi.py --ngay 2` mô phỏng đối thủ đổi giá qua đêm. `--giai-phap` chép `theo-doi.py` + `dang-ky-theo-doi.ps1` |
| **Đã kiểm thử (30/10/2026)** | Phát hiện **11/11 thay đổi** gài sẵn · Không thay đổi thì **không gọi AI** · Bước Claude chạy thật: báo cáo nửa trang, số liệu đúng (đối thủ rẻ hơn 15,0% / 14,0% / 12,2%), còn tự phát hiện "combo giấy" để kéo khách. Mẫu: `giai-phap/ket-qua-mau/` |

## Chuẩn bị

1. `python chuan-bi.py --giai-phap`, mở `tap-14-giam-sat-doi-thu/demo`. Terminal 1: `python -m http.server 8001 -d web-doi-thu`.
2. Cần Claude Code CLI (tập 8). Nếu `claude` không có trong PATH: `$env:CLAUDE_EXE = "<đường dẫn claude.exe>"`.
3. Thứ tự quay: chạy `theo-doi.py` (ngày 1) → chạy lần nữa (không thay đổi) → `python ..\chuan-bi.py --ngay 2` → chạy `theo-doi.py` (có thay đổi + gọi Claude).

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Thông báo Windows "Đối thủ vừa thay đổi" → báo cáo mở ra: bảng "Mặt hàng đối thủ đang RẺ HƠN mình: −15,0% · −14,0% · −12,2%" | Tám giờ sáng. Máy báo: đêm qua đối thủ giảm giá ba mặt hàng chủ lực, giờ họ rẻ hơn mình mười hai đến mười lăm phần trăm. |
| 0:08 | Zoom mục "Đề xuất hành động trong hôm nay" | Kèm ba việc nên làm ngay hôm nay. Mình chưa phải mở website của đối thủ lần nào. |
| 0:14 | Người dẫn | Ai làm kinh doanh cũng muốn biết đối thủ đổi giá lúc nào, nhưng không ai có thời gian ngồi canh. Hôm nay mình dựng một hệ thống canh thay bạn. Và mình sẽ chỉ một nguyên tắc thiết kế giúp nó chạy mỗi ngày mà gần như **không tốn hạn mức AI**. |
| 0:30 | Thanh 3 bước: `① Chụp & so sánh (không AI) ② AI chỉ khi có thay đổi ③ Hẹn giờ` | |
| **0:33** | **① CHỤP & SO SÁNH** — Sơ đồ: `Website → [script chụp] → ảnh chụp JSON → [so với lần trước] → danh sách thay đổi` | Nguyên tắc "AI ở đúng chỗ": việc máy móc như lấy giá, so sánh, tính phần trăm thì để **script thường** làm. Miễn phí, chính xác tuyệt đối, chạy nghìn lần cũng được. |
| 0:50 | Dán PROMPT 1 → Claude viết `theo-doi.py` (zoom phần `CHON = {...}` selector, `so_sanh`) | Mình nhờ Claude viết script. Phần đáng chú ý là bộ chọn ở đầu file: đổi sang theo dõi website khác thì chỉ sửa vài dòng này. |
| 1:05 | Terminal: chạy lần 1 → "Lần chụp đầu tiên: 15 sản phẩm" · chạy lần 2 → "Không có thay đổi. Không gọi AI → không tốn hạn mức" | Lần đầu: ghi nhận mười lăm sản phẩm. Lần hai: không có gì thay đổi, nên **không gọi AI**. Phần lớn các ngày sẽ như thế này, và chi phí bằng không. |
| 1:22 | `TEXT: ⚠️ Máy công ty có proxy?` Zoom đoạn `proxies={"http": None...}` | Một lỗi rất hay gặp ở máy văn phòng: mạng công ty có proxy, script gọi địa chỉ nội bộ lại bị đẩy ra proxy và trả về trang trống. Mình gặp đúng lỗi này khi làm video. Claude đã thêm đoạn cho địa chỉ nội bộ đi thẳng. |
| **1:40** | **② AI KHI CÓ THAY ĐỔI** — Terminal: `python ..\chuan-bi.py --ngay 2` (`TEXT: Mô phỏng: một đêm trôi qua…`) | Giờ mô phỏng một đêm trôi qua, đối thủ cập nhật website. |
| 1:50 | Chạy `theo-doi.py` → "11 thay đổi: 3 giảm giá · 2 tăng giá · 2 hết hàng · 1 có hàng lại · 2 mới · 1 ngừng bán" | Chạy lại. Mười một thay đổi, phân loại rõ ràng. Tới đây vẫn chưa có AI. |
| 2:02 | Zoom đoạn yêu cầu gửi cho Claude: "chỉ dùng số có trong 2 file", `--allowedTools Read,Write`, `--max-budget-usd 0.5` | Chỉ lúc này script mới gọi Claude, kèm hai file: danh sách thay đổi và bảng giá **của mình**. Quyền chỉ có đọc và ghi, giới hạn nửa đô mỗi lần. |
| 2:15 | Báo cáo mở ra `[TUA]`: mục 1 "3 thay đổi quan trọng nhất", mục 2 bảng rẻ hơn, mục 3 hành động | Và đây là phần script **không thể** làm: Claude nhận ra ba mặt hàng bị giảm giá là ba mặt hàng mà **trước đây mình rẻ hơn**. Giờ thì ngược lại. |
| 2:32 | Highlight đoạn: "combo 5 thùng giấy 1.850.000đ = 370.000đ/thùng, rẻ hơn giá lẻ của mình… đồng thời tăng giá thùng lẻ → kéo khách sang combo" | Đoạn này mình thích nhất. Đối thủ vừa tung combo năm thùng giấy, vừa tăng giá thùng lẻ. Claude đọc ra **chiến thuật**: họ đang kéo khách sang mua số lượng lớn. Đó mới là nhận định, không chỉ là con số. |
| 2:52 | Highlight "hết chuột M331, bút Parker, ngừng bảng trắng → cơ hội giành khách" | Và mặt tích cực: đối thủ hết ba mặt hàng, đó là cơ hội của mình ngay hôm nay. |
| **3:05** | **③ HẸN GIỜ** — Chạy `dang-ky-theo-doi.ps1 -Url "http://localhost:8001" -ChayNgay` → "Đã đăng ký: 8:00 và 14:00 hằng ngày" | Bước ba: hẹn giờ hai lần mỗi ngày, tám giờ sáng và hai giờ chiều. Có thay đổi thì thông báo và mở báo cáo, không thì im lặng. |
| 3:18 | Task Scheduler: 2 trigger. Thư mục `anh-chup/` với nhiều file theo giờ | Mỗi lần chạy, ảnh chụp được lưu lại. Sau một tháng, bạn có lịch sử giá của đối thủ để biết họ hay giảm giá vào thời điểm nào. |
| **3:30** | **MẸO PRO** — Bảng chi phí: `30 ngày × 2 lần = 60 lần chạy` · `Script: 60 lần, 0đ` · `AI: chỉ ~5–10 lần có thay đổi` | Làm phép tính: một tháng chạy sáu mươi lần, nhưng AI chỉ thức dậy năm đến mười lần, khi thực sự có chuyện. Nếu để AI đọc website cả sáu mươi lần, bạn tốn gấp mười lần mà kết quả không tốt hơn. Đây là nguyên tắc cho **mọi** hệ thống tự động: AI ở đúng chỗ. |
| 3:55 | `TEXT: Website thật dùng JavaScript? → thay requests bằng Playwright / API (tập 13)` | Với website thật dùng JavaScript, chỉ cần thay phần chụp bằng Playwright, hoặc tốt hơn, tìm API như tập trước. Phần còn lại giữ nguyên. |
| 4:08 | `⚠️ TEXT: Chỉ theo dõi thông tin công khai · Tần suất vừa phải · Tôn trọng điều khoản website` | Nhắc lại: chỉ theo dõi thông tin công khai, tần suất vừa phải, tôn trọng điều khoản của website. |
| 4:20 | Tóm tắt: `Script: chụp + so sánh` · `AI: chỉ khi có thay đổi` · `Hẹn giờ: im lặng khi bình thường` | |
| 4:30 | `TEXT: BÀI TẬP: theo dõi 1 trang công khai bạn quan tâm (bảng giá, thông báo tuyển dụng, văn bản mới…)` | Bài tập: không nhất thiết là đối thủ. Có thể là trang thông báo văn bản mới của một cơ quan, hay trang tuyển dụng. Cùng một công thức. |
| 4:38 | Teaser: bảng Google Search Console, cột "Vị trí 11" sáng lên | Từ tập sau mình chuyển sang mảng nhiều người hỏi nhất: **SEO**. Bắt đầu bằng việc tìm những từ khóa đang nằm sát trang một, chỉ cần đẩy nhẹ là lên. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1**
```text
Viết theo-doi.py nhận URL website cần theo dõi:
1. Tải trang (requests + BeautifulSoup); với địa chỉ localhost/nội bộ thì không đi qua proxy. Lấy mọi sản phẩm: mã (data-sku), tên, giá, còn hàng.
   Đặt các CSS selector trong một dict ở đầu file để dễ đổi website.
2. Lưu ảnh chụp anh-chup/<thời điểm>.json. So với ảnh chụp gần nhất: giảm giá, tăng giá (kèm %), hết hàng, có hàng lại, sản phẩm mới, ngừng bán.
3. Không có thay đổi → in thông báo và DỪNG (không gọi AI).
4. Có thay đổi → lưu thay-doi/<thời điểm>.json rồi gọi claude -p (--allowedTools Read,Write --max-budget-usd 0.5)
   để viết bao-cao-doi-thu/<thời điểm>.md: 3 thay đổi quan trọng nhất, bảng mặt hàng đối thủ rẻ hơn mình (so với bang-gia-cua-minh.csv),
   2–3 hành động đề xuất hôm nay. Không bịa số. Tham số --khong-ai để chỉ in yêu cầu.
```

**PROMPT 2**
```text
Viết dang-ky-theo-doi.ps1 (PowerShell 5.1, UTF-8 BOM): nhận -Url, đăng ký Task Scheduler chạy theo-doi.py lúc 8:00 và 14:00 hằng ngày,
ghi nhật ký; nếu có báo cáo mới thì hiện thông báo Windows và mở báo cáo. Tham số -ChayNgay để chạy thử.
```

## Gói đăng tải

- **Tiêu đề:** A: `Máy theo dõi giá đối thủ 24/7, AI chỉ thức dậy khi có biến | Claude nâng cao #14` · B: `Đối thủ giảm giá lúc nửa đêm? Sáng ra bạn đã có kế hoạch phản công`
- **Thumbnail:** Thông báo điện thoại "Đối thủ giảm 16%" + mũi tên đỏ. Chữ: **"CANH ĐỐI THỦ 24/7"**.
- **Shorts:** (1) 2:15–2:52 "AI đọc ra chiến thuật combo của đối thủ", (2) 3:30–3:55 "Nguyên tắc AI ở đúng chỗ".
