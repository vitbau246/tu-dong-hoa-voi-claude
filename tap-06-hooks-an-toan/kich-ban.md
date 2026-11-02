# Tập 6: Gắn phanh an toàn cho AI (Hooks)

| | |
|---|---|
| **Mục tiêu người xem** | Đặt "luật cứng" mà AI **không thể vi phạm**, ghi lại mọi việc AI làm, và nhận thông báo khi AI xong việc |
| **Tính năng dạy** | Hooks: `PreToolUse` (chặn), `PostToolUse` (ghi nhật ký), `Stop` / `Notification` (thông báo). Quy tắc `permissions.deny`. Lệnh `/hooks` |
| **Hình ảnh xuyên suốt** | Một chiếc xe an toàn có 3 thứ: 🛑 **Phanh** · 📹 **Camera hành trình** · 🔔 **Chuông báo** |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/du-lieu-goc/` (sổ cái, bảng lương, công nợ + 3 file rác) và `demo/lam-viec/`. `--giai-phap` chép thêm hooks hoàn chỉnh |
| **Đã kiểm thử** | Hook phanh: 9/9 tình huống đúng (5 chặn, 4 cho qua). `claude doctor` không cảnh báo. Thông báo Windows hiển thị đúng tiếng Việt |

## Chuẩn bị

1. `python chuan-bi.py`, sau đó mở `tap-06-hooks-an-toan/demo` trong VS Code. Máy cần `python` trong PATH (hook gọi `python`).
2. **Sau khi tạo hook phải mở cuộc trò chuyện mới** thì hook mới chắc chắn có hiệu lực. Gõ `/hooks` để xem danh sách hook đang chạy.
3. Nếu thời gian quay hạn chế: `python chuan-bi.py --giai-phap` để có sẵn hooks, rồi chỉ quay cảnh mở file và cảnh thử nghiệm.
4. Bật Windows notifications (Settings → System → Notifications) và tắt Focus Assist khi quay cảnh chuông báo.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Khung chat: Claude đề xuất `Remove-Item du-lieu-goc\...` → hộp đỏ `⛔ BỊ CHẶN bởi hook phanh-an-toan`. `SFX: phanh xe` | AI vừa định xóa file trong thư mục sổ cái của công ty. Và nó bị chặn. |
| 0:06 | Claude trả lời: "Tôi không được phép sửa du-lieu-goc. Tôi sẽ sao chép sang lam-viec/ và xử lý ở đó." | Không phải mình bấm từ chối. Là một quy tắc mình cài sẵn, chạy **trước** mọi hành động của AI. Và AI tự hiểu, tự đổi cách làm. |
| 0:15 | Người dẫn | Tập một mình dạy chế độ Plan, nhưng chế độ đó dựa vào việc bạn đọc kỹ. Hôm nay là thứ mạnh hơn: luật cứng, AI **không thể** vượt qua, dù bạn có lỡ tay bấm đồng ý. |
| 0:28 | Hình chiếc xe với 3 nhãn: `🛑 Phanh` · `📹 Camera hành trình` · `🔔 Chuông báo` | Mình sẽ trang bị cho Claude ba thứ như một chiếc xe an toàn: phanh, camera hành trình, và chuông báo. Tất cả gọi chung là **Hooks**, tức các móc sự kiện. |
| **0:38** | **🛑 PHANH** — Cây thư mục: `du-lieu-goc/` (sổ cái, bảng lương, công nợ). Dán PROMPT 1 | Thư mục du-liệu-gốc chứa số liệu kế toán chính thức, chỉ được đọc. Mình nhờ chính Claude viết hook: trước mỗi lệnh hoặc mỗi lần sửa file, kiểm tra xem có đụng tới du-liệu-gốc không, có thì chặn. |
| 0:55 | Claude tạo `.claude/hooks/phanh-an-toan.py` và `.claude/settings.json` `[TUA x6]`. Zoom `settings.json`: `"PreToolUse"`, `"matcher": "Bash\|PowerShell\|Edit\|Write"` | Hai file. File cài đặt nói "trước khi dùng các công cụ này, hãy chạy script phanh". Script kiểm tra, nếu vi phạm thì trả về mã hai, nghĩa là chặn, kèm lý do bằng tiếng Việt. |
| 1:15 | Zoom script: dòng `print(... file=sys.stderr)` + `sys.exit(2)` | Lý do này được gửi ngược lại cho Claude. Đây là điểm hay: AI không chỉ bị chặn, mà còn **biết vì sao** và biết nên làm gì thay thế. |
| 1:28 | Mở cuộc trò chuyện mới. Gõ `/hooks` → danh sách hiện hook PreToolUse | Mở phiên mới để hook có hiệu lực, gõ /hooks để kiểm tra. Đã có. |
| 1:38 | Chế độ **Auto**. Dán PROMPT 2: "dọn file rác trong du-lieu-goc" → Claude thử xóa → ⛔ → Claude chuyển hướng `[TUA x4]` | Giờ thử thách: mình bật chế độ tự động, rồi **cố tình** bảo nó dọn file rác ngay trong du-liệu-gốc. Nó thử xóa, bị chặn. Đọc lý do, rồi chép sang làm-việc để xử lý, và để lại danh sách file rác cho mình tự quyết. |
| 2:00 | `TEXT: Chế độ Auto · Bạn không bấm gì · Vẫn bị chặn` | Nhấn mạnh: chế độ tự động, mình không bấm gì cả, nhưng luật vẫn được thực thi. |
| **2:10** | **📹 CAMERA HÀNH TRÌNH** — Dán PROMPT 3. Claude thêm hook `PostToolUse` + `camera-hanh-trinh.py` | Thứ hai, camera hành trình. Sau **mỗi** lệnh AI chạy và mỗi file AI sửa, ghi một dòng vào file nhật ký: lúc nào, công cụ gì, làm gì. |
| 2:25 | Cho Claude làm một việc nhỏ trong `lam-viec/`, sau đó mở `.claude/nhat-ky-claude.csv` bằng Excel: các cột Thời gian / Công cụ / Chi tiết | Mở bằng Excel: từng dòng một, giờ phút giây. Sếp hỏi "con AI đó đã làm gì với dữ liệu?", bạn có câu trả lời. Ở nhiều công ty, đây là yêu cầu bắt buộc khi dùng AI. |
| **2:45** | **🔔 CHUÔNG BÁO** — Dán PROMPT 4. Claude thêm hook `Stop` và `Notification` + `chuong-bao.ps1` | Thứ ba, chuông báo. Khi Claude làm xong, hoặc khi nó cần mình duyệt, Windows hiện thông báo. |
| 3:00 | Giao một việc dài (PROMPT 5) → chuyển sang cửa sổ Outlook/Excel làm việc khác `[TUA x8]` → góc phải màn hình hiện toast "Claude đã làm xong" `SFX: ding` | Mình giao một việc dài rồi đi trả lời email. Không cần ngồi canh. Ting: "Claude đã làm xong". |
| 3:15 | `TEXT: Giao việc → làm việc khác → được gọi khi xong` | Đây mới thực sự là có trợ lý: giao việc, làm việc khác, được gọi khi xong. |
| **3:25** | **MẸO PRO: nói thật về giới hạn** — Sơ đồ 4 lớp: `Plan mode` → `permissions.deny` → `Hook phanh` → `Bản sao lưu` | Giờ là phần mình phải nói thật: hook phanh **không phải tường thành tuyệt đối**. Nó bắt các lệnh xóa, sửa phổ biến. Nhưng nếu AI viết một script Python để xóa file thì câu lệnh trông vô hại, và hook có thể không nhận ra. |
| 3:45 | Zoom `settings.json` phần `"permissions": {"deny": ["Edit(du-lieu-goc/**)"]}` | Vì vậy, hãy xếp nhiều lớp. Lớp quy tắc cấm sửa file ngay trong cài đặt. Lớp hook. Và lớp cuối cùng, không thể thiếu: **luôn có bản sao lưu** dữ liệu gốc ở nơi AI không chạm tới được. |
| 4:05 | `TEXT: .claude/settings.json + git = cả team có cùng phanh` | Mẹo cuối: file cài đặt này nằm trong thư mục dự án. Đưa nó lên git, cả nhóm của bạn có cùng một bộ phanh. |
| 4:15 | Tóm tắt: `🛑 PreToolUse = chặn trước` · `📹 PostToolUse = ghi sau` · `🔔 Stop/Notification = gọi bạn` | Tóm lại: chặn trước, ghi sau, gọi bạn khi cần. |
| 4:27 | `TEXT: BÀI TẬP: cài hook chuông báo cho thư mục bạn hay dùng Claude nhất` | Bài tập dễ nhất mà lợi nhất: cài chuông báo. Bạn sẽ không bao giờ phải ngồi canh AI nữa. |
| 4:37 | Teaser: trình duyệt Chrome tự mở, tự gõ, tự điền form | Tới giờ Claude mới làm việc với file trên máy. Tập sau, mình cho nó **lái trình duyệt**: tự vào web, tự thu thập dữ liệu, tự điền form. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (phanh)
```text
Tạo một hook PreToolUse cho dự án này:
- Script Python .claude/hooks/phanh-an-toan.py đọc JSON từ stdin.
- Nếu công cụ là Edit/Write/NotebookEdit và file nằm trong du-lieu-goc/ → chặn.
- Nếu là Bash/PowerShell và lệnh nhắc tới du-lieu-goc kèm thao tác xóa/di chuyển/ghi
  (rm, del, Remove-Item, mv, Move-Item, Set-Content, Out-File, >, ...) → chặn.
- Chặn = in lý do tiếng Việt ra stderr (kèm gợi ý: sao chép sang lam-viec/) và thoát mã 2.
Khai báo trong .claude/settings.json, dùng "command": "python" với "args" trỏ tới
${CLAUDE_PROJECT_DIR}/.claude/hooks/phanh-an-toan.py. Thêm luật permissions.deny Edit(du-lieu-goc/**).
Sau đó tự kiểm thử script bằng vài JSON mẫu (cả trường hợp chặn và cho qua).
```

**PROMPT 2** (thử thách, ở phiên mới, chế độ Auto)
```text
Dọn dẹp thư mục du-lieu-goc: xóa file tạm của Excel (~$...), file log và các file "Copy of ...".
```

**PROMPT 3** (camera hành trình)
```text
Thêm hook PostToolUse: sau mỗi lần dùng Bash/PowerShell/Edit/Write, ghi 1 dòng vào
.claude/nhat-ky-claude.csv gồm Thời gian (dd/mm/yyyy hh:mm:ss), Công cụ, Chi tiết (lệnh hoặc đường dẫn file), Phiên.
File CSV phải mở được bằng Excel, hiển thị đúng tiếng Việt (UTF-8 có BOM).
```

**PROMPT 4** (chuông báo)
```text
Thêm hook Stop và Notification (matcher permission_prompt) để hiện thông báo Windows (toast):
"Claude đã làm xong" hoặc "Claude đang chờ bạn duyệt". Viết bằng PowerShell 5.1 (không cài thêm module),
lưu file .ps1 dạng UTF-8 có BOM, gọi bằng powershell.exe -NoProfile -ExecutionPolicy Bypass -File.
```

**PROMPT 5** (việc dài để thử chuông)
```text
Sao chép toàn bộ du-lieu-goc sang lam-viec/ban-sao, rồi với mỗi file Excel tạo một sheet "Thong-ke"
gồm tổng, trung bình, lớn nhất, nhỏ nhất của từng cột số.
```

## Lời giải tham chiếu

`giai-phap/.claude/` gồm `settings.json`, `hooks/phanh-an-toan.py`, `hooks/camera-hanh-trinh.py`, `hooks/chuong-bao.ps1` (UTF-8 BOM). Đã kiểm thử trên Windows 10, Claude Code 2.1.312.

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| Hook không chạy | Mở cuộc trò chuyện mới. Gõ `/hooks` để kiểm tra. Chạy `claude doctor` để xem lỗi cài đặt |
| Lỗi `python not found` | Thay `"command": "python"` bằng đường dẫn đầy đủ, ví dụ `C:\\Python310\\python.exe` |
| Thông báo hiện ra nhưng chữ lỗi font | File `.ps1` thiếu BOM. Lưu lại bằng "UTF-8 with BOM" (VS Code: góc phải dưới → Save with Encoding) |
| Claude vẫn xóa được bằng script Python | Đúng như phần "nói thật về giới hạn". Dựng thành cảnh minh họa luôn cũng rất tốt |

## Gói đăng tải

- **Tiêu đề:**
  - A: `AI định xóa sổ cái công ty và bị chặn: Hooks trong Claude Code | Tự động hóa với Claude #6`
  - B: `3 "đồ bảo hộ" bắt buộc khi cho AI làm việc trên máy bạn (Claude + VS Code)`
- **Thumbnail:** Hộp đỏ "⛔ BỊ CHẶN" che lên lệnh `Remove-Item`. Chữ: **"AI KHÔNG THỂ XÓA"**.
- **Shorts:** (1) 1:38–2:10 "Chế độ Auto mà vẫn bị chặn", (2) 3:25–4:05 "Hook không phải tường thành".
- **Bình luận ghim:** link tải 4 file hook + "Bạn muốn cấm AI làm điều gì nhất?"
