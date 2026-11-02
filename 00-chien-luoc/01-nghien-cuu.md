# Nghiên cứu series "Tự động hóa mọi thứ với VS Code và Claude"

> Cập nhật: 30/10/2026 · Phiên bản Claude Code đã đối chiếu: 2.1.312 (extension VS Code `anthropic.claude-code`)

## 1. Khán giả mục tiêu

| Nhóm | Mô tả | Nỗi đau chính | Tập phù hợp |
|---|---|---|---|
| **A. Dân văn phòng "biết dùng máy tính"** (ưu tiên số 1) | Kế toán, hành chính, nhân sự, kinh doanh, chuyên viên tổng hợp. Dùng Excel/Word hằng ngày, chưa từng lập trình | Gộp file, nhập liệu từ PDF, trộn thư, báo cáo tuần/tháng lặp lại | 1–5, 7, 8 |
| **B. Kỹ sư / IT nội bộ / dev junior** | Đã dùng VS Code, biết chút script | Muốn tự động hóa quy trình nhóm, chuẩn hóa, chia sẻ công cụ | 5–10 |
| **C. Trưởng nhóm / quản lý** | Ra quyết định, cần phân tích nhanh | So sánh phương án, đọc nhiều tài liệu, nhân bản cách làm cho cả team | 9, 10 |

**Insight cốt lõi:** Khán giả không cần "AI viết code". Họ cần **lấy lại 3–5 giờ mỗi tuần** khỏi các việc lặp lại. Vì vậy mỗi tập phải bán **kết quả** (thời gian tiết kiệm, lỗi được bắt), chứ không bán tính năng.

## 2. Vì sao chọn "VS Code + Claude Code" cho dân văn phòng

- **Claude làm việc trực tiếp trên file trong máy** (đọc, tạo, sửa, chạy script). Đây là khác biệt lớn nhất so với chat trên web: không phải copy-paste, không bị giới hạn ở một file đính kèm.
- **VS Code miễn phí và quen thuộc** với dân IT. Với dân văn phòng, nó là "File Explorer có thêm trợ lý": cây thư mục bên trái, Claude bên phải.
- **Có cơ chế an toàn rõ ràng để dạy:** chế độ Plan (duyệt kế hoạch trước), Manual (hỏi trước mỗi thao tác), tua lại (rewind) các thay đổi file và hooks chặn lệnh nguy hiểm. Đây là điểm khiến người xem dám thử.
- **Lộ trình nâng cấp tự nhiên:** gõ prompt → lưu thành Skill → tự chạy theo lịch → đóng gói thành Plugin cho cả team. Chính lộ trình này là xương sống của series.

## 3. Tính năng đã xác minh (tài liệu chính thức code.claude.com, 10/2026)

| Tính năng | Chi tiết chính xác dùng trong kịch bản |
|---|---|
| Cài extension | `Ctrl+Shift+X` → tìm "Claude Code" (publisher Anthropic) → Install. Cần VS Code ≥ 1.94 và gói Claude trả phí (Pro/Max/Team/Enterprise) hoặc tài khoản Console. Gói Free **không** dùng được Claude Code |
| Mở Claude | Biểu tượng tia lửa (Spark) góc trên phải editor, hoặc **✻ Claude Code** ở thanh trạng thái, hoặc `Ctrl+Esc` |
| Chế độ quyền | **Auto**, **Manual** (hỏi trước khi sửa/chạy lệnh), **Plan** (lập kế hoạch, chờ duyệt), **Edit automatically**. Đổi ở chỉ báo dưới ô nhập. Có lệnh `/plan` |
| Rewind | Rê chuột lên tin nhắn → nút rewind: *Fork conversation from here* / *Rewind code to here* / *Fork conversation and rewind code*. ⚠️ **Chỉ khôi phục các thay đổi file mà Claude sửa bằng công cụ sửa file.** Lệnh shell (di chuyển, xóa file) **không** được khôi phục. Vì vậy tập 1 dạy thêm mẹo "file hoàn tác" |
| @-mention | `@ten-file`, `@thu-muc/`, `Alt+K` chèn tham chiếu kèm số dòng, `@terminal:ten`, `@browser` (cần extension Claude in Chrome) |
| CLAUDE.md | File ghi nhớ ngữ cảnh dự án, được nạp mỗi phiên |
| Skills | `.claude/skills/<ten>/SKILL.md` (dự án) hoặc `~/.claude/skills/...` (cá nhân). Frontmatter: `name`, `description`, `argument-hint`, `disable-model-invocation`, `allowed-tools`. Gọi bằng `/ten`; `$ARGUMENTS`, `$0`, `$1`. Thư mục `.claude/commands/` cũ vẫn chạy |
| Hooks | Khai báo trong `.claude/settings.json`. Có 33 sự kiện, trong đó `PreToolUse`, `PostToolUse`, `Stop`, `Notification` là chính. Thoát mã `2` thì chặn thao tác, stderr là lý do gửi cho Claude. Có dạng exec `command` + `args` (không qua shell), hợp với Windows |
| MCP | `claude mcp add <ten> -- <lenh>`, phạm vi `--scope local/project/user`, file `.mcp.json`, kiểm tra bằng `/mcp`. Playwright: gói `@playwright/mcp` |
| Chạy không giao diện | `claude -p "..."`, `--allowedTools`, `--permission-mode acceptEdits/auto/dontAsk`, `--output-format json`, `--max-budget-usd`, `--permission-prompts none`. ⚠️ **Extension không thêm `claude` vào PATH**, phải cài CLI riêng: `irm https://claude.ai/install.ps1 \| iex` |
| Lập lịch | `/loop` (chỉ chạy khi phiên còn mở, hết hạn sau 7 ngày), Desktop scheduled tasks, Cloud routines. Series dùng **Windows Task Scheduler + `claude -p`** cho dễ hiểu và chạy hoàn toàn trên máy |
| Subagents | `.claude/agents/*.md`, frontmatter `name`, `description`, `tools`, `model`. Gọi bằng ngôn ngữ tự nhiên hoặc `@"ten (agent)"`. Chạy song song tối đa 20 subagent |
| Plugin | `.claude-plugin/plugin.json` + `skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json`. Marketplace: `.claude-plugin/marketplace.json`. Lệnh `claude plugin validate`, `claude plugin marketplace add`, `claude plugin install ten@marketplace` |
| WebSearch / WebFetch (phần 2) | WebSearch dùng backend tìm kiếm của Anthropic (**không phải Google VN**), tối đa **200 lượt/phiên tương tác**. WebFetch đọc tối đa 100.000 ký tự/lần, **tóm tắt bằng một model riêng** ("lossy by design"), **từ chối localhost**, có quyền `WebFetch(domain:...)` |
| Hook PostToolUse (phần 2) | Thoát mã 2 → stderr được đưa cho Claude. Thoát mã 0 → stdout **không** tới Claude, phải trả `hookSpecificOutput.additionalContext` |
| Windows (phần 2, đo thực tế) | Phiên `-p` dùng công cụ `PowerShell` để chạy lệnh, subagent là `Task`. Quyền viết `PowerShell(python *)`. Gọi `/skill` từ Git Bash bị đổi thành đường dẫn |

## 4. Bối cảnh nội dung và khoảng trống

- Nội dung về Claude Code trên thế giới (Anh, Hàn, Nhật, Tây Ban Nha, Pháp, Đức) đang chuyển mạnh sang hướng **"Claude Code cho người không lập trình"**: xử lý Excel, PDF, báo cáo. Ví dụ điển hình là trích 40 báo giá PDF vào Excel, hay nhân viên kế toán phân loại sao kê và hóa đơn.
- Nội dung **tiếng Việt** đa số vẫn là (1) giới thiệu chung chung, (2) dành cho lập trình viên, (3) quay màn hình dài 20–40 phút. **Khoảng trống:** series tiếng Việt, ngắn 5 phút, mỗi tập giải **một việc văn phòng có thật**, có **file mẫu tải về để làm theo**.
- Hầu hết video đối thủ chỉ "demo trót lọt". Series này **khác biệt** ở chỗ dữ liệu demo được **cố tình gài lỗi** (trùng lặp, sai tổng, viết lệch tên, số điện thoại sai). Người xem thấy Claude **bắt lỗi** chứ không chỉ "làm nhanh". Đó là lợi ích thật, và cũng là khoảnh khắc "wow" để giữ chân người xem.

## 5. Nguyên tắc giữ chân người xem (tổng hợp nghiên cứu)

1. **2–3 giây đầu quyết định.** Mở bằng **kết quả cuối cùng** hoặc con số đối lập ("3 tiếng → 40 giây"), không chào hỏi, không giới thiệu kênh.
2. **Trả "phần thưởng" sớm và rải đều.** Cứ khoảng 45–60 giây phải có một khoảnh khắc mới: kết quả hiện ra, lỗi được bắt, mẹo bất ngờ.
3. **Vòng lặp mở (open loop).** Hứa một điều ở đầu ("cuối video có một mẹo giúp bạn không bao giờ mất file") và trả ở cuối.
4. **Tụt người xem mạnh trong 30 giây đầu nghĩa là hook hỏng.** Theo dõi biểu đồ giữ chân trong YouTube Studio sau mỗi tập để chỉnh hook tập sau.
5. **Tua nhanh (speed ramp) đoạn Claude đang chạy.** Người xem không cần nhìn 40 giây chờ. Tăng tốc 4–8x kèm đồng hồ đếm thời gian thật ở góc.

> Lưu ý: các con số về giữ chân người xem trên mạng chủ yếu đến từ blog bên thứ ba, chưa có số liệu chính thức của YouTube. Hãy coi chúng là nguyên tắc tham khảo và kiểm chứng bằng số liệu của chính kênh.

## 6. Rủi ro và cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Kết quả AI mỗi lần chạy một khác, quay nhiều lần không khớp | Mỗi tập có `chuan-bi.py` để reset dữ liệu và `dap-an.json` để đối chiếu số liệu. Ghi hình bản chạy tốt nhất, lời thoại nói theo **ý** chứ không đọc số cứng (trừ số trong đáp án) |
| Người xem dùng gói Free nên không chạy được | Nói rõ yêu cầu gói trả phí ngay tập 1 (mô tả + bình luận ghim) |
| Người xem sợ AI làm hỏng file | Tập 1 dạy chế độ Plan và file hoàn tác. Tập 6 dạy hooks chặn xóa và tự sao lưu. Luôn làm trên **bản sao** dữ liệu |
| Dữ liệu nhạy cảm của công ty | Toàn bộ dữ liệu demo là **hư cấu**. Nhắc người xem tuân thủ quy định bảo mật dữ liệu của đơn vị trước khi đưa dữ liệu thật vào bất kỳ công cụ AI nào |
| Tính năng thay đổi theo phiên bản | Ghi rõ phiên bản (2.1.312) trong mô tả. Kịch bản đã ghi chú các điểm dễ thay đổi |

## 7. Nguồn

- Tài liệu chính thức: [VS Code](https://code.claude.com/docs/en/vs-code) · [Hooks](https://code.claude.com/docs/en/hooks) · [Skills](https://code.claude.com/docs/en/skills) · [Headless](https://code.claude.com/docs/en/headless) · [Subagents](https://code.claude.com/docs/en/sub-agents) · [MCP](https://code.claude.com/docs/en/mcp) · [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) · [Plugins](https://code.claude.com/docs/en/plugins) · [Marketplace](https://code.claude.com/docs/en/plugins/create-marketplace) · [Cài đặt](https://code.claude.com/docs/en/setup)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- Xu hướng "Claude Code cho người không lập trình": [upliora.es](https://www.upliora.es/blog/claude-code-equipos-no-tecnicos-casos-uso-empresas-2026) · [the-intelligence-academy.com](https://www.the-intelligence-academy.com/blog/claude-code-sans-etre-developpeur) · [claudecodefornoncoders.substack.com](https://claudecodefornoncoders.substack.com/p/week-1-claude-code-for-non-coders) · [sumproduct.com](https://sumproduct.com/blog/ai-blog-claude-code-the-agent-in-your-terminal/)
- Hook và giữ chân người xem: [outlierkit.com](https://outlierkit.com/resources/youtube-hooks-and-retention/) · [opus.pro](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention) · [subscribr.ai](https://subscribr.ai/youtube-strategy/perfect-youtube-short-length-structure-hooks)
