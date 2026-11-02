# Tập 13: Duyệt web nâng cao: trang JavaScript, cần đăng nhập, cuộn vô hạn, và "cửa sau" API

| | |
|---|---|
| **Mục tiêu người xem** | Xử lý 3 loại trang mà công cụ đọc web thông thường bó tay; biết **chọn công cụ nhẹ nhất** cho từng loại; đăng nhập an toàn (không lộ mật khẩu) |
| **Tính năng dạy** | Playwright MCP (cuộn, đăng nhập, xem request mạng), tìm API JSON ẩn, chuyển thành script Python chạy độc lập, lưu phiên đăng nhập, `@browser` (Claude in Chrome) |
| **Trang luyện tập** | **quotes.toscrape.com**: trang công khai được làm ra để luyện thu thập dữ liệu (hợp pháp, an toàn khi quay) |
| **Đã kiểm thử (30/10/2026)** | HTML gốc của `/scroll` có **0** trích dẫn · Gọi API ẩn: **100 trích dẫn, 50 tác giả trong 7,6 giây** · Script Playwright có đăng nhập: 100/100 liên kết Goodreads, 20,5 giây, lần 2 dùng lại phiên |

## Chuẩn bị

1. `pip install playwright requests openpyxl` (Playwright dùng **Edge có sẵn**, không cần `playwright install`). Node.js cho Playwright MCP.
2. `python chuan-bi.py --giai-phap`, mở `tap-13-duyet-web-nang-cao/demo`, mở cuộc trò chuyện mới và duyệt MCP server `playwright`.
3. Mở sẵn Edge, tab `quotes.toscrape.com/scroll`, DevTools (F12) tab **Network** để quay cảnh tìm API.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Trình duyệt hiện trang `/scroll` đầy trích dẫn. Cắt sang terminal: `curl .../scroll \| grep -c quote` → **0** | Trình duyệt thấy một trăm câu trích dẫn. Còn máy đọc web thì thấy… không câu nào. |
| 0:07 | Terminal: `python thu-thap-api.py` → "100 trích dẫn · 50 tác giả · 7,6 giây" | Cuối video, mình lấy đủ một trăm câu trong bảy giây, không cần mở trình duyệt. |
| 0:13 | Người dẫn | Ngoài đời, website khó hơn nhiều so với trang demo ở tập bảy. Có trang chỉ hiện nội dung khi cuộn, có trang bắt đăng nhập, có trang do JavaScript vẽ ra. Hôm nay mình xử lý cả ba, và chỉ cho bạn một "cửa sau" mà dân chuyên nghiệp luôn tìm trước. |
| 0:28 | Thanh 3 bước: `① Cuộn vô hạn ② Đăng nhập an toàn ③ Tìm cửa sau API` + `TEXT: quotes.toscrape.com = trang luyện tập hợp pháp` | Mình dùng quotes.toscrape.com, một trang được làm ra **để luyện** thu thập dữ liệu. |
| **0:35** | **① CUỘN VÔ HẠN** — Dán PROMPT 1 (thử WebFetch trước) → Claude báo: "HTML không chứa trích dẫn, nội dung được tải bằng JavaScript khi cuộn" | Thử cách thường trước: bảo Claude đọc trang bằng WebFetch. Nó báo trang trống, vì nội dung chỉ được tải về **khi bạn cuộn**. Đọc HTML thì không có gì. |
| 0:52 | Dán PROMPT 2 → Edge (Playwright MCP) mở `/scroll`, tự cuộn, nội dung tải dần `[TUA x6]` → Claude đếm đủ 100, dừng khi hết | Giờ dùng trình duyệt thật qua Playwright: mở trang, cuộn xuống, chờ tải, cuộn tiếp, và tự biết dừng khi không còn gì mới. Một trăm câu. |
| 1:10 | `TEXT: Dấu hiệu "hết": cuộn mà số mục không tăng` | Mẹo trong prompt: định nghĩa rõ thế nào là "hết". Cuộn mà số mục không tăng nữa thì dừng. Không có câu này, AI có thể cuộn mãi, hoặc dừng quá sớm. |
| **1:20** | **② ĐĂNG NHẬP AN TOÀN** — `TEXT: ⚠️ KHÔNG BAO GIỜ dán mật khẩu vào khung chat` | Trang thứ hai cần đăng nhập. Quy tắc số một: **không bao giờ** dán mật khẩu thật vào khung chat. Nội dung chat được gửi lên máy chủ và lưu lại trong lịch sử. |
| 1:32 | Dán PROMPT 3 → Edge mở trang login, Claude **dừng lại**: "Bạn hãy tự đăng nhập trong cửa sổ trình duyệt, xong báo tôi" → người dẫn tự gõ, bấm Login → "xong" | Cách an toàn: Claude mở trang đăng nhập rồi **dừng lại**. Mình tự gõ tài khoản trong cửa sổ trình duyệt, Claude không nhìn thấy mật khẩu. Đăng nhập xong mình báo, Claude làm tiếp. |
| 1:52 | Claude thu thập 10 trang, đếm "100/100 có liên kết Goodreads" | Bằng chứng đăng nhập thành công: mỗi câu giờ có thêm liên kết Goodreads, thứ chỉ hiện khi đã đăng nhập. Một trăm trên một trăm. |
| 2:05 | Dán PROMPT 4 → Claude viết `thu-thap-dang-nhap.py`: zoom `os.environ["WEB_USER"]`, `storage_state`, `.gitignore` có `phien-dang-nhap.json` | Việc này lặp lại hằng ngày thì sao? Mình bảo Claude viết thành script. Ba chi tiết an toàn: mật khẩu đọc từ biến môi trường chứ không viết trong code; phiên đăng nhập được lưu để lần sau khỏi đăng nhập; và file phiên đó bị **loại khỏi git**, vì nó chẳng khác gì chìa khóa tài khoản. |
| 2:28 | Terminal: chạy 2 lần → lần 1 "Đăng nhập mới…", lần 2 "Dùng lại phiên đã lưu" · "20,5 giây" | Chạy lần một: đăng nhập. Lần hai: dùng lại phiên. Hai mươi giây cho mười trang. |
| **2:40** | **③ CỬA SAU API** — Edge DevTools → tab Network → cuộn `/scroll` → hiện request `api/quotes?page=2` → click → JSON đẹp | Giờ là bí quyết của dân chuyên nghiệp. Mở DevTools, tab Network, rồi cuộn trang. Thấy chưa: mỗi lần cuộn, trang gọi một địa chỉ `api/quotes` và nhận về dữ liệu **JSON** sạch sẽ. Trang web cũng chỉ đang "đọc" từ cửa sau này. |
| 3:00 | Dán PROMPT 5 → Claude dùng công cụ xem request mạng của Playwright, tìm ra API, viết `thu-thap-api.py` → chạy: **7,6 giây** | Claude cũng tự tìm được: nó xem danh sách request của trình duyệt, nhận ra API, rồi viết script gọi thẳng vào đó. Không trình duyệt. Bảy phẩy sáu giây, bao gồm cả nửa giây nghỉ giữa mỗi lần gọi cho lịch sự. |
| 3:18 | Bảng so sánh: `Playwright MCP (AI lái): vài phút · tốn hạn mức` · `Script trình duyệt: 20,5 giây` · `Gọi API: 7,6 giây` | So sánh ba cách: để AI lái trình duyệt mất vài phút và tốn hạn mức. Script trình duyệt: hai mươi giây. Gọi API: bảy giây. |
| **3:30** | **MẸO PRO 1** — Sơ đồ quyết định: `Trang tĩnh? → requests` · `Có API trong Network? → gọi API` · `Cần JS/đăng nhập? → Playwright script` · `Khám phá lần đầu / việc 1 lần → Playwright MCP` | Đây là sơ đồ mình dùng cho mọi website: trang tĩnh thì đọc thẳng. Có API thì gọi API. Cần JavaScript hay đăng nhập thì viết script Playwright. Còn AI lái trình duyệt trực tiếp hợp nhất cho **lần đầu khám phá** hoặc việc làm một lần. AI khám phá, rồi viết công cụ, như mọi tập. |
| 3:55 | **MẸO PRO 2** — `TEXT: @browser = Claude dùng chính Chrome đang đăng nhập của bạn (extension Claude in Chrome)` | Với hệ thống nội bộ bạn đã đăng nhập sẵn trên Chrome, extension Claude in Chrome cho phép gõ a-còng browser để Claude dùng luôn trình duyệt đó, khỏi đăng nhập lại. |
| 4:08 | `⚠️ TEXT: Đọc điều khoản & robots.txt · Nghỉ giữa các lần gọi · Không thu thập dữ liệu cá nhân` | Và luôn luôn: đọc điều khoản sử dụng của website, nghỉ giữa các lần gọi, và không thu thập dữ liệu cá nhân của người khác. |
| 4:20 | Tóm tắt: `Cuộn: định nghĩa "hết"` · `Đăng nhập: người gõ, AI làm tiếp` · `Luôn tìm API trước` | |
| 4:30 | `TEXT: BÀI TẬP: mở Network trên 1 trang bạn hay tra cứu, tìm request trả về JSON` | Bài tập: mở tab Network trên một trang bạn hay tra cứu, tìm xem có request nào trả về JSON không. Bạn sẽ ngạc nhiên vì có rất nhiều. |
| 4:38 | Teaser: báo cáo "Đối thủ giảm giá 3 mặt hàng chủ lực đêm qua" hiện trên điện thoại | Thu thập một lần thì xong. Nhưng nếu bạn muốn biết **mỗi sáng** đối thủ vừa đổi giá gì? Tập sau: máy theo dõi đối thủ thay bạn. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** `Dùng WebFetch đọc https://quotes.toscrape.com/scroll và cho biết trang có bao nhiêu trích dẫn.`

**PROMPT 2**
```text
Dùng trình duyệt (Playwright) mở https://quotes.toscrape.com/scroll, cuộn xuống tới khi số trích dẫn
KHÔNG tăng thêm sau 2 lần cuộn liên tiếp (= đã hết). Lấy nội dung, tác giả, thẻ của tất cả, lưu trich-dan-scroll.xlsx, báo tổng số.
```

**PROMPT 3**
```text
Mở https://quotes.toscrape.com/login trong trình duyệt rồi DỪNG LẠI để tôi tự đăng nhập (không hỏi mật khẩu của tôi).
Khi tôi báo "xong", đi qua tất cả các trang, lấy trích dẫn kèm liên kết Goodreads của tác giả, và đếm bao nhiêu câu có liên kết.
```

**PROMPT 4**
```text
Viết thu-thap-dang-nhap.py bằng Playwright Python, dùng Microsoft Edge (channel="msedge"): mật khẩu đọc từ biến môi trường
WEB_USER/WEB_PASS; sau lần đăng nhập đầu, lưu storage_state vào phien-dang-nhap.json và dùng lại ở lần sau;
nghỉ 0,5 giây giữa các trang; tham số --hien để hiện trình duyệt. Thêm phien-dang-nhap.json vào .gitignore. Chạy thử 2 lần.
```

**PROMPT 5**
```text
Mở lại https://quotes.toscrape.com/scroll trong trình duyệt, cuộn vài lần, rồi xem các request mạng mà trang đã gửi.
Có API nào trả về dữ liệu JSON không? Nếu có, viết thu-thap-api.py dùng requests gọi thẳng API đó (nghỉ 0,5 giây/lần),
lưu trich-dan.xlsx + sheet thống kê top tác giả, in thời gian chạy.
```

## Gói đăng tải

- **Tiêu đề:** A: `Thu thập dữ liệu web nâng cao: cuộn vô hạn, đăng nhập, API ẩn | Claude nâng cao #13` · B: `Web "giấu" dữ liệu? Cửa sau API giúp nhanh hơn 20 lần`
- **Thumbnail:** Tab Network với dòng `api/quotes` phát sáng. Chữ: **"CỬA SAU"**.
- **Shorts:** (1) 0:00–0:13 "Trình duyệt thấy 100, máy thấy 0", (2) 2:40–3:18 "Tab Network: vũ khí bí mật".
