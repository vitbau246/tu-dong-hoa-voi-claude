# Phần 2: Nâng cao (tập 11–20): Nghiên cứu · Duyệt web · SEO · Cỗ máy nội dung

## 1. Định vị

Phần 1 dạy **công cụ** (Skills, Hooks, MCP, Subagents, Plugin) qua việc văn phòng. Phần 2 dùng chính những công cụ đó để giải **bài toán tăng trưởng**: tìm thông tin đáng tin, theo dõi thị trường, kéo khách từ Google, và tự động hóa cả quy trình nội dung.

| Nhóm khán giả mới | Nỗi đau | Tập phù hợp |
|---|---|---|
| Marketer / content / SEO in-house | Viết nhiều mà không lên top, quy trình đăng bài thủ công, sợ AI bịa | 15–20 |
| Chủ doanh nghiệp nhỏ, quản lý kinh doanh | Không có thời gian nghiên cứu thị trường, canh đối thủ | 11, 12, 14 |
| Chuyên viên phân tích, nghiên cứu | Tổng hợp nhiều nguồn, cần trích dẫn chính xác | 11, 12, 13 |

**Lời hứa của phần 2:** *"Không chỉ nhanh hơn, mà **tin được**."* Mọi tập đều có một cơ chế kiểm chứng: script kiểm trích dẫn, giám khảo chấm điểm, crawler đo lại, cổng duyệt của con người.

## 2. Lộ trình 3 chặng

| Chặng | Tập | Chủ đề | "Wow" đã kiểm chứng |
|---|---|---|---|
| **A. Nghiên cứu đáng tin** | 11 | Nghiên cứu có trích nguồn + kiểm chứng tự động | Bắt 3/9 trích dẫn sai, có câu giống **99,5%** vẫn sai 1 con số |
| | 12 | Đội 5 AI nghiên cứu song song (deep research) | Ma trận độ tin cậy + danh sách số liệu bị gỡ |
| **B. Web nâng cao** | 13 | Trang JS, đăng nhập, cuộn vô hạn, "cửa sau" API | 100 trích dẫn trong **7,6 giây** qua API ẩn |
| | 14 | Theo dõi đối thủ 24/7, AI chỉ chạy khi có thay đổi | 11/11 thay đổi; Claude đọc ra chiến thuật "combo giấy" của đối thủ |
| **C. SEO và nội dung** | 15 | Nghiên cứu từ khóa từ Search Console | Sửa 1 dòng tiêu đề = **+901 click** / 3 tháng |
| | 16 | Viết bài + giám khảo tự chấm, AI tự sửa | Chạy thật: **100/100**; hook trả lỗi → Claude tự sửa |
| | 17 | Đăng WordPress (bản nháp) + 4 kênh | Ảnh bìa, meta Yoast, schema FAQ, UTM bằng 1 lệnh |
| | 18 | Audit SEO kỹ thuật + tự sửa | **0 → 100/100**; 1 dòng robots.txt chặn mọi trang sản phẩm |
| | 19 | Landing page chuẩn SEO, lên mạng 15 phút | JSON-LD hợp lệ, WCAG AA, không bịa đánh giá sao |
| | 20 | Cỗ máy nội dung hằng tuần + plugin | 7 skills · 2 agents · 1 hook, cổng duyệt của con người |

## 3. Bài học kỹ thuật rút ra từ lần chạy thật (đã đưa vào kịch bản)

Đây là những điểm **chỉ phát hiện được khi chạy thật** trên Windows 10 + Claude Code 2.1.312. Mỗi điểm là chất liệu đáng tin cho video (người xem sẽ gặp đúng các lỗi này):

| # | Phát hiện | Ảnh hưởng | Cách xử lý trong series |
|---|---|---|---|
| 1 | **WebFetch tóm tắt trang bằng một model khác** ("lossy by design", theo tài liệu chính thức) | Con số có thể bị làm tròn, câu bị diễn đạt lại | Tập 11: script tải lại nguyên bản để kiểm chứng |
| 2 | WebFetch **từ chối localhost** và tên máy nội bộ | Không audit được site nội bộ bằng WebFetch | Tập 14, 18: dùng script requests/crawler |
| 3 | WebSearch **không phải** Google Việt Nam; giới hạn **200 lượt/phiên** | Thứ hạng khác; nghiên cứu lớn có thể hết lượt | Tập 15: tự lấy top 5 Google ẩn danh; tập 12: `/clear`, biến môi trường |
| 4 | Hook **PostToolUse** thoát mã 0: stdout **không** tới Claude | Claude tưởng hook "im lặng" | Tập 16: trả `hookSpecificOutput.additionalContext` |
| 5 | Trên Windows, phiên `-p` chạy lệnh bằng công cụ **PowerShell** (không có Bash), subagent là **Task** | `Bash(python *)` và agent khai `tools: Bash` không chạy được Python | Thêm `PowerShell(python *)` vào mọi skill; `PowerShell` vào mọi agent; dùng `Task` trong `--allowedTools` |
| 6 | Gọi `claude -p "/skill"` từ **Git Bash**: dấu `/` bị đổi thành đường dẫn | Không tìm thấy skill | Luôn chạy lịch bằng PowerShell |
| 7 | Máy công ty có **proxy** (`HTTP_PROXY`) | requests tới localhost bị đẩy qua proxy, nhận trang trống/503 | Bỏ proxy cho địa chỉ nội bộ (`trust_env=False` / `proxies=None`) |
| 8 | Windows PowerShell 5.1 đọc `.ps1` **không BOM** theo bảng mã ANSI | Mất dấu tiếng Việt | Mọi `.ps1` lưu UTF-8 **có BOM** |
| 9 | Python trên Windows in tiếng Việt ra console lỗi `cp1252` | Script chết ở dòng `print`/`sys.exit` | `sys.stdout/stderr.reconfigure(encoding="utf-8")` ở mọi script |
| 10 | Yoast/RankMath không cho ghi meta SEO qua REST API mặc định | Khung Yoast trống | mu-plugin `seo-meta-rest.php` (15 dòng) |

## 4. Giới hạn cần nói thật trên video

- Claude **không có** dữ liệu lượng tìm kiếm (search volume). Phải dùng Search Console / Keyword Planner / công cụ SEO.
- 100 điểm on-page hay 100 điểm kỹ thuật **không đảm bảo** lên top. Đó chỉ là điều kiện cần.
- Script kiểm chứng xác nhận "nguồn **có nói** vậy", không xác nhận điều đó **đúng**.
- Không thu thập dữ liệu cá nhân, tôn trọng điều khoản website, không gửi yêu cầu dồn dập. Tập 13 dùng trang luyện tập hợp pháp `quotes.toscrape.com`.
- Mọi thứ công khai (xuất bản bài, đăng mạng xã hội, gửi email) đều do **con người bấm nút cuối**.

## 5. Mức độ kiểm thử từng tập

| Tập | Dữ liệu / script | Chạy thật với Claude |
|---|---|---|
| 11 | ✔ kiểm chứng 6 khớp / 3 sai | Chưa (nghiên cứu web thật, kết quả mỗi lần khác): tập dượt trước khi quay |
| 12 | ✔ agent + skill đúng định dạng (validate qua plugin) | Chưa: tập dượt, ghi thời gian/chi phí |
| 13 | ✔ API 7,6 giây; Playwright đăng nhập 100/100 | Phần MCP: tập dượt |
| 14 | ✔ 11/11 thay đổi | ✔ **Bước AI chạy thật**: báo cáo đúng số liệu |
| 15 | ✔ 6 sát trang 1 · 2 CTR thấp · 1 tự cạnh tranh | Phần `/brief-seo`: tập dượt |
| 16 | ✔ 14/100 và 100/100 | ✔ **Chạy thật** `/viet-bai-seo`: 100/100; ✔ vòng phản hồi hook |
| 17 | ✔ với WordPress giả lập | Chưa thử WordPress thật: tập dượt trên staging |
| 18 | ✔ 31/31 lỗi; sửa xong 100/100, 0 báo nhầm | Phần Claude sửa: tập dượt |
| 19 | ✔ JSON-LD, WCAG AA, responsive (ảnh chụp Playwright) | Phần Claude dựng trang: tập dượt |
| 20 | ✔ plugin validate + cài cô lập (7/2/1) | Chưa chạy trọn chuỗi: **bắt buộc tập dượt** |

## 6. Lịch đăng phần 2 (tiếp nối tuần 11 của phần 1)

| Tuần | Video dài (Thứ 3, 20:00) | Ghi chú |
|---|---|---|
| 12 | Trailer phần 2 (60 giây) + Tập 11 | Trailer dùng cảnh "99,5% vẫn sai", "robots.txt", "+901 click" |
| 13–14 | Tập 12, 13 | |
| 15 | Tập 14 | Chia sẻ vào nhóm chủ shop / kinh doanh online |
| 16–19 | Tập 15–18 | **Mini-series SEO**: gom thành playlist riêng "SEO bằng AI không bịa" |
| 20 | Tập 19 | |
| 21 | Tập 20 + livestream "Dựng cỗ máy nội dung cho website của bạn" | Mời người xem gửi website để audit trực tiếp (chỉ website của chính họ) |

Shorts: mỗi tập 2 Shorts (đã chọn sẵn trong mục "Gói đăng tải" của từng kịch bản), đăng Thứ 5 và Thứ 7.
