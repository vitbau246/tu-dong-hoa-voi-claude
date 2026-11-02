# Tập 7: Cho Claude tự lái trình duyệt: thu thập dữ liệu web và điền form (MCP)

| | |
|---|---|
| **Mục tiêu người xem** | Hiểu MCP là gì, kết nối Claude với trình duyệt, tự động thu thập dữ liệu nhiều trang và điền form hàng loạt |
| **Tính năng dạy** | MCP server (Playwright), file `.mcp.json` (phạm vi dự án), `/mcp`, phê duyệt server, chụp ảnh màn hình làm bằng chứng |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/web/` (website "Văn phòng phẩm An Phát" hư cấu: 28 sản phẩm / 3 trang + form đăng ký đại lý) và `demo/dai-ly.xlsx` (5 đại lý, 1 số điện thoại sai) |
| **Đã kiểm thử** | Thu thập 3 trang bằng Playwright + Microsoft Edge: đủ 28 sản phẩm. Form: số hợp lệ → mã DL-2026-1001, số `09123 4567` → bị từ chối |
| **Con số chốt** | 28 sản phẩm · 5 khuyến mãi (hiện 2 giá) · 1 giá "Liên hệ" · 3 hết hàng · 2 sắp hết · 4/5 đại lý đăng ký thành công |

## Chuẩn bị

1. `python chuan-bi.py`, sau đó mở `tap-07-trinh-duyet-mcp/demo` trong VS Code.
2. Cần **Node.js** (để chạy `npx`). Trình duyệt dùng **Microsoft Edge** có sẵn trên Windows, không cần cài thêm.
3. Mở terminal trong VS Code (`` Ctrl+` ``) và chạy web: `python -m http.server 8000 -d web`. Kiểm tra http://localhost:8000.
4. Chạy thử trước một lần `npx -y @playwright/mcp@latest --version` để npm tải sẵn gói (tránh chờ khi quay).
5. Nếu cần bỏ qua bước cài: `python chuan-bi.py --giai-phap` để có sẵn `.mcp.json`.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Màn hình chia đôi: trái là VS Code, phải là Edge **tự** cuộn trang, bấm "Trang sau →", rồi tự gõ vào form. Chuột nằm yên. `TEXT: Không chạm chuột` | Mình không chạm vào chuột. Trình duyệt đang tự chạy. |
| 0:06 | Edge hiện "✅ Đăng ký thành công! Mã DL-2026-1001" | Nó vừa đọc hết ba trang sản phẩm, rồi tự điền form đăng ký cho năm đại lý. |
| 0:12 | Người dẫn | Sáu tập trước, Claude chỉ làm việc với file trên máy bạn. Hôm nay mình mở cho nó một cánh cửa ra thế giới bên ngoài, gọi là **MCP**. Và cuối video, Claude sẽ làm một việc mà nhiều người, và nhiều AI, làm sai: **từ chối tự sửa** dữ liệu khi không chắc chắn. |
| 0:28 | Thanh 3 bước: `① Cắm MCP ② Thu thập dữ liệu ③ Điền form` | |
| **0:32** | **① CẮM MCP** — Hình ổ cắm USB: Claude ↔ `[Trình duyệt]` `[Gmail]` `[Database]` `[Jira]`... | MCP giống cổng USB cho AI. Mỗi "thiết bị" cắm vào, như trình duyệt, email, cơ sở dữ liệu, cho Claude thêm một bộ công cụ mới. Hôm nay mình cắm **Playwright**, công cụ điều khiển trình duyệt của Microsoft. |
| 0:50 | Dán PROMPT 1 → Claude tạo `.mcp.json`. Zoom: `"command": "npx"`, `"@playwright/mcp@latest"`, `"--browser", "msedge"` | Mình nhờ Claude tự tạo file cấu hình. File này nói: khi cần trình duyệt, hãy chạy Playwright, dùng Edge có sẵn trên Windows. File nằm trong dự án, nên đồng nghiệp mở thư mục này cũng có ngay. |
| 1:05 | Mở cuộc trò chuyện mới → hộp thoại hỏi phê duyệt server `playwright` → Cho phép. Gõ `/mcp` → `playwright ✔ connected` | Mở phiên mới. Claude hỏi: có tin server này không? Đây là bước an toàn: MCP từ dự án luôn phải được bạn duyệt. Đồng ý, gõ /mcp, đã kết nối. |
| 1:20 | `⚠️ TEXT: Chỉ cài MCP từ nguồn bạn tin cậy` | Nguyên tắc: chỉ cài MCP từ nguồn bạn tin. Nó chạy với quyền của chính bạn trên máy. |
| **1:28** | **② THU THẬP DỮ LIỆU** — Edge với localhost:8000: lưới sản phẩm, có giá gạch ngang, có "Liên hệ" | Đây là website demo mình dựng: ba trang sản phẩm. Có sản phẩm giảm giá hiện hai mức giá, có sản phẩm "liên hệ", có sản phẩm hết hàng. |
| 1:40 | Dán PROMPT 2 → Edge tự mở, đọc trang 1, bấm "Trang sau →", trang 2, trang 3 `[TUA x4]` | Mình yêu cầu: đi hết các trang, lấy mọi sản phẩm vào Excel. Và để ý: mình **không** chỉ cho nó nút "Trang sau" ở đâu. Nó tự nhìn trang và tự tìm. |
| 2:00 | Mở `san-pham-an-phat.xlsx`: 28 dòng. Highlight: cột Giá gốc / Giá bán / % giảm. Dòng máy chiếu: Giá = trống, Ghi chú = "Liên hệ". 3 dòng hết hàng tô xám | Hai mươi tám sản phẩm. Hàng giảm giá được tách thành giá gốc và giá bán, kèm phần trăm giảm. Máy chiếu ghi "liên hệ", **không** bị ghi thành số không. Nếu ghi số không, giá trung bình của bạn sẽ sai ngay. |
| 2:20 | `TEXT: 3 trang · 28 sản phẩm · [thời gian thật]` | Ba trang, hai mươi tám sản phẩm, chưa tới một phút. Với website hai trăm trang, công thức vẫn y hệt. |
| **2:30** | **③ ĐIỀN FORM** — Mở `dai-ly.xlsx` (5 dòng). Dán PROMPT 3 | Việc thứ hai, thứ mà dân văn phòng ghét nhất: nhập dữ liệu từ Excel vào một form trên web. Năm đại lý, mỗi người sáu ô. |
| 2:45 | Edge tự điền từng ô, chọn dropdown, bấm Gửi, hiện ✅, chụp ảnh `[TUA x4]`. Đại lý 4: ❌ "Số điện thoại không hợp lệ" | Nó điền, chọn tỉnh, chọn doanh số, bấm gửi, chụp ảnh màn hình xác nhận làm bằng chứng. Đại lý thứ tư: lỗi. |
| 3:05 | Khung chat: *"Cảng Xanh: SĐT '09123 4567' chỉ có 9 chữ số. Tôi không tự thêm số vì không biết số đúng. Bạn cần xác nhận lại với đại lý."* `SFX: ding` | Đây là khoảnh khắc mình hứa. Số điện thoại chỉ có chín chữ số. Claude **không** đoán thêm một số để form chấp nhận. Nó dừng lại và báo mình. Một AI "chăm chỉ" quá mức sẽ bịa số để hoàn thành nhiệm vụ, và đó là loại lỗi nguy hiểm nhất. |
| 3:30 | Edge mở trang "Đại lý đã đăng ký": 4 dòng. Thư mục `anh-chup/`: 5 ảnh | Kiểm tra chéo: trang danh sách có đúng bốn đại lý. Năm ảnh chụp lưu trong thư mục, gồm cả ảnh lỗi. |
| **3:42** | **MẸO PRO 1** — `TEXT: Việc lặp lại hằng ngày → bảo Claude VIẾT SCRIPT Playwright` | Mẹo một: nếu việc này lặp lại mỗi ngày, đừng để Claude lái trình duyệt mỗi lần. Hãy bảo nó **viết một script** Playwright. Chạy nhanh hơn, miễn phí, và lần nào cũng giống nhau. Vẫn là bài học của tập hai: AI viết công cụ, bạn dùng mãi. |
| 4:00 | **MẸO PRO 2** — `TEXT: @browser = dùng chính Chrome đã đăng nhập của bạn` | Mẹo hai: cần làm việc trên trang đã đăng nhập, như hệ thống nội bộ? Extension **Claude in Chrome** cho phép gõ a-còng browser để Claude dùng chính trình duyệt của bạn. |
| 4:12 | `⚠️ TEXT: Chỉ thu thập dữ liệu web bạn được phép · Tôn trọng điều khoản website · Không gửi dồn dập` | Và nhớ: chỉ thu thập dữ liệu từ trang bạn được phép, tôn trọng điều khoản của website, và đừng gửi yêu cầu dồn dập. Muốn luyện tập trên web thật thì có trang **books.toscrape.com**, được làm riêng cho việc này. |
| 4:28 | Tóm tắt: `MCP = cổng USB cho AI` · `Thu thập: nói RÕ cách xử lý trường hợp đặc biệt` · `Điền form: chụp ảnh + không tự sửa dữ liệu` | |
| 4:35 | Teaser: đồng hồ 7:30 sáng, màn hình máy tính sáng lên, bản tin đã nằm sẵn | Tập sau: mình đi ngủ. Bảy giờ rưỡi sáng, máy tính tự chạy Claude, tự đọc tin, tự soạn bản tin cho mình. Không cần mở VS Code. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (cắm MCP)
```text
Tạo file .mcp.json ở thư mục gốc dự án để kết nối MCP server Playwright:
lệnh npx, gói @playwright/mcp@latest, dùng trình duyệt Microsoft Edge (--browser msedge),
lưu ảnh chụp vào thư mục anh-chup (--output-dir anh-chup).
```

**PROMPT 2** (thu thập dữ liệu; web đang chạy ở localhost:8000)
```text
Dùng trình duyệt mở http://localhost:8000, đi qua TẤT CẢ các trang sản phẩm (bấm "Trang sau" đến hết).
Lưu vào san-pham-an-phat.xlsx các cột: Mã | Tên | Giá gốc | Giá bán | % giảm | Tình trạng | Số sao | Số đánh giá.
Quy tắc: sản phẩm giảm giá thì tách giá gốc và giá bán; giá "Liên hệ" thì để trống giá và ghi chú "Liên hệ"
(KHÔNG ghi 0); tô xám dòng hết hàng. Cuối cùng báo: tổng số sản phẩm, số hết hàng, giá bán trung bình.
```

**PROMPT 3** (điền form)
```text
Với mỗi đại lý trong @dai-ly.xlsx, mở http://localhost:8000/dang-ky-dai-ly.html, điền form và bấm Gửi.
Sau mỗi lần gửi, chụp ảnh màn hình kết quả. Nếu form báo lỗi: KHÔNG tự sửa dữ liệu, ghi lại lỗi và chuyển sang đại lý tiếp theo.
Cuối cùng mở trang "Đại lý đã đăng ký" để đối chiếu, rồi báo cáo: thành công bao nhiêu, mã đăng ký từng đại lý, lỗi gì cần tôi xử lý.
```

## Đối chiếu (dap-an.json)

- 28 sản phẩm / 3 trang. Hết hàng (3): Bút dạ quang Stabilo, Máy in đa năng Brother, Tủ hồ sơ sắt.
- Khuyến mãi (5): ví dụ Bút bi Thiên Long 72.000 → 58.000 đ. Giá "Liên hệ": Máy chiếu Epson EB-X51.
- Giá bán trung bình (27 sản phẩm có giá): xem `gia_trung_binh_cac_sp_co_gia`.
- Đăng ký: 4 thành công (DL-2026-1001 … 1004), 1 thất bại (Đại lý Cảng Xanh Demo, SĐT 9 chữ số).

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| `/mcp` báo `✘ Failed to connect` trên Windows | Đổi cấu hình thành `"command": "cmd", "args": ["/c", "npx", "-y", "@playwright/mcp@latest", "--browser", "msedge"]` |
| Không có Edge / muốn dùng Chrome | Bỏ `--browser msedge` (mặc định là Chrome) |
| Không thấy hộp thoại phê duyệt server | Mở cuộc trò chuyện mới. Nếu lỡ từ chối trước đó, chạy `claude mcp reset-project-choices` (cần CLI) |
| Danh sách đại lý trống sau khi khởi động lại trình duyệt | Danh sách lưu trong localStorage của phiên trình duyệt. Chạy lại bước điền form trong cùng phiên |

## Gói đăng tải

- **Tiêu đề:**
  - A: `Claude tự lái trình duyệt: thu thập dữ liệu + điền form hàng loạt (MCP) | Tự động hóa với Claude #7`
  - B: `Không chạm chuột: AI tự nhập 5 form web và biết từ chối bịa dữ liệu`
- **Thumbnail:** Edge với con trỏ "ma" tự di chuyển. Chữ: **"KHÔNG CHẠM CHUỘT"**.
- **Shorts:** (1) 0:00–0:12 + 2:45–3:05 "Trình duyệt tự điền form", (2) 3:05–3:30 "AI không bịa số điện thoại".
- **Bình luận ghim:** 3 prompt + `.mcp.json` + "Bạn muốn AI tự điền form nào nhất?"
