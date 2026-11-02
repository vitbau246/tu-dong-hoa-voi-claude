# Tập 3: 30 hóa đơn PDF vào Excel trong 2 phút, và bắt được 3 hóa đơn có vấn đề

| | |
|---|---|
| **Mục tiêu người xem** | Trích xuất dữ liệu từ hàng loạt PDF có bố cục khác nhau, **kèm kiểm tra chéo** để tin được kết quả |
| **Tính năng dạy** | Yêu cầu Claude trích bằng script (thay vì "đọc rồi gõ lại"), quy tắc kiểm tra chéo, kiểm tra ngẫu nhiên |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/hoa-don/` (30 PDF, 4 nhà cung cấp, 3 kiểu bố cục) |
| **Con số chốt** | 30 file = 29 hóa đơn thật + 1 bản trùng · 2 hóa đơn cộng sai (+100.000 đ và −90.000 đ) · Tổng 2 lỗi **chỉ lệch 10.000 đ**, nên nhìn tổng không thể phát hiện |

## Chuẩn bị

1. `python chuan-bi.py`, sau đó mở `tap-03-hoa-don-pdf/demo` trong VS Code.
2. `pip install pdfplumber openpyxl` trước khi quay.
3. Xem `dap-an.json → can_kiem_tra` để biết tên 3 file có vấn đề. **Số file thay đổi nếu sửa `chuan-bi.py`**, còn nếu giữ nguyên seed thì không đổi.
4. Mở sẵn 3 PDF ở 3 bố cục (A: bảng cổ điển, B: thanh màu xanh, C: dạng danh sách) trong trình duyệt để quay cảnh so sánh.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Lưới 30 hóa đơn PDF thu nhỏ. 3 ô chuyển đỏ, nhấp nháy. `TEXT: 30 hóa đơn · 3 có vấn đề` | Ba mươi hóa đơn. Ba cái có vấn đề. Bạn có tìm ra không? |
| 0:05 | Ô Excel: `Tổng chênh lệch: 10.000 đ` | Gợi ý: nếu cộng tổng, bạn chỉ thấy lệch đúng mười nghìn đồng. Nhỏ đến mức ai cũng bỏ qua. |
| 0:12 | Người dẫn | Hôm nay Claude sẽ đưa ba mươi hóa đơn này vào Excel, tự soát từng cái, và chỉ ra chính xác ba hóa đơn có vấn đề, kể cả một lỗi mà chính mình suýt bỏ qua. |
| 0:22 | Thanh 3 bước: `① Trích xuất ② Kiểm tra chéo ③ Soát ngẫu nhiên` | |
| 0:25 | Lật nhanh 3 PDF bố cục A, B, C cạnh nhau, khoanh vùng "Tổng" ở 3 vị trí khác nhau, 3 cách gọi: "Tổng cộng tiền thanh toán" / "TỔNG CỘNG ... VND" / "Phải thanh toán" | Cái khó: bốn nhà cung cấp, ba kiểu mẫu hóa đơn. Cùng một con số "tổng tiền" nhưng mỗi mẫu gọi một tên, nằm một chỗ. Đây là lý do việc nhập liệu hóa đơn chưa bao giờ hết người làm. |
| **0:45** | **① TRÍCH XUẤT** — Dán PROMPT 1 | Bước một. Chú ý câu này trong yêu cầu: **dùng script để trích**, không đọc rồi gõ lại. Tại sao? Script cho kết quả giống hệt nhau mỗi lần chạy, và bạn kiểm tra được. |
| 1:00 | Claude mở thử vài PDF, nhận ra 3 bố cục, viết `trich_hoa_don.py` `[TUA x8]` | Claude mở thử vài file, tự nhận ra có ba kiểu bố cục, rồi viết script xử lý cả ba. |
| 1:20 | Mở `hoa-don-thang-9.xlsx`: sheet *Hoa-don* (1 dòng/hóa đơn), sheet *Chi-tiet* (từng mặt hàng) | Ba mươi file, mỗi file một dòng: nhà cung cấp, mã số thuế, ký hiệu, số, ngày, tiền hàng, thuế, tổng. Thêm một sheet chi tiết từng mặt hàng cho bộ phận kho. |
| **1:40** | **② KIỂM TRA CHÉO** — Dán PROMPT 2. Hiện 4 quy tắc trên màn hình | Bước hai, bước làm nên giá trị thật. Mình cho Claude bốn quy tắc kế toán: tiền hàng phải bằng tổng các dòng; thuế phải bằng tiền hàng nhân thuế suất; tổng phải bằng tiền hàng cộng thuế; và không được có hai hóa đơn cùng **nhà cung cấp và số hóa đơn**. |
| 2:00 | Claude chạy kiểm tra `[TUA x6]`. Sheet *Can-kiem-tra* hiện 3 dòng đỏ | Kết quả: ba dòng đỏ. |
| 2:10 | Zoom dòng 1. Bên cạnh mở PDF tương ứng, khoanh "5.963.000" | Hóa đơn số một trăm bảy mươi bảy: tiền hàng cộng thuế là năm triệu tám trăm sáu mươi ba nghìn, nhưng tổng ghi năm triệu **chín** trăm sáu mươi ba. Thừa một trăm nghìn. |
| 2:25 | Zoom dòng 2: đảo chữ số | Hóa đơn thứ hai bị đảo hai chữ số, thiếu chín mươi nghìn. Một cái thừa một trăm nghìn, một cái thiếu chín mươi nghìn. Cộng lại chỉ lệch mười nghìn. Đó là lý do nhìn tổng thì thấy "gần đúng". |
| 2:42 | Zoom dòng 3: `scan_xxxx.pdf` trùng với `HD_1C25TPN_00000200.pdf` | Và cái thứ ba: một file tên "scan" thực chất là hóa đơn đã nhập rồi. Nếu không phát hiện, công ty trả tiền hai lần. |
| 2:52 | `TEXT: Cùng số 00000224 — nhưng KHÁC nhà cung cấp → KHÔNG trùng` | Để ý: có bốn cặp hóa đơn trùng **số** nhưng khác nhà cung cấp. Claude không báo nhầm, vì mình yêu cầu so cả nhà cung cấp lẫn số hóa đơn. Một câu trong yêu cầu, tránh được bốn cảnh báo sai. |
| **3:05** | **③ SOÁT NGẪU NHIÊN** — Dán PROMPT 3. Claude chọn 3 hóa đơn ngẫu nhiên, in bảng so sánh "PDF ↔ Excel" | Bước ba. Đừng tin một trăm phần trăm. Bảo Claude chọn ngẫu nhiên ba hóa đơn, rồi tự mình mở PDF ra so. Mất ba mươi giây, đổi lại sự yên tâm. |
| 3:20 | Split screen PDF / dòng Excel, tick xanh từng trường | Khớp, khớp, khớp. |
| **3:30** | **MẸO PRO** — Kéo thả một ảnh chụp hóa đơn (jpg) vào ô chat | Mẹo mình hứa: nếu hóa đơn là **ảnh chụp** thay vì PDF có chữ thì sao? Script không đọc được, nhưng Claude **nhìn** được ảnh. Kéo ảnh vào, bảo nó đọc. |
| 3:50 | `⚠️ TEXT: Ảnh chụp → BẮT BUỘC soát lại 100%` | Nhưng với ảnh, hãy soát lại toàn bộ, vì đọc bằng mắt, dù của người hay của máy, đều có thể nhầm. |
| 4:05 | `⚠️ TEXT: Dữ liệu thật → tuân thủ quy định bảo mật của đơn vị` | Và một lưu ý nghiêm túc: hóa đơn thật là dữ liệu kinh doanh. Trước khi đưa vào bất kỳ công cụ AI nào, hãy chắc chắn công ty bạn cho phép. |
| 4:20 | Tóm tắt: `Trích bằng script` · `Kiểm tra chéo bằng quy tắc` · `Soát ngẫu nhiên` | Ba bước: trích bằng script, kiểm tra chéo bằng quy tắc, và soát ngẫu nhiên. |
| 4:30 | `TEXT: BÀI TẬP: 5 hóa đơn điện tử thật của bạn (PDF) → Excel` | Bài tập: tải năm hóa đơn điện tử của chính bạn, thử ngay. |
| 4:38 | Teaser: 40 thư mời Word xếp chồng, mỗi cái một tên + Outlook mở 40 thư nháp | Tập sau: bốn mươi thư mời, tên ai người nấy, kèm sẵn bốn mươi email nháp trong Outlook. Bạn chỉ việc bấm gửi. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (trích xuất)
```text
@hoa-don/ có 30 hóa đơn PDF của tháng 9 từ nhiều nhà cung cấp, bố cục khác nhau.
Viết script Python trich_hoa_don.py (dùng pdfplumber) để trích ra hoa-don-thang-9.xlsx:
- Sheet Hoa-don: Tên file | Nhà cung cấp | MST | Ký hiệu | Số HĐ | Ngày | Tiền hàng | Thuế suất | Tiền thuế | Tổng thanh toán
- Sheet Chi-tiet: Số HĐ | Tên hàng | ĐVT | SL | Đơn giá | Thành tiền
Dùng script để trích, KHÔNG đọc rồi gõ lại bằng tay. Mở thử vài file trước để nhận diện các bố cục.
Số tiền lưu dạng số, định dạng 1.000.000.
```

**PROMPT 2** (kiểm tra chéo)
```text
Thêm sheet Can-kiem-tra, đánh dấu mọi hóa đơn vi phạm một trong các quy tắc:
1. Tiền hàng ≠ tổng thành tiền các dòng hàng
2. Tiền thuế ≠ Tiền hàng × Thuế suất (cho phép lệch làm tròn ≤ 1 đ)
3. Tổng thanh toán ≠ Tiền hàng + Tiền thuế
4. Trùng hóa đơn = trùng cả MST nhà cung cấp VÀ Ký hiệu VÀ Số HĐ (chỉ trùng số thì KHÔNG tính)
Mỗi dòng ghi rõ: file, quy tắc vi phạm, chênh lệch bao nhiêu. Cuối cùng cho biết tổng chênh lệch.
```

**PROMPT 3** (soát ngẫu nhiên)
```text
Chọn ngẫu nhiên 3 hóa đơn hợp lệ. Với mỗi hóa đơn, in bảng so sánh: giá trị trong PDF gốc
(trích lại trực tiếp) và giá trị trong Excel, theo từng trường.
```

## Đối chiếu (dap-an.json)

| Chỉ số | Giá trị |
|---|---|
| Số file / hóa đơn duy nhất | 30 / 29 |
| Tổng thanh toán đúng (29 HĐ) | 261.591.460 đ |
| Tổng theo số ghi trên HĐ | 261.601.460 đ (lệch +10.000 đ) |
| Nếu nhập cả bản trùng | 273.151.460 đ |
| Có vấn đề | `HD_1C25TPN_00000177.pdf` (+100.000 đ) · `HD_1C25TBL_00000246.pdf` (−90.000 đ, đảo chữ số) · `scan_7269.pdf` (trùng 1C25TPN-00000200) |
| Bẫy "trùng số khác NCC" | 224, 230, 251, 304 |

## Gói đăng tải

- **Tiêu đề:**
  - A: `30 hóa đơn PDF → Excel trong 2 phút, AI bắt được 3 hóa đơn sai | Tự động hóa với Claude #3`
  - B: `Kế toán ơi, đừng nhập hóa đơn bằng tay nữa (Claude + VS Code)`
- **Thumbnail:** Chồng hóa đơn, 3 tờ có dấu X đỏ. Chữ: **"3 HÓA ĐƠN SAI"**, nhỏ hơn: "chỉ lệch 10.000đ".
- **Shorts:** (1) 2:10–2:52 "Hai lỗi che nhau còn đúng 10 nghìn", (2) 2:52–3:05 "Trùng số ≠ trùng hóa đơn".
- **Bình luận ghim:** 3 prompt + "Bạn đang nhập bao nhiêu hóa đơn mỗi tháng?"
