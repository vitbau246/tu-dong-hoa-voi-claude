# Series "Tự động hóa mọi thứ với VS Code và Claude"

**20 video × 5 phút, chia 2 phần.** Mỗi tập giải quyết **một việc có thật**, dùng dữ liệu demo **gài sẵn lỗi** để Claude bắt lỗi ngay trên màn hình. Mỗi tập có kịch bản 2 cột, prompt dùng ngay, script tạo dữ liệu (reset được khi quay lại) và đáp án hoặc lời giải để đối chiếu.

- **Phần 1: Nền tảng (tập 1–10):** việc văn phòng (file, Excel, PDF, trộn thư) → Skills, Hooks, MCP, chạy theo lịch, Subagents, Plugin.
- **Phần 2: Nâng cao (tập 11–20):** nghiên cứu có kiểm chứng, duyệt web nâng cao, theo dõi đối thủ, SEO trọn quy trình (từ khóa → viết → đăng WordPress → audit → landing page) và cỗ máy nội dung hằng tuần.

> Đã đối chiếu với tài liệu chính thức và kiểm thử trên Windows 10 · VS Code 1.144 · Claude Code 2.1.312 (30/10/2026). Mức độ kiểm thử từng tập: `00-chien-luoc/05-phan-2-nang-cao.md` mục 5.

## Bắt đầu nhanh

```powershell
pip install -r requirements.txt
cd tap-01-don-dep-downloads
python chuan-bi.py          # tạo demo/ + dap-an.json (chạy lại bất cứ lúc nào để reset)
code demo                   # mở trong VS Code, làm theo kich-ban.md
```

`python chuan-bi.py --giai-phap` (tập 5 trở đi) chép thêm lời giải hoàn chỉnh (skill, hook, agent, script, plugin), dùng khi muốn quay nhanh hoặc khi Claude chạy chưa tốt.

## Phần 1: Nền tảng

| # | Tập | Việc thật | Tính năng | Khoảnh khắc "wow" (đã kiểm chứng) |
|---|---|---|---|---|
| 1 | [Dọn 300 file trong 1 phút](tap-01-don-dep-downloads/kich-ban.md) | Thư mục Downloads | Cài đặt, Plan mode, file hoàn tác | 318 file, 27 bản trùng nội dung dù khác tên |
| 2 | [Gộp 12 file Excel](tap-02-gop-excel/kich-ban.md) | Báo cáo doanh thu năm | `@`, Claude viết + chạy script | SUM thẳng ra 13,18 tỷ, số đúng 10,63 tỷ (**sai 2,55 tỷ**) |
| 3 | [30 hóa đơn PDF → Excel](tap-03-hoa-don-pdf/kich-ban.md) | Nhập liệu kế toán | Trích bằng script + kiểm tra chéo | 3 hóa đơn có vấn đề, 2 lỗi che nhau chỉ còn lệch 10.000 đ |
| 4 | [Trộn thư 40 thư mời](tap-04-tron-thu/kich-ban.md) | Thư mời, email | Hàng loạt, để AI **hỏi** khi mơ hồ | 40 thư + 37 email nháp, AI không đoán giới tính |
| 5 | [Báo cáo tuần bằng 1 lệnh](tap-05-skills-bao-cao-tuan/kich-ban.md) | Báo cáo định kỳ | CLAUDE.md + Skills | `/bao-cao-tuan 44` ra file Word đúng mẫu |
| 6 | [Phanh an toàn cho AI](tap-06-hooks-an-toan/kich-ban.md) | Sợ AI xóa nhầm | Hooks | Chế độ Auto mà vẫn bị chặn (9/9 test đạt) |
| 7 | [Claude tự lái trình duyệt](tap-07-trinh-duyet-mcp/kich-ban.md) | Thu thập web, điền form | MCP Playwright (Edge) | Từ chối bịa số điện thoại thiếu 1 chữ số |
| 8 | [Bản tin tự chạy 7:30 sáng](tap-08-tu-chay-moi-sang/kich-ban.md) | Tin tức + việc trong ngày | `claude -p` + Task Scheduler | Chạy thật 119 giây, 5/5 link tin có thật |
| 9 | [Đội 3 trợ lý AI](tap-09-subagents-doi-ai/kich-ban.md) | So sánh báo giá | Subagents | Báo giá "rẻ nhất" 189tr → thực tế 392tr |
| 10 | [Plugin cho cả team](tap-10-plugin-cho-ca-team/kich-ban.md) | Nhân rộng | Plugin + marketplace | Đồng nghiệp gõ 2 lệnh là có đủ bộ công cụ |

## Phần 2: Nâng cao

| # | Tập | Việc thật | Tính năng | Khoảnh khắc "wow" (đã kiểm chứng) |
|---|---|---|---|---|
| 11 | [Nghiên cứu không sợ bịa số](tap-11-nghien-cuu-trich-nguon/kich-ban.md) | Báo cáo thị trường | WebSearch/WebFetch + script kiểm chứng | Trích dẫn giống **99,5%** vẫn sai 1 con số, bị bắt |
| 12 | [Đội 5 AI nghiên cứu song song](tap-12-doi-nghien-cuu-song-song/kich-ban.md) | Câu hỏi chiến lược | Skill điều phối + subagents | Ma trận độ tin cậy, gỡ số không có nguồn |
| 13 | [Duyệt web nâng cao](tap-13-duyet-web-nang-cao/kich-ban.md) | Trang JS/đăng nhập/cuộn vô hạn | Playwright MCP + "cửa sau" API | 100 bản ghi trong **7,6 giây** qua API ẩn |
| 14 | [Theo dõi đối thủ 24/7](tap-14-giam-sat-doi-thu/kich-ban.md) | Canh giá đối thủ | Script + `claude -p` khi có thay đổi | 11/11 thay đổi, AI đọc ra chiến thuật "combo" |
| 15 | [Từ khóa SEO từ Search Console](tap-15-tu-khoa-seo/kich-ban.md) | Chọn bài nên viết | Phân tích CSV + `/brief-seo` | Sửa 1 dòng tiêu đề = **+901 click** |
| 16 | [Viết bài SEO, máy tự chấm, AI tự sửa](tap-16-viet-bai-chuan-seo/kich-ban.md) | Viết bài chuẩn SEO | Hook PostToolUse + `/viet-bai-seo` | **Chạy thật: 100/100**, không bịa chính sách |
| 17 | [Đăng WordPress + 4 kênh](tap-17-dang-wordpress-da-kenh/kich-ban.md) | Xuất bản đa kênh | REST API + `/da-kenh` | Bản nháp đủ ảnh bìa, Yoast, schema FAQ, UTM |
| 18 | [Audit SEO kỹ thuật & tự sửa](tap-18-audit-seo-ky-thuat/kich-ban.md) | Sức khỏe website | Crawler + sửa hàng loạt | **0 → 100/100**, 1 dòng robots.txt chặn mọi sản phẩm |
| 19 | [Landing page 15 phút](tap-19-landing-page-seo/kich-ban.md) | Trang chiến dịch | HTML + WebP + JSON-LD + Netlify Drop | WCAG AA, không bịa đánh giá sao |
| 20 | [Cỗ máy nội dung hằng tuần](tap-20-co-may-noi-dung/kich-ban.md) | Content marketing | Plugin `tro-ly-marketing` + lịch | Thứ Hai 7:00 bài đã chờ duyệt |

## Cấu trúc thư mục

```
00-chien-luoc/
  01-nghien-cuu.md              khán giả, tính năng đã xác minh, khoảng trống thị trường, nguồn
  02-cong-thuc-tap-5-phut.md    khung 5 phút, giọng điệu, ngân hàng hook
  03-ke-hoach-xuat-ban.md       lịch đăng, Shorts, SEO, KPI
  04-thiet-lap-quay.md          OBS, VS Code, quy trình quay, checklist an toàn
  05-phan-2-nang-cao.md         định vị phần 2, 10 bài học từ lần chạy thật, mức độ kiểm thử, lịch đăng phần 2
  vscode-settings-quay-phim.json
tap-XX-.../
  kich-ban.md                   kịch bản 2 cột + prompt + đối chiếu + xử lý sự cố + gói đăng tải
  chuan-bi.py                   tạo demo/ (reset được) + dap-an.json
  giai-phap/                    lời giải tham chiếu đã kiểm thử (skill, hook, agent, script, plugin)
```

## Yêu cầu

- Windows 10/11, VS Code ≥ 1.94, extension **Claude Code** (Anthropic), gói Claude **Pro/Max/Team/Enterprise** (gói Free không dùng được Claude Code).
- Python 3.10+ (`requirements.txt`). Node.js cho tập 7, 13. Microsoft Word + Outlook cho tập 4. **Claude Code CLI** cho tập 8, 10, 14, 20 (`irm https://claude.ai/install.ps1 | iex`, vì extension không thêm lệnh `claude` vào PATH).
- Tập 17, 20: site WordPress **thử nghiệm** (hoặc `wp-gia-lap.py` để tập dượt).

## Lưu ý

- Toàn bộ dữ liệu, công ty, người, mã số thuế, website trong demo là **hư cấu**. Hóa đơn có dòng "MẪU DEMO – KHÔNG CÓ GIÁ TRỊ PHÁP LÝ". Email và website dùng tên miền dành riêng `.example`. Tập 13 dùng trang luyện tập hợp pháp `quotes.toscrape.com`.
- `chuan-bi.py` chỉ xóa **nội dung bên trong** `demo/`, nên chạy được khi VS Code đang mở thư mục đó.
- Các con số `[thời gian thật]` trong kịch bản là chỗ trống. Điền theo đồng hồ của lần quay được chọn.
- **Trên Windows:** chạy `claude -p` từ PowerShell (không dùng Git Bash). Mọi `.ps1` đã lưu UTF-8 có BOM. Script đã tự xử lý proxy công ty cho địa chỉ nội bộ. Chi tiết: `00-chien-luoc/05-phan-2-nang-cao.md` mục 3.
