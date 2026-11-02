# Tập 20: Cỗ máy nội dung tự chạy mỗi tuần, bạn chỉ còn một việc: duyệt

| | |
|---|---|
| **Mục tiêu người xem** | Ghép toàn bộ phần nâng cao (tập 11–19) thành một quy trình tự chạy hằng tuần, có **cổng duyệt của con người**; đóng gói thành plugin `tro-ly-marketing` để cả phòng dùng |
| **Tính năng dạy** | Skill điều phối gọi skill khác, plugin có hook + agent + script, `claude -p "/plugin:skill"` theo lịch, quyền tối thiểu cho chạy không người giám sát, phiếu "chờ duyệt" |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/`: CLAUDE.md (bộ sự thật), san-pham.csv, `ke-hoach-noi-dung.csv` (đầu ra tập 15, việc tiếp theo: "máy hủy tài liệu"), `wp-gia-lap.py`, `chay-hang-tuan.ps1`. `--giai-phap` dựng và chép `marketplace/` (2 plugin) |
| **Đã kiểm thử** | Plugin `tro-ly-marketing`: `claude plugin validate` ✔, cài trong cấu hình cô lập: **7 skills · 2 agents · 1 hook**, khoảng 651 token cố định/phiên. Marketplace chứa cả plugin tập 10 ✔. Các mắt xích đã chạy thật ở từng tập: viết bài + hook (tập 16, 100/100), đăng bản nháp (tập 17, WordPress giả lập), kiểm chứng (tập 11). **Chưa chạy trọn chuỗi bằng một lệnh**: tập dượt `chay-hang-tuan.ps1` ít nhất 1 lần trước khi quay (khoảng 15–30 phút, ngân sách mặc định $3) |

## Chuẩn bị

1. Cài plugin (tập 10 đã hướng dẫn): `claude plugin marketplace add ./marketplace` → `claude plugin install tro-ly-marketing@van-phong-demo`. Tập dượt thì dùng `$env:CLAUDE_CONFIG_DIR` cô lập.
2. WordPress: site thử nghiệm thật, hoặc `python wp-gia-lap.py` + 3 biến `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` (xem tập 17).
3. **Tập dượt trọn chuỗi**: `powershell -ExecutionPolicy Bypass -File .\chay-hang-tuan.ps1` (PowerShell, **không** dùng Git Bash). Ghi lại thời gian, chi phí, điểm SEO để điền vào chữ trên màn hình.
4. Cảnh "Thứ 2, 7:00": `.\chay-hang-tuan.ps1 -DangKy`, rồi `Start-ScheduledTask -TaskName "Claude - Co may noi dung"` để chạy ngay khi quay.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Thứ Hai, 7:00. Thông báo Windows: "Bài tuần này đang CHỜ BẠN DUYỆT" → phiếu `cho-duyet/…-may-huy-tai-lieu.md` tự mở | Thứ Hai, bảy giờ sáng. Bài viết tuần này đã sẵn sàng, chỉ chờ mình duyệt. |
| 0:07 | Lướt phiếu: điểm SEO 9x · link bản nháp WordPress · 4 file kênh · ☐ "Chụp 2 ảnh thật", ☐ "Chọn câu mở đầu Facebook A/B", ☐ "Bấm Xuất bản" | Máy đã chọn chủ đề, nghiên cứu đối thủ, viết, tự chấm điểm, đăng bản nháp, soạn bài cho bốn kênh. Phần việc của mình là ba ô vuông: chụp hai tấm ảnh, chọn một câu mở đầu, và bấm Xuất bản. |
| 0:20 | Người dẫn | Đây là tập cuối của phần nâng cao. Chín tập vừa rồi là chín mắt xích. Hôm nay mình nối chúng thành một chuỗi, và quan trọng nhất, chỉ cho bạn **chỗ nào phải để con người đứng**. |
| 0:35 | Thanh 3 bước: `① Nối chuỗi ② Đóng gói plugin ③ Hẹn giờ + cổng duyệt` | |
| **0:38** | **① NỐI CHUỖI** — Sơ đồ 7 ô: `Kế hoạch (T15) → Brief (T15) → Viết + tự chấm (T16) → Bản nháp WP (T17) → 4 kênh (T17) → Phiếu duyệt → Cập nhật kế hoạch` | Đây là chuỗi. Mỗi ô là một tập bạn đã xem. Kế hoạch nội dung từ tập mười lăm cho biết tuần này viết gì. Brief, viết và tự chấm điểm, bản nháp WordPress, bốn kênh. Rồi một phiếu duyệt, và cập nhật lại kế hoạch. |
| 0:58 | Mở `co-may-noi-dung/SKILL.md`: zoom bước 1 "lấy dòng Chưa làm đầu tiên", bước 4 "TUYỆT ĐỐI không đổi trạng thái sang xuất bản", bước 6 "Danh sách việc NGƯỜI phải làm" | Toàn bộ chuỗi là một skill. Ba dòng quan trọng nhất: tự chọn việc tiếp theo trong kế hoạch, **tuyệt đối** không xuất bản, và phải liệt kê rõ việc gì con người cần làm. |
| 1:18 | Mở `ke-hoach-noi-dung.csv`: 2 dòng "Đã xong", dòng 3 "máy hủy tài liệu · Viết mới · Chưa làm" | Kế hoạch hiện tại: hai việc tuần một đã xong. Việc tiếp theo là bài "máy hủy tài liệu". |
| **1:28** | **② ĐÓNG GÓI** — Terminal: `python dong-goi.py` → "tro-ly-marketing (7 skills, 2 agents, 1 hook)" → `claude plugin validate` ✔ | Bước hai: đóng gói. Một script gom các skill, agent và script **đã chạy thử** ở các tập trước thành plugin "trợ-lý-marketing". Sửa ở tập gốc, đóng gói lại, cả phòng nhận bản mới. |
| 1:45 | `claude plugin details tro-ly-marketing`: Skills (7) · Agents (2) · Hooks (1) · "~651 tok" | Bảy skill, hai agent, một hook chấm điểm. Chi phí cố định khoảng sáu trăm năm mươi token mỗi phiên. Nội dung skill chỉ được nạp khi dùng tới. |
| 1:58 | Cây `marketplace/plugins/`: `tro-ly-van-phong` (tập 10) + `tro-ly-marketing` | Và nó nằm chung "chợ" với plugin văn phòng ở tập mười. Phòng hành chính cài một plugin, phòng marketing cài plugin kia, hoặc cài cả hai. |
| **2:10** | **③ HẸN GIỜ + CỔNG DUYỆT** — Mở `chay-hang-tuan.ps1`: zoom `--allowedTools "Read,Write,Edit,Glob,WebSearch,WebFetch,Skill,Task,…python…"` + `--max-budget-usd` | Bước ba: chạy không người giám sát. Chú ý danh sách quyền: đọc, ghi, tìm web, chạy đúng các script Python. **Không** có quyền nào để xuất bản hay xóa. Và có trần chi phí cho mỗi lần chạy. |
| 2:30 | `TEXT: ⚠️ Chạy từ PowerShell, KHÔNG từ Git Bash` | Một lỗi mình đã vấp khi làm series: gọi lệnh có dấu gạch chéo từ Git Bash thì Git Bash tự đổi nó thành đường dẫn thư mục, và Claude không tìm thấy skill. Hãy chạy từ PowerShell. |
| 2:42 | `.\chay-hang-tuan.ps1 -DangKy` → "Đã hẹn: Thứ 2 lúc 7:00" → `Start-ScheduledTask` → `[TUA x30]` đồng hồ thật góc màn hình | Hẹn giờ thứ Hai bảy giờ sáng. Để quay video, mình bấm chạy ngay. Và tua nhanh. |
| 3:00 | Montage tua nhanh: `brief/may-huy-tai-lieu.md` xuất hiện → `bai-viet/…md` → `.claude/nhat-ky-cham-diem.csv` (8x → 9x) → bản nháp trên WordPress → `da-kenh/…` 5 file → `cho-duyet/…md` | Brief. Bài viết. Giám khảo chấm, chưa đạt, sửa, đạt. Bản nháp lên WordPress. Bốn kênh. Phiếu duyệt. |
| 3:15 | Mở WordPress: bài ở trạng thái **Bản nháp** · khung cam "ẢNH CẦN CHỤP" | Trên WordPress: bản nháp, kèm hai khung cam chờ ảnh thật. |
| 3:25 | `ke-hoach-noi-dung.csv`: dòng "máy hủy tài liệu" → "Chờ duyệt" | Kế hoạch tự cập nhật. Tuần sau, cỗ máy sẽ tự lấy việc tiếp theo. |
| **3:35** | **MẸO PRO: vì sao phải có cổng duyệt** — 3 thẻ: `📸 Ảnh thật & kinh nghiệm thật: AI không có` · `⚖️ Trách nhiệm pháp lý: thuộc về người đăng` · `🎯 Google ưu tiên nội dung "người thật, việc thật"` | Vì sao không để máy tự xuất bản luôn cho nhanh? Ba lý do. Ảnh thật và kinh nghiệm thật là thứ AI không có, mà Google đánh giá rất cao. Trách nhiệm pháp lý của bài đăng thuộc về **người** đăng. Và một bài có người đọc lại luôn tốt hơn bài không ai đọc. |
| 4:00 | `TEXT: Chi phí thật = [chi phí lần tập dượt]/tuần` · `So với: 1 buổi làm việc của 1 người` | Chi phí mỗi tuần, mình đo khi tập dượt, là con số trên màn hình. So với nửa ngày công của một người, bạn tự tính. |
| 4:12 | Tổng kết phần nâng cao: dựng nhanh 10 cảnh wow tập 11–20 (2 giây/cảnh) | Nhìn lại phần nâng cao: bắt AI bịa số, đội nghiên cứu năm người, cửa sau API, canh đối thủ hai bốn trên bảy, mỏ vàng Search Console, giám khảo tự chấm, đăng WordPress một lệnh, robots.txt chết người, landing page mười lăm phút, và cỗ máy hôm nay. |
| 4:35 | Người dẫn | Hai mươi tập, một ý xuyên suốt: để máy làm phần lặp lại, giữ phần cần suy nghĩ và chịu trách nhiệm cho con người. |
| 4:45 | Màn hình kết (bản đặc biệt): link repo file mẫu + playlist 2 phần | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. Hẹn gặp bạn ở phần tiếp theo. |

## Lệnh dùng trong tập

```powershell
python giai-phap\dong-goi.py                      # (từ thư mục tập 20) dựng marketplace 2 plugin
claude plugin validate .\marketplace
claude plugin marketplace add .\marketplace
claude plugin install tro-ly-marketing@van-phong-demo
.\chay-hang-tuan.ps1                              # chạy tay 1 lần (tập dượt)
.\chay-hang-tuan.ps1 -DangKy                      # hẹn Thứ 2, 7:00
Start-ScheduledTask -TaskName "Claude - Co may noi dung"
```

Hoặc gọi trong VS Code: `/tro-ly-marketing:co-may-noi-dung` (có thể kèm từ khóa).

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| "Không tìm thấy skill" khi chạy theo lịch | Plugin cài ở phạm vi user trên **đúng tài khoản Windows** chạy Task Scheduler. Kiểm tra `claude plugin list` |
| Subagent / Python bị từ chối khi chạy `-p` | Trên Windows, công cụ chạy lệnh là `PowerShell` và công cụ subagent là `Task`. Danh sách `--allowedTools` trong script đã có đủ |
| Vượt ngân sách giữa chừng | Tăng `-NganSach`, hoặc tách: chạy brief + viết vào Thứ 2, đăng + đa kênh vào Thứ 3 |
| Bài viết lặp chủ đề cũ | Kiểm tra `ke-hoach-noi-dung.csv` đã được cập nhật "Chờ duyệt" chưa. Nếu không, xem `cho-duyet/nhat-ky-chay.txt` |

## Gói đăng tải

- **Tiêu đề:** A: `Cỗ máy nội dung tự chạy mỗi tuần: bạn chỉ việc bấm duyệt | Claude nâng cao #20` · B: `Từ 9 công cụ thành 1 quy trình: tự động hóa content marketing có cổng duyệt`
- **Thumbnail:** Băng chuyền 7 ô, ô cuối là bàn tay bấm nút "Duyệt". Chữ: **"BẠN CHỈ VIỆC DUYỆT"**.
- **Shorts:** (1) 0:00–0:20 "Thứ Hai 7 giờ: bài đã chờ sẵn", (2) 3:35–4:00 "3 lý do không để AI tự xuất bản".
