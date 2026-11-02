# Tập 9: Thuê cả một đội AI: 3 trợ lý làm song song (Subagents)

| | |
|---|---|
| **Mục tiêu người xem** | Tạo "trợ lý chuyên trách" (subagent), giao việc song song, và dùng một trợ lý **độc lập** để phản biện kết quả |
| **Tính năng dạy** | Subagents (`.claude/agents/*.md`: `name`, `description`, `tools`, `model`), chạy song song, gọi đích danh `@"ten (agent)"` |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/bao-gia/` (A.docx, B.pdf 3 trang, C.docx) + `demo/yeu-cau-du-an.md`. `--giai-phap` chép 2 subagent mẫu |
| **Con số chốt** | Giá quảng cáo B: **189 triệu** ("rẻ nhất") → TCO 3 năm cho 50 người: **392,04 triệu** (đắt nhất) · A: 240 triệu · C: 330 triệu · B còn **vi phạm** yêu cầu lưu dữ liệu tại Việt Nam |

## Chuẩn bị

1. `python chuan-bi.py`, sau đó mở `tap-09-subagents-doi-ai/demo` trong VS Code. `pip install pdfplumber python-docx openpyxl`.
2. Thư mục `.claude/agents/` chưa có lúc mở phiên, nên sau khi tạo subagent hãy **mở cuộc trò chuyện mới**.
3. Mở sẵn trang 1 của `B - Sao Viet - bao gia CRM.pdf` ở mức zoom 100% để quay cảnh "189.000.000 đ" (chú thích chữ nhỏ gần như không đọc được, đúng ý đồ).

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | PDF báo giá B: chữ đỏ khổng lồ **"189.000.000 đ \*"**, "TRỌN GÓI 3 NĂM". Zoom chậm xuống dấu \* và dòng chữ nhỏ xíu cuối trang | Báo giá rẻ nhất: một trăm tám mươi chín triệu, trọn gói ba năm. Thấy dấu sao nhỏ kia không? |
| 0:07 | Bảng so sánh cuối cùng: B gạch đỏ `189tr → 392tr`. `TEXT: Rẻ nhất → Đắt nhất` | Một đội ba trợ lý AI đã đọc hết chữ nhỏ, và phương án rẻ nhất hóa ra **đắt nhất**, gấp đôi con số quảng cáo. |
| 0:15 | Người dẫn | Tới giờ mình luôn làm việc với **một** Claude. Hôm nay mình lập **một đội**: ba chuyên viên phân tích chạy song song, cộng một thẩm định viên chuyên đi bắt lỗi. Và bạn sẽ thấy vì sao thẩm định viên là nhân vật quan trọng nhất. |
| 0:30 | Thanh 3 bước: `① Lập đội ② Chạy song song ③ Thẩm định độc lập` | |
| 0:33 | Lướt 3 file báo giá: A (Word, bảng rõ ràng), B (PDF quảng cáo màu cam), C (Word, gói cao cấp) + `yeu-cau-du-an.md` | Bối cảnh: công ty cần phần mềm quản lý khách hàng cho năm mươi người, ba năm. Ba nhà cung cấp, ba kiểu tài liệu. Cuối file yêu cầu có một dòng quan trọng: **dữ liệu phải lưu tại Việt Nam**. |
| **0:50** | **① LẬP ĐỘI** — Dán PROMPT 1 | Bước một: tuyển người. Mình nhờ Claude tạo hai "nhân viên". Một chuyên viên phân tích báo giá, đọc kỹ cả chữ nhỏ. Một thẩm định viên độc lập, khó tính, chuyên tìm chỗ sai. |
| 1:05 | Mở `.claude/agents/phan-tich-bao-gia.md`: zoom `description`, `tools: Read, Grep, Glob, Bash, PowerShell`, `model: sonnet` | Mỗi nhân viên là một file văn bản: tên, mô tả công việc, được dùng công cụ nào, và dùng mô hình AI nào. Chuyên viên phân tích chỉ được **đọc**, không được sửa gì. |
| 1:20 | Mở `tham-dinh-doc-lap.md`: zoom "Nhiệm vụ của bạn là tìm chỗ sai…", `model: opus` | Thẩm định viên có chỉ dẫn ngược lại: nhiệm vụ của bạn là **tìm chỗ sai**, không phải đồng ý. Và mình cho nó dùng mô hình mạnh hơn. |
| 1:32 | `TEXT: Mỗi subagent = 1 phòng làm việc riêng` | Điểm mấu chốt: mỗi trợ lý có một "phòng làm việc" riêng, tức bộ nhớ riêng. Nó đọc tài liệu dài bao nhiêu cũng không làm rối cuộc trò chuyện chính của bạn. Xong việc, nó chỉ nộp lại bản tóm tắt. |
| **1:45** | **② CHẠY SONG SONG** — Cuộc trò chuyện mới. Dán PROMPT 2. Màn hình hiện 3 tác vụ subagent chạy cùng lúc `[TUA x6]`, đồng hồ góc | Bước hai, giao việc: ba báo giá, ba chuyên viên, chạy **cùng lúc**. Ba người làm song song thay vì một người làm lần lượt. |
| 2:05 | Ba bản tóm tắt trả về. Highlight bản B: `Giá quảng cáo 189tr chỉ cho 30 người` · `+20 người × 1,5tr × 3 năm = 90tr` · `Phụ lục 2: triển khai 45tr` · `Điều 5: bảo trì 18%/năm từ năm 2 = 68,04tr` · `Điều 3: dữ liệu tại Singapore` | Xem chuyên viên phụ trách báo giá B nộp gì. Giá quảng cáo chỉ cho ba mươi người, nhưng mình cần năm mươi. Hai mươi người thêm, ba năm: chín mươi triệu. Phụ lục hai: phí triển khai bốn mươi lăm triệu. Điều năm: từ năm thứ hai, bảo trì mười tám phần trăm mỗi năm. Và Điều ba: dữ liệu lưu tại **Singapore**. |
| 2:30 | Đồ họa cộng dồn: `189 + 90 + 45 + 68,04 = 392,04 triệu` | Cộng lại: ba trăm chín mươi hai triệu. Gấp đôi con số in to ở trang đầu. |
| **2:42** | **③ THẨM ĐỊNH ĐỘC LẬP** — Gõ `@"tham-dinh-doc-lap (agent)"` + PROMPT 3 | Bước ba, bước nhiều người bỏ qua nhất: cho một người **khác** kiểm tra. Mình gọi đích danh thẩm định viên, a-còng tên agent, và yêu cầu: mở lại file gốc, tính lại từ đầu, đừng tin con số của ai. |
| 3:00 | Thẩm định viên trả về: bảng TCO "Khớp/Lệch", "B bị loại vì vi phạm yêu cầu bắt buộc số 1", thêm rủi ro: "phí xuất dữ liệu 25tr khi chấm dứt", "trả trước 100%", "SLA 99,0% không bồi hoàn" | Thẩm định viên xác nhận các con số, và bổ sung những thứ nằm **ngoài** tổng chi phí: muốn rời nhà cung cấp B thì mất thêm hai mươi lăm triệu để lấy lại dữ liệu của chính mình, phải trả trước một trăm phần trăm, và cam kết chất lượng không có bồi hoàn. Kết luận: B bị loại, dù rẻ đến đâu. |
| 3:25 | Claude chính tổng hợp → mở `so-sanh-bao-gia.xlsx` (bảng TCO + yêu cầu bắt buộc) và `to-trinh-de-xuat.docx`: "Đề xuất chọn A (240tr)… phương án C nếu cần SLA 24/7" | Cuối cùng Claude chính gom lại: một bảng so sánh Excel, và một tờ trình đề xuất chọn A, kèm điều kiện khi nào nên cân nhắc C. Sẵn sàng trình sếp. |
| **3:42** | **MẸO PRO** — 3 lý do dùng subagent: `⚡ Song song = nhanh` · `🧠 Bộ nhớ riêng = đọc sâu, không rối` · `🔍 Người thứ hai = bớt "tự khen mình"` | Vì sao dùng đội thay vì một người? Ba lý do: nhanh hơn vì chạy song song. Đọc sâu hơn vì mỗi người tập trung một tài liệu. Và quan trọng nhất: người làm và người kiểm tra là **hai người khác nhau**, giống hệt quy trình bốn mắt trong công ty bạn. |
| 4:05 | `⚠️ TEXT: Việc nhỏ → đừng dùng đội (tốn hạn mức hơn)` | Nhưng nói thật: mỗi trợ lý đều tiêu hạn mức sử dụng. Việc nhỏ, một tài liệu, thì một Claude là đủ. Hãy dùng đội cho việc lớn, quan trọng, hoặc có nhiều phần độc lập. |
| 4:18 | Tóm tắt: `Agent = file .md trong .claude/agents` · `Giao song song` · `Luôn có người thẩm định độc lập` | |
| 4:25 | `TEXT: BÀI TẬP: tạo 1 agent "phản biện" và cho nó soát lại 1 báo cáo bạn sắp gửi` | Bài tập: tạo một agent phản biện, rồi trước khi gửi bất kỳ báo cáo quan trọng nào, cho nó soát một lượt. |
| 4:35 | Teaser: đồng nghiệp gõ 2 lệnh → có đủ `/bao-cao-tuan`, hooks phanh, đội agent | Chín tập, bạn đã có skill, hook, MCP, agent. Nhưng tất cả đang nằm trên **máy bạn**. Tập cuối: đóng gói tất cả thành một bộ "trợ lý văn phòng", để cả phòng cài bằng hai lệnh. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (lập đội)
```text
Tạo 2 subagent trong .claude/agents/:
1. phan-tich-bao-gia (model sonnet, chỉ dùng Read, Grep, Glob, Bash, PowerShell): phân tích MỘT báo giá.
   Đọc toàn bộ kể cả chú thích chữ nhỏ, điều khoản, phụ lục. Tính TCO theo đúng số người dùng và số năm
   trong yeu-cau-du-an.md. Đối chiếu từng yêu cầu bắt buộc (Đạt/Không đạt/Không rõ).
   Liệt kê chi phí ẩn và rủi ro, mỗi ý có trích dẫn nguyên văn + vị trí. Không suy đoán.
2. tham-dinh-doc-lap (model opus, chỉ dùng Read, Grep, Glob, Bash, PowerShell): người phản biện khó tính.
   Mở lại file gốc, tính lại TCO độc lập, tìm điều khoản bị bỏ sót, loại phương án vi phạm yêu cầu bắt buộc.
Viết phần description rõ ràng để biết khi nào dùng từng agent.
```

**PROMPT 2** (chạy song song, ở cuộc trò chuyện mới)
```text
Dùng 3 subagent phan-tich-bao-gia chạy SONG SONG, mỗi agent phân tích một file trong @bao-gia/
theo yêu cầu trong @yeu-cau-du-an.md. Khi cả 3 xong, tóm tắt cho tôi: giá quảng cáo vs TCO thực tế của từng bên.
```

**PROMPT 3** (thẩm định và tổng hợp)
```text
@"tham-dinh-doc-lap (agent)" hãy thẩm định 3 bản phân tích vừa rồi so với file gốc.
Sau đó tạo:
- so-sanh-bao-gia.xlsx: bảng TCO từng khoản, bảng yêu cầu bắt buộc, bảng rủi ro
- to-trinh-de-xuat.docx: tờ trình 1 trang gửi Ban Giám đốc, có phương án đề xuất, phương án dự phòng, lý do loại
```

## Đối chiếu (dap-an.json)

| Nhà cung cấp | Giá quảng cáo | TCO 3 năm / 50 người | Yêu cầu bắt buộc |
|---|---|---|---|
| A – Đông Á Digital | 240.000.000 | **240.000.000** | Đạt 5/5 (điểm yếu: app chưa offline, hỗ trợ 8x5) |
| B – Sao Việt | **189.000.000** | **392.040.000** (= 189 + 90 + 45 + 68,04) | **Không đạt**: dữ liệu lưu tại Singapore |
| C – Hoàn Cầu Enterprise | 330.000.000 | 330.000.000 | Đạt 5/5, SLA 99,9%, hỗ trợ 24/7 |

Rủi ro B ngoài TCO: phí xuất dữ liệu 25tr khi chấm dứt · trả trước 100% · SLA 99,0% không bồi hoàn · hỗ trợ 8x5.

## Gói đăng tải

- **Tiêu đề:**
  - A: `Báo giá "rẻ nhất" hóa ra ĐẮT NHẤT: 3 trợ lý AI đọc hết chữ nhỏ | Tự động hóa với Claude #9`
  - B: `Lập một đội AI làm việc song song (Subagents trong Claude Code)`
- **Thumbnail:** Chữ đỏ "189 TRIỆU\*" bị kính lúp soi vào dấu \* → "392 TRIỆU". Chữ: **"ĐỌC CHỮ NHỎ"**.
- **Shorts:** (1) 2:05–2:42 "Chữ nhỏ trị giá 200 triệu", (2) 3:42–4:05 "Quy trình bốn mắt cho AI".
- **Bình luận ghim:** 2 file agent mẫu + "Bạn từng bị 'chữ nhỏ' lừa chưa?"
