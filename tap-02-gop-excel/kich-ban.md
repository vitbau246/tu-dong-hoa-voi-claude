# Tập 2: Gộp 12 file Excel thành báo cáo có biểu đồ, không cần một công thức

| | |
|---|---|
| **Mục tiêu người xem** | Biết cách để Claude **khảo sát → làm sạch → tổng hợp → tự kiểm tra** dữ liệu Excel |
| **Tính năng dạy** | Gọi thư mục bằng `@`, Claude tự viết và chạy script Python, đòi "nhật ký làm sạch", lưu script để dùng lại |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/du-lieu/` (12 file, 7 kiểu lỗi). Đáp án trong `dap-an.json` |
| **Con số chốt** | Tổng đúng **10,63 tỷ** · Nếu cộng SUM thẳng sẽ ra **13,18 tỷ** (sai **2,55 tỷ**) · 15 dòng trùng ở T8 · Tháng cao nhất: T12 |

## Chuẩn bị

1. `python chuan-bi.py`, sau đó mở thư mục `tap-02-gop-excel/demo` trong VS Code.
2. Máy cần Python. Nếu Claude hỏi cài `pandas`/`openpyxl`, cứ đồng ý. Nên cài sẵn trước khi quay để tránh mất thời gian: `pip install pandas openpyxl`.
3. Chế độ quyền: **Manual** ở bước 1 (để thấy Claude chỉ đọc), sau đó chuyển **Edit automatically** ở bước 2.
4. Mở sẵn 3 file trong Excel để quay cảnh "lộn xộn": `BC T3 (final).xlsx` (có dòng tiêu đề), `T5_2025.xlsx` (số dạng chữ), `BC_T07_2025.xlsx` (cột khác thứ tự).

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Cận màn hình Excel: ô SUM hiện **13.178.585.000**. Gạch đỏ. Bên cạnh hiện **10.625.890.000** màu xanh. `TEXT: Lệch 2,55 tỷ` | Hai con số này cùng là doanh thu năm của một công ty. Một con số sai hai tỷ rưỡi. |
| 0:06 | Lướt nhanh 12 tên file: "BC T3 (final)", "BC T9 (final) (1)", "Ban hang T6 - gui chi Lan"... | Và cái sai đó nằm trong mười hai file Excel trông rất bình thường này. |
| 0:12 | Người dẫn | Hôm nay Claude sẽ gộp chúng thành một báo cáo có biểu đồ, và quan trọng hơn, **tìm ra vì sao** con số kia sai. Cuối video có một mẹo để tháng sau bạn làm lại việc này chỉ trong mười giây. |
| 0:25 | Thanh 3 bước: `① Khảo sát ② Gộp & làm sạch ③ Tự kiểm tra` | |
| 0:28 | Lật nhanh 3 file Excel đã mở sẵn, khoanh đỏ từng lỗi: dòng tiêu đề thừa · "1.250.000" căn trái (là chữ) · cột bị đổi thứ tự | Ai từng tổng hợp báo cáo từ nhiều người đều biết cảnh này: file thì có dòng tiêu đề, file thì số tiền lưu dạng chữ, file thì cột bị đảo. Làm tay mất cả buổi chiều. |
| **0:45** | **① KHẢO SÁT** — VS Code, chế độ **Manual**. Gõ `@du-lieu/` rồi dán PROMPT 1 | Bước một: đừng bảo AI làm ngay. Bảo nó **khảo sát** trước. Mình gõ a-còng du-liệu để chỉ đúng thư mục, và yêu cầu: đọc hết mười hai file, liệt kê mọi điểm không nhất quán, chưa sửa gì. |
| 1:00 | Claude đọc từng file `[TUA x6]` | |
| 1:12 | Kết quả khảo sát hiện dạng danh sách. Highlight lần lượt từng dòng, mỗi dòng một tiếng "tick". `SFX: tick ×7` | Và đây là danh sách nó tìm ra. Hai kiểu tên cột. Hai file có dòng tiêu đề phía trên. Ngày tháng lưu dạng chữ ở tháng hai và mười một. Số tiền dạng chữ ở tháng năm và mười. Bốn file có dòng **Tổng cộng** ở cuối. Mười lăm dòng bị dán trùng ở tháng tám. |
| 1:35 | Zoom vào dòng chi nhánh: `"Hà Nội", "Ha Noi", "HN", "hà nội "` | Và cái mình thích nhất: chi nhánh Hà Nội được viết **bốn kiểu**, kể cả một kiểu có dấu cách thừa ở cuối mà mắt thường không thể thấy. |
| **1:50** | **② GỘP & LÀM SẠCH** — Chuyển chế độ **Edit automatically**. Dán PROMPT 2 | Bước hai. Giờ mới cho làm. Mình yêu cầu một file tổng hợp có bốn sheet: dữ liệu sạch, tổng hợp theo tháng và chi nhánh, top năm sản phẩm kèm biểu đồ, và một sheet **nhật ký làm sạch** ghi rõ đã sửa những gì. |
| 2:05 | Claude viết `gop_bao_cao.py`, chạy, sửa lỗi nhỏ nếu có `[TUA x8]`, đồng hồ góc phải | Claude không "đoán" kết quả. Nó viết một đoạn script rồi tự chạy. Nếu script lỗi, nó đọc lỗi và tự sửa. Bạn không cần biết Python. |
| 2:30 | Mở `tong-hop-2025.xlsx` trong Excel: lướt 4 sheet, dừng ở biểu đồ cột doanh thu 12 tháng, T12 cao nhất | Đây là kết quả. Một nghìn ba trăm chín mươi tám giao dịch sạch. Bảng tháng nhân chi nhánh. Biểu đồ cho thấy tháng mười hai bán mạnh nhất. |
| 2:50 | Sheet `Nhat-ky-lam-sach` | Và sheet nhật ký: sếp hỏi "số này ở đâu ra", bạn có câu trả lời ngay. |
| **3:00** | **③ TỰ KIỂM TRA** — Dán PROMPT 3 | Bước ba, bước mà chín mươi phần trăm người dùng AI bỏ qua: bắt nó **tự kiểm tra**. Mình hỏi: nếu ai đó mở mười hai file rồi cộng SUM thẳng cột tiền thì ra bao nhiêu, lệch bao nhiêu, vì sao? |
| 3:15 | Claude trả lời: 13,18 tỷ so với 10,63 tỷ, giải thích 3 nguyên nhân. Hiện đồ họa 3 mũi tên: `+ dòng trùng T8` · `+ 4 dòng TỔNG CỘNG` · `− T5, T10 bị bỏ sót vì số dạng chữ` | Mười ba phẩy mười tám tỷ so với mười phẩy sáu ba tỷ. Lệch hai tỷ rưỡi. Bị cộng thừa dòng trùng và các dòng tổng cộng, nhưng lại **thiếu** hai tháng vì SUM bỏ qua ô chứa chữ. Hai lỗi ngược chiều che cho nhau, nên con số sai trông vẫn rất "hợp lý". |
| 3:40 | `⚠️ TEXT: Luôn hỏi "đối chiếu bằng cách khác"` | Đó là lý do câu "hãy đối chiếu bằng một cách khác" nên có trong mọi yêu cầu liên quan đến tiền. |
| **3:50** | **MẸO PRO** — Cây thư mục: `gop_bao_cao.py`. Gõ PROMPT 4 | Giờ đến mẹo mình hứa. Claude vừa viết script `gop_bao_cao.py`. Mình bảo nó sửa script để nhận thư mục bất kỳ và ghi hướng dẫn lên đầu file. |
| 4:05 | Terminal: `python gop_bao_cao.py du-lieu` → chạy xong trong 2 giây | Tháng sau có mười hai file mới? Bạn không cần hỏi AI nữa. Chỉ cần chạy lại script. Hai giây, miễn phí, kết quả giống hệt. **AI viết công cụ một lần, bạn dùng mãi mãi.** |
| 4:25 | `TEXT: BÀI TẬP: gộp 2-3 file Excel thật của bạn (bản sao) — nhớ bước KHẢO SÁT` | Bài tập: lấy hai ba file Excel bạn hay phải gộp, làm đúng ba bước: khảo sát, gộp, tự kiểm tra. |
| 4:35 | Teaser: tập hồ sơ 30 hóa đơn PDF, 3 hóa đơn nhấp nháy đỏ | Tập sau khó hơn: ba mươi hóa đơn PDF, ba cái có vấn đề. Mắt người mất hai tiếng. Xem Claude mất bao lâu. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (chế độ Manual: khảo sát)
```text
@du-lieu/ có 12 file Excel doanh thu năm 2025 do nhiều người làm.
Hãy đọc tất cả và liệt kê MỌI điểm không nhất quán: tên/thứ tự cột, dòng tiêu đề thừa,
kiểu dữ liệu ngày và số, cách viết tên chi nhánh, dòng tổng cộng, dòng trùng lặp.
Chỉ khảo sát và báo cáo, chưa sửa hay tạo file nào.
```

**PROMPT 2** (chế độ Edit automatically: gộp và làm sạch)
```text
Dựa trên khảo sát, viết script Python gop_bao_cao.py để tạo tong-hop-2025.xlsx gồm:
1. Du-lieu-sach: Ngày | Tháng | Chi nhánh (chuẩn hóa về Hà Nội, TP.HCM, Đà Nẵng, Cần Thơ) | Sản phẩm | SL | Đơn giá | Thành tiền
2. Tong-hop: doanh thu theo tháng (dòng) x chi nhánh (cột), có tổng dòng/cột, định dạng 1.000.000
3. Top-san-pham: top 5 theo doanh thu + biểu đồ cột doanh thu 12 tháng
4. Nhat-ky-lam-sach: mỗi lỗi đã xử lý ở file nào, bao nhiêu dòng
Không sửa file gốc. Chạy script và báo tổng doanh thu cả năm.
```

**PROMPT 3** (tự kiểm tra)
```text
Đối chiếu bằng cách khác: nếu ai đó mở 12 file gốc và SUM thẳng cột tiền rồi cộng lại,
họ sẽ ra bao nhiêu? Chênh lệch so với kết quả của bạn là bao nhiêu và do những nguyên nhân nào?
```

**PROMPT 4** (mẹo pro)
```text
Sửa gop_bao_cao.py để nhận đường dẫn thư mục làm tham số dòng lệnh,
và thêm hướng dẫn sử dụng ngắn bằng tiếng Việt ở đầu file.
```

## Đối chiếu (dap-an.json)

| Chỉ số | Giá trị đúng |
|---|---|
| Số giao dịch sạch | 1.398 |
| Tổng doanh thu 2025 | 10.625.890.000 đ |
| SUM thẳng (sai) | 13.178.585.000 đ (lệch 2.552.695.000 đ) |
| Chi nhánh | TP.HCM 4.050.015.000 · Hà Nội 3.813.970.000 · Đà Nẵng 1.680.360.000 · Cần Thơ 1.081.545.000 |
| Top 1 sản phẩm | Ghế công thái học: 2.889.000.000 |
| Tháng cao nhất | T12: 1.424.840.000 |

> Đã kiểm chứng bằng một quy trình làm sạch độc lập (pandas): ra đúng 1.398 dòng, tổng 10.625.890.000 đ, khớp đáp án.

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| Claude không bỏ dòng "TỔNG CỘNG" | Hỏi "Tổng của bạn có khớp với 10,63 tỷ không? Kiểm tra lại các dòng tổng cộng". Có thể dựng thành cảnh "AI cũng sai, và đây là cách bắt lỗi" (chất liệu rất tốt) |
| Dedupe trước khi chuẩn hóa tên chi nhánh, nên chỉ bắt được ít hơn 15 dòng trùng | Nhắc "chuẩn hóa chi nhánh trước rồi mới lọc trùng" |
| Biểu đồ không hiện trong Excel | Yêu cầu dùng `openpyxl.chart.BarChart` (biểu đồ gốc của Excel) |

## Gói đăng tải

- **Tiêu đề:**
  - A: `Gộp 12 file Excel bằng AI — và phát hiện báo cáo SAI 2,5 tỷ | Tự động hóa với Claude #2`
  - B: `Đừng dùng SUM khi gộp báo cáo! Claude + VS Code gộp 12 file Excel trong 1 phút`
- **Thumbnail:** Ô Excel đỏ "13,18 tỷ" bị gạch, ô xanh "10,63 tỷ". Chữ lớn: **"SAI 2,5 TỶ"**.
- **Mô tả:** ⏱ 0:45 Khảo sát · 1:50 Gộp & làm sạch · 3:00 Tự kiểm tra · 3:50 Dùng lại mãi mãi. File mẫu 12 báo cáo trong link.
- **Bình luận ghim:** 4 prompt + câu hỏi "Bạn từng gặp kiểu lỗi nào trong 7 lỗi này?"
- **Shorts:** (1) 1:12–1:50 "4 cách viết chữ Hà Nội", (2) 3:00–3:40 "Hai lỗi che cho nhau, sai 2,5 tỷ".
