# Tập 4: 40 thư mời cá nhân hóa và 37 email nháp, không gõ một chữ

| | |
|---|---|
| **Mục tiêu người xem** | Trộn thư (mail merge) từ Excel + mẫu Word, xuất PDF, tạo sẵn email nháp có đính kèm. Biết để **con người duyệt trước khi gửi** |
| **Tính năng dạy** | Gọi nhiều file bằng `@`, để Claude **hỏi lại** khi dữ liệu mơ hồ, xử lý hàng loạt, tạo file `.eml` nháp |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/danh-sach-khach-moi.xlsx` (41 dòng) và `demo/mau-thu-moi.docx` (mẫu có `{{...}}`) |
| **Con số chốt** | 41 dòng → 40 khách (1 trùng) · 40 thư mời · 37 email nháp · 3 người cần bổ sung email · 1 người thiếu danh xưng (không đoán!) |

## Chuẩn bị

1. `python chuan-bi.py`, sau đó mở `tap-04-tron-thu/demo` trong VS Code. `pip install python-docx openpyxl`.
2. Máy cần **Microsoft Word** để xuất PDF (Claude sẽ điều khiển Word qua PowerShell/COM). Không có Word thì đính kèm `.docx`.
3. Outlook desktop được cài và đặt làm ứng dụng mặc định cho `.eml`. Thư nháp mở ra là cửa sổ soạn thư mới.
4. Email trong dữ liệu dùng tên miền `.example` (được dành riêng, không tồn tại). **Lỡ bấm gửi cũng không tới ai.** Nếu Claude thắc mắc về tên miền này, trả lời "đây là dữ liệu demo, bỏ qua".

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Thư mục `thu-moi/` cuộn: 40 file PDF "01 - Đỗ Thành Dũng.pdf"... Mở nhanh 3 thư, tên và bàn số đổi theo từng người | Bốn mươi thư mời. Tên ai người nấy, chức vụ, đơn vị, bàn ngồi, giờ tham dự đều đúng. |
| 0:06 | Outlook bật ra cửa sổ thư nháp: người nhận, tiêu đề có tên, file PDF đính kèm | Kèm ba mươi bảy email nháp, đính kèm sẵn. Mình chỉ việc đọc lại và bấm gửi. |
| 0:12 | Người dẫn | Toàn bộ mất chưa tới ba phút, và mình không gõ một chữ nào vào Word. Nhưng điều đáng xem nhất là lúc Claude **dừng lại hỏi mình** thay vì tự đoán. Lát nữa bạn sẽ thấy. |
| 0:25 | Thanh 3 bước: `① Soát danh sách ② Trộn thư ③ Email nháp` | |
| 0:28 | Mở `mau-thu-moi.docx`: highlight `{{danh_xung}}`, `{{ho_ten}}`... Mở Excel danh sách | Nguyên liệu gồm một mẫu thư Word với các ô trống trong ngoặc nhọn, và danh sách khách mời trong Excel. Ai làm hành chính, sự kiện chắc quá quen. |
| **0:40** | **① SOÁT DANH SÁCH** — Chế độ **Plan**. Gõ `@danh-sach-khach-moi.xlsx @mau-thu-moi.docx` + dán PROMPT 1 | Vẫn quy tắc cũ: soát trước, làm sau. Mình nhắc đến hai file và hỏi: dữ liệu có vấn đề gì trước khi trộn thư? |
| 0:55 | Claude trả về danh sách 4 vấn đề | Bốn vấn đề. |
| 1:00 | Highlight lần lượt: `Dòng 13 & 29 trùng: Hoàng Văn Trung` · `2 khách thiếu email` · `1 email sai định dạng (thiếu @)` | Một khách bị nhập hai lần: nếu không phát hiện, ông Trung nhận hai thư mời, và người gửi trông rất thiếu chuyên nghiệp. Hai người thiếu email, một email bị gõ sai. |
| 1:15 | Highlight: `Trần Minh Anh: thiếu danh xưng. Tên này dùng cho cả nam và nữ, tôi không nên đoán. Bạn muốn dùng gì?` `SFX: ding` | Còn đây là điều mình muốn bạn chú ý: Trần Minh Anh không có danh xưng. Minh Anh có thể là nam, có thể là nữ. Claude **không đoán**, mà hỏi mình. Viết nhầm "Ông" cho một nữ giám đốc là lỗi bạn không muốn mắc phải. |
| 1:35 | Gõ PROMPT 2 (trả lời quyết định) | Mình quyết: gộp dòng trùng, Minh Anh dùng "Ông/Bà", ba người thiếu hoặc sai email thì vẫn làm thư mời nhưng đưa vào danh sách cần bổ sung. |
| **1:50** | **② TRỘN THƯ** — Chuyển **Edit automatically**, dán PROMPT 3 | Bước hai. Mình yêu cầu: mỗi khách một thư Word và một bản PDF, đặt tên theo số thứ tự và họ tên, giờ tham dự lấy theo phiên sáng hoặc chiều. |
| 2:05 | Claude viết `tron_thu.py`, chạy; mở Word ngầm để xuất PDF `[TUA x8]`, đồng hồ góc | Claude viết script thay chữ vào mẫu, giữ nguyên định dạng, rồi điều khiển Word xuất PDF. |
| 2:25 | Mở 3 thư cạnh nhau, zoom vào "Kính gửi", "Thời gian 08:30 / 13:30", "Bàn số" | Kiểm tra ngẫu nhiên ba thư: tên đúng, phiên sáng tám giờ rưỡi, phiên chiều một giờ rưỡi, bàn số đúng. Phông chữ, màu sắc giữ nguyên như mẫu. |
| 2:40 | Mở thư của Trần Minh Anh: "Kính gửi: Ông/Bà Trần Minh Anh" | Và thư của Minh Anh: "Kính gửi Ông/Bà", đúng như mình quyết định. |
| **2:50** | **③ EMAIL NHÁP** — Dán PROMPT 4 | Bước ba, bước tiết kiệm thời gian nhất: email. Nhưng mình **không** cho AI tự gửi. Mình bảo nó tạo **thư nháp**. |
| 3:05 | Thư mục `email-nhap/` có 37 file `.eml`. Double-click một file → Outlook mở cửa sổ soạn thư: To, Subject "Thư mời Hội nghị Khách hàng 2026 – Kính gửi Ông Đỗ Thành Dũng", nội dung cá nhân hóa, PDF đính kèm | Ba mươi bảy file email. Bấm đúp, Outlook mở ra một thư đã soạn sẵn: người nhận, tiêu đề có tên, lời chào riêng, thư mời PDF đính kèm. Đọc lại một giây, bấm gửi. |
| 3:25 | Mở `can-bo-sung.xlsx`: 3 người + lý do | Ba người còn lại nằm trong file "cần bổ sung", kèm lý do. Không ai bị bỏ sót trong im lặng. |
| **3:35** | **MẸO PRO** — `TEXT: Vì sao KHÔNG cho AI tự gửi?` | Vì sao mình không cho Claude gửi thẳng? Claude hoàn toàn làm được, nhưng **gửi email là việc không thể rút lại**. |
| 3:45 | Sơ đồ: `Việc đảo ngược được → để AI làm` · `Việc KHÔNG đảo ngược được → AI chuẩn bị, NGƯỜI bấm nút` | Đây là nguyên tắc mình áp dụng cho mọi tự động hóa: việc gì đảo ngược được thì để AI làm hết. Việc gì không đảo ngược được, như gửi email, chuyển tiền hay xóa dữ liệu, thì AI chuẩn bị, **con người bấm nút cuối**. |
| 4:10 | Tóm tắt: `Soát danh sách` · `Để AI hỏi khi mơ hồ` · `Nháp, không gửi thẳng` | Ba điều: soát danh sách trước, để AI hỏi khi dữ liệu mơ hồ, và chỉ tạo nháp. |
| 4:22 | `TEXT: BÀI TẬP: lấy 1 mẫu giấy tờ bạn hay điền tay → đổi chỗ cần điền thành {{...}}` | Bài tập: lấy một mẫu giấy tờ bạn hay phải điền tay, như giấy xác nhận hay quyết định, rồi thay chỗ cần điền bằng ngoặc nhọn. Phần còn lại để Claude lo. |
| 4:35 | Teaser: gõ `/bao-cao-tuan` → báo cáo hiện ra | Bốn tập vừa rồi, lần nào mình cũng phải dán một prompt dài. Tập sau mình sẽ biến cả quy trình thành **một lệnh** duy nhất. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (Plan: soát danh sách)
```text
@danh-sach-khach-moi.xlsx là danh sách khách mời, @mau-thu-moi.docx là mẫu thư có các ô {{...}}.
Trước khi trộn thư, hãy soát danh sách: dòng trùng, thiếu thông tin, email sai định dạng,
và bất cứ điều gì mơ hồ. Điều gì không chắc chắn thì HỎI TÔI, không tự đoán.
```

**PROMPT 2** (quyết định)
```text
Gộp dòng trùng. Trần Minh Anh dùng danh xưng "Ông/Bà".
Ai thiếu hoặc sai email: vẫn làm thư mời, nhưng ghi vào can-bo-sung.xlsx kèm lý do.
```

**PROMPT 3** (trộn thư)
```text
Viết tron_thu.py: với mỗi khách, thay các ô {{...}} trong mẫu (giữ nguyên định dạng) và lưu vào thu-moi/
dạng "STT - Họ tên.docx". {{thoi_gian}}: phiên Sáng = 08:30 - 11:30, Chiều = 13:30 - 16:30.
Sau đó xuất mỗi file sang PDF bằng Microsoft Word. Báo số thư đã tạo.
```

**PROMPT 4** (email nháp)
```text
Với mỗi khách có email hợp lệ, tạo email nháp .eml trong email-nhap/ (có header X-Unsent: 1
để Outlook mở ra dạng thư soạn mới): tiêu đề "Thư mời Hội nghị Khách hàng 2026 – Kính gửi {Danh xưng} {Họ tên}",
nội dung 3-4 câu lịch sự, cá nhân hóa theo chức vụ và đơn vị, đính kèm PDF thư mời của người đó.
KHÔNG gửi email.
```

## Đối chiếu (dap-an.json)

- 41 dòng → **40** khách (dòng 13 và 29 trùng: Hoàng Văn Trung)
- Thiếu email: Vũ Minh Khánh, Lê Văn Tuấn · Sai định dạng: Ngô Đức Nam (`...at.ankhang.example`)
- Thiếu danh xưng: Trần Minh Anh
- **40** thư mời · **37** email nháp

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| Claude tự đặt "Ông" cho Minh Anh, không hỏi | Câu "điều gì không chắc chắn thì HỎI TÔI" đã có trong prompt. Nếu vẫn xảy ra, dựng thành cảnh dạy "đây là lý do phải kiểm tra", rồi bảo Claude sửa |
| Xuất PDF lỗi COM / Word bị treo | Đóng hết Word đang mở trước khi chạy. Hoặc yêu cầu "xuất PDF lần lượt, đóng Word sau mỗi 10 file" |
| `.eml` mở ra dạng thư đã nhận (không sửa được) | Kiểm tra header `X-Unsent: 1` có nằm trong phần header (trước dòng trống đầu tiên) |

## Gói đăng tải

- **Tiêu đề:**
  - A: `Trộn thư bằng AI: 40 thư mời + 37 email nháp trong 3 phút | Tự động hóa với Claude #4`
  - B: `Mail merge kiểu mới: AI biết DỪNG LẠI HỎI khi không chắc (Claude + VS Code)`
- **Thumbnail:** Quạt 40 thư mời. Chữ: **"40 THƯ · 0 CHỮ GÕ"**.
- **Shorts:** (1) 1:15–1:35 "AI không đoán giới tính, nó hỏi", (2) 3:35–4:10 "Nguyên tắc bấm nút cuối".
- **Bình luận ghim:** 4 prompt + mẫu thư `.docx` để tải.
