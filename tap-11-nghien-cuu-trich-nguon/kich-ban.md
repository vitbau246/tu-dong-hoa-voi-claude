# Tập 11: Nghiên cứu bằng AI mà KHÔNG sợ bịa số: mọi con số đều được kiểm chứng

> **Phần 2: Nâng cao.** Từ tập này người xem đã biết Skills, Hooks, MCP, Subagents (tập 1–10).

| | |
|---|---|
| **Mục tiêu người xem** | Dùng Claude tìm kiếm và đọc web để làm báo cáo nghiên cứu, **mỗi con số có trích dẫn nguyên văn**, rồi kiểm chứng tự động bằng cách mở lại nguồn gốc |
| **Tính năng dạy** | WebSearch, WebFetch (và điểm yếu: **tóm tắt có mất mát**), quyền `WebFetch(domain:...)`, script kiểm chứng, đóng gói thành skill `/nghien-cuu` |
| **Dữ liệu** | `python chuan-bi.py` (cần mạng) tạo `demo/de-bai.md` và `demo/ban-nhap-dong-nghiep/` (9 trích dẫn lấy **trực tiếp** từ Wikipedia lúc chạy, gài 2 câu sửa số + 1 câu bịa). `--giai-phap` chép script kiểm chứng + skill |
| **Đã kiểm thử** | `kiem-chung-trich-dan.py` trên bản nháp: **6 KHỚP · 3 KHÔNG THẤY**, đúng cả 3 lỗi gài. Có trích dẫn giống **99,5%** nhưng sai đúng một con số vẫn bị bắt |

## Chuẩn bị

1. `pip install requests beautifulsoup4 lxml pdfplumber`, sau đó `python chuan-bi.py` (cần Internet), rồi mở `tap-11-nghien-cuu-trich-nguon/demo` trong VS Code.
2. Bước 1 là nghiên cứu **thật** trên Internet nên kết quả mỗi lần một khác. Đó là điều bình thường. Lời thoại bước 1 không đọc số cụ thể, chỉ đọc số nào đã qua kiểm chứng ở bước 2.
3. Khi Claude hỏi quyền WebFetch: chọn **"Yes, and don't ask again for <tên miền>"** cho các nguồn uy tín. Nhân cảnh này giải thích về quyền.
4. Script kiểm chứng phải có sẵn khi quay (`--giai-phap`). Prompt để Claude tự viết script này nằm ở mục **PROMPT phụ** bên dưới, đưa vào mô tả video.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Terminal chạy kiểm chứng trên bản nháp: 6 dòng ✅ chạy ra, rồi 3 dòng ❌ đỏ. Zoom `❌ [N3] KHÔNG THẤY 99.5% — Số không có trong nguồn: 3.526` | Câu này giống nguồn chín mươi chín phẩy năm phần trăm. Và nó sai. Sai đúng một con số. |
| 0:07 | Zoom `❌ [N9] … (bịa)` | Câu này thì nguồn không hề có. Hoàn toàn bịa. |
| 0:12 | Người dẫn | Nỗi sợ lớn nhất khi dùng AI để nghiên cứu là **bịa số**. Hôm nay mình làm một quy trình mà mỗi con số trong báo cáo đều được máy mở lại nguồn gốc và đối chiếu từng chữ. Số nào không có trong nguồn sẽ bị loại. |
| 0:25 | Thanh 3 bước: `① Nghiên cứu có trích dẫn ② Kiểm chứng tự động ③ Đóng gói /nghien-cuu` | |
| **0:28** | **① NGHIÊN CỨU** — Mở `de-bai.md`: câu hỏi về thị trường TMĐT Việt Nam 2025 + 5 yêu cầu bắt buộc | Đề bài: thị trường thương mại điện tử Việt Nam năm 2025. Năm yêu cầu, quan trọng nhất là: mọi con số phải kèm **câu trích nguyên văn** từ nguồn. |
| 0:40 | Dán PROMPT 1 → Claude trình bày kế hoạch: 4 câu hỏi con, nguồn ưu tiên, truy vấn Việt + Anh | Claude không tìm lung tung. Nó chia nhỏ câu hỏi, chọn loại nguồn ưu tiên: Bộ Công Thương, báo cáo của các tổ chức nghiên cứu, rồi mới tới báo chí. Và nó tìm bằng cả tiếng Việt lẫn tiếng Anh. |
| 0:58 | Chuỗi WebSearch/WebFetch chạy `[TUA x8]`. Hộp thoại xin quyền WebFetch → chọn "Yes, and don't ask again for moit.gov.vn" | Claude đang tìm và đọc hàng chục trang. Mỗi lần mở một trang web mới, nó xin phép. Với nguồn uy tín, chọn "đừng hỏi lại tên miền này". Lần sau đọc nguồn đó, nó không hỏi nữa. |
| 1:18 | Mở `bao-cao.md` (1 trang, số gắn `[N1]`…) và `nguon.csv` (cột trích dẫn nguyên văn + URL) | Kết quả: báo cáo một trang, mỗi con số gắn mã nguồn. Và file nguồn: câu trích nguyên văn kèm đường dẫn. Trông rất chuyên nghiệp. Nhưng **có đúng không?** |
| **1:30** | **② KIỂM CHỨNG** — Đồ họa: `Trang web → [model tóm tắt] → Claude`. `TEXT: WebFetch = bản tóm tắt, có mất mát` | Bước hai, bí mật ít người biết: khi Claude đọc web, nó không đọc nguyên trang. Một model khác đọc trước rồi **tóm tắt** lại cho Claude. Tài liệu chính thức của Anthropic nói thẳng: công cụ này "lossy by design", tức có mất mát theo thiết kế. Con số có thể bị làm tròn, câu có thể bị diễn đạt lại. |
| 1:52 | Mở `kiem-chung-trich-dan.py`, cuộn nhanh, highlight `requests.get` + `do_khop` + "so con số trong ĐOẠN tương ứng" | Vì vậy mình dùng một script nhỏ: tải lại **nguyên bản** từng trang, tìm câu trích, so từng chữ. Và nếu câu gần giống nhưng **con số** khác, thì đánh trượt luôn. |
| 2:08 | Chạy trên `nghien-cuu/.../nguon.csv` của Claude → phần lớn ✅, vài 🟡/⚠️ | Chạy trên báo cáo của Claude: phần lớn khớp. Vài câu gần đúng, vài trang không tải được vì chặn máy hoặc cần JavaScript. |
| 2:22 | Dán PROMPT 2 → Claude sửa các câu 🟡, đánh dấu ⚠️ "(chưa kiểm chứng tự động)" → chạy lại → không còn ❌ | Mình bảo Claude xử lý: câu gần đúng thì lấy lại nguyên văn, trang không tải được thì ghi rõ "chưa kiểm chứng tự động". Chạy lại: sạch. |
| 2:38 | Chạy trên `ban-nhap-dong-nghiep/nguon.csv` → **6 ✅ · 3 ❌** (cảnh mở đầu) | Còn đây là bản nháp đồng nghiệp gửi mình, lấy từ Wikipedia. Ba lỗi. Hai câu bị sửa một con số, một câu bịa hoàn toàn. Người đọc lướt **không thể** phát hiện. |
| 2:55 | `TEXT: Dùng được cho MỌI tài liệu có trích nguồn: của AI, của đồng nghiệp, của đối tác` | Script này dùng được cho mọi tài liệu có trích nguồn, dù do AI viết, đồng nghiệp viết hay đối tác gửi. |
| **3:05** | **③ ĐÓNG GÓI** — Dán PROMPT 3 → Claude tạo `.claude/skills/nghien-cuu/` (SKILL.md + scripts/) | Bước ba: đóng gói cả quy trình thành lệnh nghiên-cứu, với bước kiểm chứng là **bắt buộc**: còn trích dẫn sai thì không được bàn giao. |
| 3:18 | Zoom SKILL.md mục "4. Kiểm chứng (bắt buộc, không được bỏ qua)" + "nguồn không có con số đó thì xóa con số khỏi báo cáo" | Câu quan trọng nhất trong skill: nguồn không có con số đó thì **xóa con số khỏi báo cáo**. Thà thiếu còn hơn sai. |
| 3:28 | Cuộc trò chuyện mới: `/nghien-cuu Chi phí quảng cáo trung bình trên Shopee và TikTok Shop cho người bán nhỏ` `[TUA x10]` → bàn giao 4 dòng | Thử một câu hỏi mới. Lệnh chạy hết: lập kế hoạch, tìm, viết, tự kiểm chứng, rồi bàn giao bốn dòng. |
| **3:45** | **MẸO PRO** — 4 thẻ: `🇻🇳+🇬🇧 Tìm cả 2 thứ tiếng` · `📅 Ghi năm của số liệu` · `⚖️ Nguồn vênh nhau → ghi cả hai` · `🔢 200 lượt tìm/phiên` | Bốn mẹo. Tìm cả tiếng Anh, vì nhiều báo cáo gốc về Việt Nam viết bằng tiếng Anh. Luôn ghi số liệu của **năm nào**. Hai nguồn vênh nhau thì ghi cả hai, đó là thông tin quý chứ không phải lỗi. Và mỗi phiên có giới hạn hai trăm lượt tìm kiếm, nên nghiên cứu lớn thì chia nhỏ. Tập sau mình chia việc cho cả một đội. |
| 4:10 | `⚠️ TEXT: Kiểm chứng = "nguồn có nói vậy", KHÔNG phải "điều đó đúng"` | Một lưu ý trung thực: script chỉ xác nhận **nguồn có nói vậy**, chứ không xác nhận điều đó đúng. Chọn nguồn uy tín vẫn là việc của bạn. |
| 4:22 | Tóm tắt: `Trích NGUYÊN VĂN` · `Máy mở lại nguồn để so` · `Thà thiếu còn hơn sai` | |
| 4:30 | `TEXT: BÀI TẬP: chạy kiểm chứng trên 1 báo cáo có trích nguồn bạn từng nhận` | Bài tập: lấy một báo cáo có trích nguồn bạn từng nhận, cho Claude lập file nguồn rồi chạy kiểm chứng. Kết quả có thể làm bạn bất ngờ. |
| 4:38 | Teaser: 4 khung "nhà nghiên cứu" chạy song song + 1 "người kiểm chứng" | Tập sau: một người nghiên cứu là chậm. Mình lập **đội nghiên cứu** bốn người chạy song song, cộng một người chuyên đi kiểm chứng. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (nghiên cứu)
```text
Nghiên cứu theo @de-bai.md. Trước khi tìm, trình bày kế hoạch: 3–5 câu hỏi con, loại nguồn ưu tiên, truy vấn (Việt + Anh).
Kết quả lưu ở nghien-cuu/tmdt-viet-nam-2025/:
- nguon.csv (UTF-8) cột: ma,nhan_dinh,trich_dan,url (trich_dan là câu NGUYÊN VĂN chứa con số, khi WebFetch hãy yêu cầu trích nguyên văn)
- bao-cao.md tối đa 1 trang, mỗi con số gắn [mã], tách phần Số liệu / Nhận định / Điểm vênh giữa các nguồn.
```

**PROMPT 2** (xử lý kết quả kiểm chứng)
```text
Chạy python kiem-chung-trich-dan.py nghien-cuu/tmdt-viet-nam-2025/nguon.csv.
KHÔNG THẤY hoặc GẦN ĐÚNG: mở lại nguồn lấy đúng câu nguyên văn; nguồn không có con số đó thì xóa con số khỏi báo cáo.
KHÔNG TẢI ĐƯỢC: ghi "(chưa kiểm chứng tự động)" cạnh con số. Chạy lại tới khi không còn KHÔNG THẤY.
```

**PROMPT 3** (đóng gói)
```text
Đóng gói quy trình vừa rồi thành skill "nghien-cuu" trong .claude/skills/: nhận câu hỏi hoặc file đề bài làm tham số,
kèm script kiểm chứng trong thư mục scripts/ của skill (gọi bằng ${CLAUDE_SKILL_DIR}),
bước kiểm chứng là BẮT BUỘC trước khi bàn giao. allowed-tools: WebSearch WebFetch Read Write Bash(python *) PowerShell(python *).
```

**PROMPT phụ** (đưa vào mô tả video, để người xem tự tạo script kiểm chứng)
```text
Viết kiem-chung-trich-dan.py: đọc CSV (ma,nhan_dinh,trich_dan,url), tải NGUYÊN BẢN từng URL bằng requests
(HTML → text bằng BeautifulSoup, PDF → pdfplumber), chuẩn hóa Unicode NFC + khoảng trắng, tìm câu trích:
khớp nguyên văn = KHỚP; giống >= 85% = GẦN ĐÚNG, nhưng nếu con số trong câu trích không có trong ĐOẠN nguồn tương ứng thì = KHÔNG THẤY;
lỗi tải = KHÔNG TẢI ĐƯỢC. Xuất kiem-chung.csv + in bảng tóm tắt, exit code 1 nếu còn KHÔNG THẤY.
```

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| Nhiều nguồn `KHÔNG TẢI ĐƯỢC` (403) | Trang chặn bot. Đánh dấu "chưa kiểm chứng tự động", hoặc dùng Playwright như tập 13 |
| Trích dẫn từ trang cần JavaScript luôn `KHÔNG THẤY` | `requests` không chạy JavaScript (xem tập 13). Ghi chú nguồn là trang động |
| `chuan-bi.py` báo lỗi lấy câu | Kiểm tra mạng. Wikipedia đổi bố cục thì đổi `NGUON_URL` sang một bài khác có nhiều số liệu |
| Claude tự "làm tròn" số trong `trich_dan` | Đúng loại lỗi script bắt được. Giữ lại làm minh họa |

## Gói đăng tải

- **Tiêu đề:** A: `AI bịa số? Quy trình nghiên cứu mà mọi con số đều được kiểm chứng | Claude nâng cao #11` · B: `Giống nguồn 99,5% mà vẫn SAI: cách bắt AI bịa số liệu`
- **Thumbnail:** Dòng trích dẫn với con số bị khoanh đỏ, nhãn "99,5% GIỐNG… VẪN SAI".
- **Shorts:** (1) 0:00–0:25 "Giống 99,5% vẫn sai", (2) 1:30–1:52 "Bí mật: Claude không đọc nguyên trang web".
- **Bình luận ghim:** PROMPT phụ + link script kiểm chứng.
