# Tập 10 (cuối): Đóng gói thành "trợ lý văn phòng" cho cả team (Plugin)

| | |
|---|---|
| **Mục tiêu người xem** | Gom skill, agent, hook thành **một plugin**, cài bằng một lệnh, chia sẻ cho cả phòng qua git |
| **Tính năng dạy** | Cấu trúc plugin (`.claude-plugin/plugin.json`, `skills/`, `agents/`, `hooks/hooks.json`), marketplace (`marketplace.json`), `claude plugin validate / marketplace add / install / list / details`, `${CLAUDE_PLUGIN_ROOT}` |
| **Dữ liệu** | `python chuan-bi.py` gom các "mảnh" từ tập 1, 3, 4, 5, 6, 9 vào `demo/da-co/`. `--giai-phap` chép marketplace hoàn chỉnh |
| **Đã kiểm thử** | `claude plugin validate` ✔ cả plugin và marketplace. Cài thử trong thư mục cấu hình cô lập: **4 skills · 2 agents · 3 hooks**, chi phí cố định khoảng **386 token/phiên** |

## Chuẩn bị

1. Cần Claude Code CLI (đã cài ở tập 8). `python chuan-bi.py`, sau đó mở `tap-10-plugin-cho-ca-team/demo` trong VS Code.
2. **Cài thử không ảnh hưởng máy thật** (khuyên dùng khi tập dượt). Trong PowerShell: `$env:CLAUDE_CONFIG_DIR = "$env:TEMP\claude-thu"`, rồi chạy các lệnh `claude plugin ...`. Lúc quay thật thì bỏ biến này để VS Code thấy plugin.
3. Chuẩn bị một repo git nội bộ trống (GitLab/GitHub private) để quay cảnh chia sẻ. Hoặc dùng cảnh dựng.
4. Sau khi quay, gỡ: `claude plugin marketplace remove van-phong-demo` (gỡ luôn plugin).

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Máy của "đồng nghiệp" (profile khác): terminal gõ 2 lệnh `claude plugin marketplace add ...` và `claude plugin install tro-ly-van-phong@van-phong-demo` → ✔ | Đồng nghiệp của mình vừa gõ hai lệnh. |
| 0:06 | VS Code của đồng nghiệp: gõ `/tro-ly-van-phong:` → menu hiện `bao-cao-tuan`, `tron-thu`, `kiem-tra-hoa-don`, `don-thu-muc` | Và giờ máy họ có toàn bộ những gì mình xây trong chín tập: báo cáo tuần, trộn thư, kiểm tra hóa đơn, dọn thư mục, đội phân tích báo giá, và cả phanh an toàn. |
| 0:15 | Người dẫn | Tập cuối của series. Bạn đã có rất nhiều công cụ, nhưng chúng đang nằm rải rác trên **một** máy. Hôm nay mình đóng gói tất cả thành một bộ "trợ lý văn phòng", để cả phòng cùng dùng, cùng được cập nhật. Cuối video có lộ trình ba mươi ngày cho bạn. |
| 0:30 | Thanh 3 bước: `① Đóng gói ② Kiểm tra & cài ③ Chia sẻ cho team` | |
| **0:33** | **① ĐÓNG GÓI** — Cây `demo/da-co/`: skills, agents, hooks, kịch bản các tập | Đây là những gì mình có: skill báo cáo tuần ở tập năm, hai agent ở tập chín, hook phanh và chuông ở tập sáu, và quy trình dọn thư mục, kiểm tra hóa đơn, trộn thư ở các tập một, ba, bốn, hiện vẫn đang là prompt. |
| 0:48 | Dán PROMPT 1 | Mình nhờ Claude: đóng gói tất cả thành một plugin tên "trợ-lý-văn-phòng". Những quy trình còn ở dạng prompt thì viết thành skill luôn. |
| 1:00 | Claude tạo cấu trúc `[TUA x8]`. Hiện cây thư mục (đồ họa): `.claude-plugin/plugin.json` · `skills/ (4)` · `agents/ (2)` · `hooks/hooks.json` + 2 script | Plugin chỉ là một thư mục có cấu trúc chuẩn: một file giới thiệu, thư mục skills, thư mục agents, thư mục hooks. Không có gì bí ẩn. |
| 1:18 | Zoom `hooks.json`: `${CLAUDE_PLUGIN_ROOT}/hooks/phanh-an-toan.py`. Zoom docstring: "BẤT KỲ thư mục nào tên du-lieu-goc đều chỉ được đọc" | Một chi tiết hay: hook phanh giờ áp dụng theo **quy ước**. Ở bất kỳ máy nào trong phòng, thư mục nào tên du-liệu-gốc sẽ tự động được bảo vệ. Muốn bảo vệ dữ liệu, chỉ cần đặt đúng tên. |
| 1:35 | Mở `skills/tron-thu/SKILL.md`: zoom `disable-model-invocation: true` + "KHÔNG gửi email" | Với những skill có tác động lớn như trộn thư và dọn thư mục, mình đặt chế độ "chỉ chạy khi người dùng gọi đích danh". Claude sẽ không tự ý chạy chúng. |
| 1:48 | Dán PROMPT 2 → Claude tạo `van-phong-marketplace/.claude-plugin/marketplace.json` | Để chia sẻ, cần thêm một "chợ", tức marketplace: một file danh mục liệt kê các plugin của phòng. |
| **2:00** | **② KIỂM TRA & CÀI** — Terminal: `claude plugin validate ./van-phong-marketplace` → `✔ Validation passed` | Bước hai. Trước khi đưa cho ai, kiểm tra: plugin validate. Đạt. |
| 2:10 | `claude plugin marketplace add ./van-phong-marketplace` → ✔ · `claude plugin install tro-ly-van-phong@van-phong-demo` → ✔ | Thêm chợ, cài plugin. Hai lệnh. |
| 2:20 | `claude plugin details tro-ly-van-phong` → "Skills (4) · Agents (2) · Hooks (3)" · "Always-on: ~386 tok" | Kiểm tra chi tiết: bốn skill, hai agent, ba hook. Và dòng này rất đáng chú ý: plugin chỉ tốn khoảng ba trăm tám mươi token cố định mỗi phiên, vì nội dung skill chỉ được nạp khi thực sự dùng. |
| 2:35 | VS Code → cuộc trò chuyện mới → `/tro-ly-van-phong:bao-cao-tuan 44` → báo cáo hiện ra | Quay lại VS Code, gõ lệnh của plugin. Chạy y như skill ở tập năm. Plugin cài ở terminal thì VS Code cũng dùng được ngay. |
| **2:50** | **③ CHIA SẺ CHO TEAM** — Terminal: `git init`, `git add .`, `git commit`, `git push` lên repo nội bộ | Bước ba: đưa thư mục marketplace lên git của công ty, private cũng được. |
| 3:05 | Màn hình đồng nghiệp: `claude plugin marketplace add <org>/<repo>` (hoặc URL GitLab nội bộ) + `claude plugin install tro-ly-van-phong@van-phong-demo` | Đồng nghiệp chỉ cần hai lệnh: thêm chợ của phòng, cài plugin. Đây chính là cảnh đầu video. |
| 3:18 | Đồ họa: sửa skill → tăng `"version": "1.1.0"` → push → cả phòng nhận bản mới | Khi bạn cải tiến một skill, chỉ cần tăng số phiên bản rồi đẩy lên. Cả phòng nhận bản mới. Một người cải tiến, cả phòng hưởng lợi. |
| **3:30** | **MẸO PRO** — `⚠️ TEXT: Plugin chạy với QUYỀN CỦA BẠN → chỉ cài từ nguồn tin cậy, đọc trước khi cài` | Mẹo cuối và quan trọng nhất: plugin chạy với quyền của chính bạn trên máy. Chỉ cài plugin từ nguồn bạn tin, và đọc qua các hook trước khi cài. Doanh nghiệp còn có thể cấu hình để nhân viên chỉ cài được từ chợ nội bộ. |
| **3:45** | **TỔNG KẾT SERIES** — Dựng nhanh 10 cảnh "wow", mỗi cảnh 2 giây, kèm tên tập | Nhìn lại mười tập. Ba trăm file được dọn trong một phút. Báo cáo sai hai tỷ rưỡi bị lật tẩy. Ba hóa đơn có vấn đề. Bốn mươi thư mời. Báo cáo tuần bằng một lệnh. AI bị chặn trước khi xóa sổ cái. Trình duyệt tự điền form. Bản tin bảy giờ rưỡi sáng. Báo giá rẻ nhất hóa ra đắt nhất. Và giờ là cả phòng dùng chung. |
| 4:10 | Lộ trình 30 ngày (3 dòng): `Tuần 1: Tập 1–4, mỗi ngày tự động 1 việc nhỏ` · `Tuần 2–3: Biến 3 việc lặp lại nhất thành Skill + gắn Hooks` · `Tuần 4: Hẹn giờ 1 việc + đóng gói chia sẻ cho 1 đồng nghiệp` | Lộ trình ba mươi ngày cho bạn. Tuần một: mỗi ngày tự động một việc nhỏ. Tuần hai và ba: biến ba việc lặp lại nhiều nhất thành skill, gắn phanh an toàn. Tuần bốn: hẹn giờ một việc, và chia sẻ cho một đồng nghiệp. |
| 4:30 | `TEXT: Bình luận: việc bạn đã tự động hóa được` | Bình luận cho mình biết bạn đã tự động hóa được việc gì. Những câu chuyện hay nhất sẽ thành tập đặc biệt. |
| 4:40 | Người dẫn, cảnh kết series | Cảm ơn bạn đã đi cùng mình mười tập. Và như mọi lần: |
| 4:50 | Màn hình kết (bản đặc biệt) | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (đóng gói)
```text
Đóng gói mọi thứ trong @da-co/ thành một Claude Code plugin tên "tro-ly-van-phong", đặt tại
van-phong-marketplace/plugins/tro-ly-van-phong/ với cấu trúc chuẩn:
- .claude-plugin/plugin.json (name, version 1.0.0, description, author)
- skills/: bao-cao-tuan (giữ script md_sang_docx.py, gọi bằng ${CLAUDE_SKILL_DIR}),
  và viết thêm 3 skill từ quy trình trong kich-ban-tap/: don-thu-muc (tập 1), kiem-tra-hoa-don (tập 3), tron-thu (tập 4).
  Skill có tác động lớn (don-thu-muc, tron-thu) đặt disable-model-invocation: true.
- agents/: 2 agent có sẵn
- hooks/hooks.json: phanh an toàn (PreToolUse, bảo vệ MỌI thư mục tên du-lieu-goc) và chuông báo (Stop, Notification),
  dùng ${CLAUDE_PLUGIN_ROOT} cho đường dẫn script. Bỏ phần quy tắc riêng của từng dự án.
Viết skill tổng quát, không gắn với tên người hay dữ liệu cụ thể.
```

**PROMPT 2** (marketplace)
```text
Tạo van-phong-marketplace/.claude-plugin/marketplace.json: name "van-phong-demo", owner "Phòng Kế hoạch - Tổng hợp",
liệt kê plugin tro-ly-van-phong với source "./plugins/tro-ly-van-phong" và mô tả ngắn.
```

**Lệnh terminal**
```powershell
claude plugin validate ./van-phong-marketplace
claude plugin marketplace add ./van-phong-marketplace
claude plugin install tro-ly-van-phong@van-phong-demo
claude plugin details tro-ly-van-phong
# Đồng nghiệp (sau khi bạn push lên git):
claude plugin marketplace add <to-chuc>/<repo>        # GitHub; hoặc URL git nội bộ
claude plugin install tro-ly-van-phong@van-phong-demo
```

## Lời giải tham chiếu

`giai-phap/van-phong-marketplace/`: marketplace + plugin hoàn chỉnh (4 skills, 2 agents, hooks.json, `phanh-an-toan.py`, `chuong-bao.ps1` UTF-8 BOM). Đã validate và cài thử thành công với Claude Code 2.1.312.

## Gói đăng tải

- **Tiêu đề:**
  - A: `Đóng gói trợ lý AI cho cả phòng: cài bằng 2 lệnh (Claude Code Plugin) | Tự động hóa với Claude #10`
  - B: `Tập cuối: từ 1 người dùng AI thành cả team tự động hóa`
- **Thumbnail:** Hộp quà mở ra có các biểu tượng 📊 ✉️ 🧾 🛑. Chữ: **"CẢ PHÒNG · 2 LỆNH"**.
- **Shorts:** (1) 0:00–0:15 "2 lệnh là có trợ lý", (2) 3:45–4:10 "10 tập trong 25 giây".
- **Bình luận ghim:** link repo marketplace mẫu + lộ trình 30 ngày + "Việc đầu tiên bạn sẽ tự động hóa?"
