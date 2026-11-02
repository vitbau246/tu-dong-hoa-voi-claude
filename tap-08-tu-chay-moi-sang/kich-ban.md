# Tập 8: Máy tự làm bản tin lúc 7:30 sáng, khi bạn còn đang ngủ

| | |
|---|---|
| **Mục tiêu người xem** | Chạy Claude **không cần mở VS Code**: một lệnh, một script, một lịch hẹn giờ |
| **Tính năng dạy** | `claude -p` (chế độ không giao diện), `--allowedTools` (quyền tối thiểu), `--max-budget-usd`, Windows Task Scheduler. Nhắc thêm Cloud routines (`/schedule`) và `/loop` |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/cong-viec.csv` (9 việc, **hạn tính theo ngày chạy script**: luôn có 2 việc quá hạn + 4 việc trong 3 ngày tới). `--giai-phap` chép `ban-tin-sang.ps1`, `dang-ky-lich.ps1` |
| **Đã kiểm thử (30/10/2026)** | Chạy thật `ban-tin-sang.ps1` mất **119 giây**: 5 tin (5/5 link có thật trong RSS), 2 quá hạn, 4 sắp đến hạn. `dang-ky-lich.ps1` đăng ký được không cần quyền admin (đã gỡ sau khi thử). Bản tin mẫu: `giai-phap/ket-qua-mau/ban-tin-mau.html` |

## Chuẩn bị

1. **Cài Claude Code CLI** (extension VS Code **không** thêm lệnh `claude` vào PATH): PowerShell → `irm https://claude.ai/install.ps1 | iex` → mở terminal mới → `claude --version` → chạy `claude` một lần để đăng nhập.
2. `python chuan-bi.py` **ngay trong ngày quay** (để hạn công việc khớp ngày), sau đó mở `tap-08-tu-chay-moi-sang/demo` trong VS Code.
3. Cảnh mở đầu "7:30 sáng": quay thật bằng cách đăng ký lịch cho 2 phút sau (`.\dang-ky-lich.ps1 -Gio "9:02am"`), hoặc dựng lại bằng `Start-ScheduledTask`.
4. Sau khi quay: `Unregister-ScheduledTask -TaskName "Claude - Ban tin sang" -Confirm:$false`.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Đồng hồ điện thoại 7:30, chuông reo. Cắt sang laptop vừa mở nắp: góc phải hiện thông báo "Bản tin sáng 30/10/2026 đã sẵn sàng", trình duyệt đang mở bản tin | Bảy giờ rưỡi sáng. Mình vừa mở máy, và bản tin đã nằm sẵn đó. |
| 0:07 | Cuộn bản tin trên điện thoại (hoặc khung mobile): 5 tin + tóm tắt · ô đỏ "Quá hạn 2 ngày" · ô cam · "Việc nên làm đầu tiên hôm nay" | Năm tin kinh doanh, công nghệ đáng đọc, tóm tắt hai câu. Hai việc quá hạn tô đỏ. Bốn việc sắp đến hạn. Và một gợi ý: việc nên làm đầu tiên hôm nay. |
| 0:18 | Người dẫn | Không ai bấm nút nào cả. Không mở VS Code, không gõ prompt. Hôm nay mình biến Claude từ trợ lý **chờ bạn ra lệnh** thành trợ lý **tự làm việc theo lịch**. |
| 0:30 | Thanh 3 bước: `① Claude không cần cửa sổ ② Viết kịch bản ③ Hẹn giờ` | |
| **0:33** | **① CLAUDE KHÔNG CẦN CỬA SỔ** — Terminal PowerShell: `irm https://claude.ai/install.ps1 \| iex` `[TUA x4]` → `claude --version` | Trước tiên cài Claude dạng dòng lệnh. Lưu ý: extension VS Code **không** tự cài lệnh này, nên bạn cần chạy một dòng cài đặt. |
| 0:48 | Gõ: `claude -p "Đọc cong-viec.csv, việc nào đã quá hạn?" --allowedTools Read` → câu trả lời in ngay trong terminal | Giờ là phép màu: claude, gạch ngang p, rồi câu hỏi. Không cửa sổ chat. Claude đọc file, trả lời ngay trong terminal, rồi thoát. Lệnh nào chạy được trong terminal thì máy tự chạy được. |
| 1:05 | Zoom `--allowedTools Read`. `TEXT: Chỉ cho phép ĐỌC` | Chú ý phần cuối: gạch-gạch allowed-tools Read. Mình chỉ cho phép Claude **đọc**. Khi chạy tự động không có ai ngồi canh, nguyên tắc số một là: cho đúng quyền cần thiết, không hơn. |
| **1:18** | **② VIẾT KỊCH BẢN** — Quay lại khung chat VS Code, dán PROMPT 1 | Bước hai. Mình nhờ Claude trong VS Code viết một script PowerShell: gọi Claude để đọc tin từ RSS của VnExpress, đọc danh sách việc, xuất bản tin HTML rồi bật thông báo. |
| 1:35 | Claude tạo `ban-tin-sang.ps1`. Zoom 3 điểm: (1) here-string chứa yêu cầu, (2) `--allowedTools "Read,Write,WebFetch(domain:vnexpress.net)"`, (3) `--max-budget-usd 1` | Ba điểm đáng chú ý. Một: yêu cầu được viết sẵn trong script. Hai: quyền chỉ gồm đọc, ghi, và truy cập **đúng một tên miền** vnexpress.net, không trang nào khác. Ba: giới hạn chi phí mỗi lần chạy. |
| 1:58 | Terminal: `powershell -ExecutionPolicy Bypass -File .\ban-tin-sang.ps1` → đồng hồ góc chạy thật `[TUA x10]` → trình duyệt mở bản tin + thông báo | Chạy thử bằng tay. Khoảng hai phút. Xong. Trình duyệt tự mở, thông báo hiện lên. |
| 2:15 | Mở `ban-tin\nhat-ky.txt` | Mỗi lần chạy đều ghi lại vào nhật ký: lúc nào, mất bao lâu, kết quả ra sao. Có lỗi thì xem ở đây. |
| 2:25 | Bấm vào 1 link trong bản tin → mở đúng bài VnExpress | Kiểm tra: link mở ra bài thật. Trong yêu cầu mình có ghi "không bịa tin, chỉ dùng tin có trong RSS". Lần mình chạy thử, năm trên năm link đều có thật. |
| **2:40** | **③ HẸN GIỜ** — Dán PROMPT 2 → Claude tạo `dang-ky-lich.ps1` → chạy | Bước ba: hẹn giờ. Mình nhờ Claude viết thêm script đăng ký với **Task Scheduler** của Windows: bảy giờ rưỡi sáng, thứ Hai đến thứ Sáu. Không cần quyền quản trị. |
| 2:58 | Mở Task Scheduler (Win → "Task Scheduler") → thấy "Claude - Ban tin sang", Trigger: Weekly Mon–Fri 7:30 | Mở Task Scheduler để kiểm tra: đã có lịch. |
| 3:08 | Zoom tab Settings: ☑ "Run task as soon as possible after a scheduled start is missed" | Còn chi tiết hay nhất: nếu bảy rưỡi máy đang tắt, tác vụ sẽ chạy bù **ngay khi bạn bật máy**. Đó chính là cảnh đầu video. |
| 3:20 | `Start-ScheduledTask -TaskName "Claude - Ban tin sang"` → thông báo hiện ra sau ~2 phút `[TUA]` | Muốn thử ngay không cần đợi sáng mai: một lệnh Start, và nó chạy luôn. |
| **3:32** | **MẸO PRO** — Bảng 3 lựa chọn: `Task Scheduler (máy bạn, cần bật máy, đọc được file)` · `Cloud routines /schedule (chạy trên cloud, máy tắt vẫn chạy, không đọc file máy)` · `/loop (chỉ khi phiên đang mở)` | Ba cách hẹn giờ, chọn cho đúng. Task Scheduler: chạy trên máy bạn, đọc được file, nhưng máy phải bật. **Cloud routines**: chạy trên đám mây của Anthropic, tắt máy vẫn chạy, nhưng không đọc được file trên máy. Còn lệnh /loop chỉ chạy khi cửa sổ Claude còn mở, hợp với những việc canh chừng ngắn. |
| 4:00 | Ý tưởng hiện lần lượt: `Thứ 2 7:00: chạy gop_bao_cao.py (tập 2)` · `Mỗi tối: quét hóa đơn mới (tập 3)` · `Thứ 6 16:00: /bao-cao-tuan (tập 5)` | Và giờ bạn ghép được mọi thứ đã học: sáng thứ Hai tự gộp báo cáo doanh thu, mỗi tối tự quét hóa đơn mới, chiều thứ Sáu tự gọi lệnh báo-cáo-tuần. Chế độ gạch-p chạy được cả skill của bạn. |
| 4:20 | `⚠️ TEXT: Mỗi lần chạy dùng hạn mức gói Claude của bạn · Đặt --max-budget-usd` | Lưu ý: mỗi lần chạy đều dùng hạn mức gói Claude của bạn. Đặt lịch vừa phải, và luôn có giới hạn chi phí. |
| 4:30 | `TEXT: BÀI TẬP: 1 việc bạn muốn có sẵn mỗi sáng → claude -p → Task Scheduler` | Bài tập: nghĩ một thứ bạn muốn có sẵn mỗi sáng, rồi làm đúng ba bước hôm nay. |
| 4:38 | Teaser: 3 khung chat chạy song song, 3 báo giá, bảng so sánh | Tập sau: mình không thuê một trợ lý, mình thuê **cả một đội**. Ba AI làm song song, mổ xẻ ba báo giá, và phát hiện phương án "rẻ nhất" thực ra đắt nhất. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**Lệnh terminal (bước 1)**
```powershell
irm https://claude.ai/install.ps1 | iex
claude --version
claude -p "Đọc cong-viec.csv, việc nào đã quá hạn so với hôm nay?" --allowedTools Read
```

**PROMPT 1** (viết script)
```text
Viết script PowerShell 5.1 ban-tin-sang.ps1 (lưu UTF-8 có BOM) để:
1. Gọi claude -p với yêu cầu: hôm nay là <ngày>; đọc RSS https://vnexpress.net/rss/kinh-doanh.rss và
   https://vnexpress.net/rss/khoa-hoc-cong-nghe.rss, chọn 5 tin đáng chú ý cho dân văn phòng (tiêu đề, 2 câu tóm tắt, link);
   đọc cong-viec.csv, liệt kê việc quá hạn (đỏ) và đến hạn trong 3 ngày (cam); thêm 'việc nên làm đầu tiên'.
   Xuất một file HTML đẹp, đọc tốt trên điện thoại: ban-tin/<yyyy-MM-dd>.html. Không bịa tin.
2. Chỉ cấp quyền: --allowedTools "Read,Write,WebFetch(domain:vnexpress.net)", --max-budget-usd 1.
3. Tự tìm claude.exe (PATH hoặc %USERPROFILE%\.local\bin), ghi nhật ký vào ban-tin/nhat-ky.txt,
   mở file HTML và hiện thông báo Windows khi xong.
Lưu ý PowerShell 5.1: không dùng dấu nháy kép bên trong chuỗi yêu cầu; đặt [Console]::OutputEncoding = UTF8.
```

**PROMPT 2** (hẹn giờ)
```text
Viết dang-ky-lich.ps1 đăng ký Windows Task Scheduler chạy ban-tin-sang.ps1 lúc 7:30 sáng Thứ 2–Thứ 6,
cửa sổ ẩn, chạy bù khi máy bật lại nếu lỡ giờ (StartWhenAvailable), giới hạn 15 phút, không cần quyền admin.
In ra lần chạy tới. Ghi chú cách thử ngay và cách gỡ bỏ ở đầu file.
```

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| `claude` không nhận lệnh | Mở terminal **mới** sau khi cài. Hoặc truyền `-Claude "C:\Users\<tên>\.local\bin\claude.exe"` |
| Bản tin lỗi font / mất dấu | File `.ps1` thiếu BOM. Trong VS Code: Save with Encoding → UTF-8 with BOM |
| Task chạy nhưng không có bản tin | Xem `ban-tin\nhat-ky.txt`. Thường do chưa đăng nhập: chạy `claude` một lần trong terminal để đăng nhập |
| Chạy theo lịch không hiện thông báo | Tắt Focus Assist. Task phải chạy ở chế độ "Run only when user is logged on" (mặc định của script) |

## Gói đăng tải

- **Tiêu đề:**
  - A: `Máy tính tự làm bản tin lúc 7:30 sáng: claude -p + Task Scheduler | Tự động hóa với Claude #8`
  - B: `Trợ lý AI làm việc cả khi bạn ngủ (không cần mở VS Code)`
- **Thumbnail:** Đồng hồ 7:30 + laptop sáng màn hình bản tin. Chữ: **"TỰ CHẠY LÚC 7:30"**.
- **Shorts:** (1) 0:48–1:18 "Claude không cần cửa sổ chat", (2) 3:32–4:00 "3 cách hẹn giờ AI".
- **Bình luận ghim:** link tải 2 script + "Bạn muốn sáng nào cũng có sẵn cái gì?"
