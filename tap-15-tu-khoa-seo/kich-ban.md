# Tập 15: Nghiên cứu từ khóa SEO từ dữ liệu thật: tìm "mỏ vàng" sát trang 1

| | |
|---|---|
| **Mục tiêu người xem** | Dùng dữ liệu **Google Search Console** của chính website để tìm cơ hội SEO nhanh nhất, phân tích đối thủ top đầu, ra content brief và kế hoạch nội dung |
| **Tính năng dạy** | Claude phân tích CSV, quy tắc định lượng (sát trang 1 / CTR thấp / tự cạnh tranh), WebFetch phân tích trang đối thủ, skill `/brief-seo`. Nói rõ giới hạn: **Claude không có dữ liệu lượng tìm kiếm**, và WebSearch ≠ Google Việt Nam |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/gsc/` (Queries.csv, Pages.csv đúng định dạng nút Export + truy-van-theo-trang.csv kiểu API), `website.md`. `--giai-phap` chép `phan-tich-gsc.py` + skill `brief-seo` |
| **Đã kiểm thử** | Script tìm ra: **6** từ khóa sát trang 1 (lớn nhất: "ghế công thái học", vị trí 11,2, 18.400 hiển thị, +934 click) · **2** top 3 CTR thấp ("giấy a4 double a giá": vị trí 2,8, CTR 1,1%, **+901 click chỉ nhờ đổi tiêu đề**) · **1** tự cạnh tranh ("bàn làm việc chân sắt", 2 trang vị trí 9,6 và 12,9) |

## Chuẩn bị

1. `python chuan-bi.py --giai-phap`, mở `tap-15-tu-khoa-seo/demo`.
2. Bước 2 cần 5 URL top Google cho "ghế công thái học": mở Edge ở **chế độ InPrivate**, tìm trên google.com.vn, copy 5 URL kết quả tự nhiên (bỏ quảng cáo) vào Notepad.
3. Muốn dùng dữ liệu thật: Search Console → Hiệu suất → 3 tháng → Xuất → CSV. Có thể bổ sung file truy vấn × trang từ Looker Studio.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Excel `co-hoi-seo.xlsx`, sheet CTR-thap: dòng "giấy a4 double a giá · vị trí 2,8 · CTR 1,1% · +901 click" phát sáng | Website này đang đứng top 3 Google cho từ khóa "giấy A4 Double A giá", nhưng gần như không ai bấm vào. |
| 0:07 | `TEXT: Sửa 1 dòng tiêu đề = +900 click / 3 tháng` | Chỉ cần sửa một dòng tiêu đề, thêm chín trăm lượt truy cập. Không cần viết bài mới. |
| 0:13 | Người dẫn | Ai làm SEO cũng muốn biết nên viết gì. Nhưng câu trả lời tốt nhất không nằm ở công cụ đắt tiền, mà nằm trong **dữ liệu Google đã cho bạn miễn phí**: Search Console. Hôm nay Claude đào ba loại "mỏ vàng" trong đó, rồi phân tích đối thủ và lập luôn kế hoạch nội dung. |
| 0:30 | Thanh 3 bước: `① Đào mỏ vàng Search Console ② Mổ xẻ top 5 Google ③ Brief + kế hoạch 4 tuần` | |
| **0:33** | **① ĐÀO MỎ VÀNG** — Search Console → Hiệu suất → Xuất CSV (cảnh minh họa). Cây `gsc/` 3 file | Bước một: xuất dữ liệu ba tháng từ Search Console. Đây là dữ liệu thật về những gì người ta gõ trên Google trước khi thấy website của bạn. |
| 0:48 | Dán PROMPT 1 → Claude đọc CSV, áp 3 quy tắc, xuất Excel `[TUA x6]` | Mình yêu cầu Claude tìm ba thứ theo quy tắc định lượng rõ ràng, không theo cảm tính. |
| 1:00 | Sheet "Sat-trang-1": "ghế công thái học · 11,2 · 18.400 · +934" | Mỏ vàng thứ nhất: từ khóa **sát trang một**. "Ghế công thái học" đang ở vị trí mười một, ngay đầu trang hai, với mười tám nghìn lượt hiển thị. Người ta hầu như không bao giờ lật sang trang hai. Đẩy lên vị trí năm là thêm khoảng chín trăm click. Và đúng nhóm hàng lãi cao nhất của công ty. |
| 1:22 | Sheet "CTR-thap" (cảnh mở đầu) | Mỏ vàng thứ hai: **top ba mà không ai bấm**. Thường do tiêu đề nhàm chán, hoặc mô tả không nói giá trong khi người ta đang tìm giá. |
| 1:35 | Sheet "Tu-canh-tranh": 2 URL cùng "bàn làm việc chân sắt". Mũi tên nối sang dòng đó ở sheet Sat-trang-1 | Mỏ vàng thứ ba, khó thấy nhất: hai trang của **chính mình** tranh nhau một từ khóa. Google không biết chọn trang nào, nên cả hai cùng kẹt ở trang hai. Nhìn sang sheet đầu: "bàn làm việc chân sắt" cũng đang sát trang một. Nó bị kẹt **chính vì** tự cạnh tranh. |
| 1:58 | `TEXT: Gộp hoặc phân vai: 1 trang bán hàng + 1 bài hướng dẫn liên kết sang` | Cách chữa: gộp hai trang, hoặc phân vai rõ ràng: một trang bán, một bài hướng dẫn trỏ liên kết sang trang bán. |
| **2:08** | **② MỔ XẺ TOP 5** — `⚠️ TEXT: Kết quả tìm kiếm của Claude ≠ trang Google người Việt thấy` | Bước hai, và một điều phải nói thật: công cụ tìm kiếm của Claude **không phải** Google Việt Nam. Thứ hạng sẽ khác. Nên mình tự tìm trên Google ở chế độ ẩn danh, copy năm kết quả đầu. Mất ba mươi giây. |
| 2:25 | Gõ `/brief-seo ghế công thái học <5 URL>` → Claude WebFetch từng trang, bảng phân tích `[TUA x8]` | Rồi gọi lệnh brief-SEO kèm năm đường dẫn. Claude đọc từng trang đối thủ: loại trang, độ dài, các đề mục, điểm mạnh, điểm thiếu. |
| 2:45 | Zoom mục "Ý định tìm kiếm: Cân nhắc, 4/5 trang top là bài so sánh/hướng dẫn chọn" | Phát hiện quan trọng: phần lớn trang top là **bài hướng dẫn chọn mua**, không phải trang bán hàng. Nghĩa là người tìm "ghế công thái học" đang cân nhắc chứ chưa mua ngay. Trang sản phẩm của mình đứng thứ mười một là hợp lý: **sai loại nội dung**. |
| 3:05 | Zoom "Khoảng trống ★": ví dụ "chọn ghế theo chiều cao người Việt", "bảo hành và đổi trả" | Và khoảng trống: những câu người mua cần mà gần như không trang nào trả lời tốt. Đây là chỗ mình vượt mặt đối thủ. |
| **3:18** | **③ BRIEF + KẾ HOẠCH** — Mở `brief/ghe-cong-thai-hoc.md`: 3 tiêu đề ≤ 60 ký tự, dàn ý H2/H3 có ★, FAQ, liên kết nội bộ | Kết quả là một bản brief hoàn chỉnh: ba phương án tiêu đề, dàn ý chi tiết, câu hỏi thường gặp, liên kết nội bộ. Người viết, dù là người hay AI, cầm vào là viết được ngay. |
| 3:35 | Dán PROMPT 3 → `ke-hoach-noi-dung.xlsx`: 4 tuần × 2 bài, cột từ khóa/ý định/loại trang/việc cần làm, có dòng "Viết lại title trang giấy A4" ở tuần 1 | Cuối cùng: kế hoạch bốn tuần, đúng sức đội một người, hai bài một tuần. Tuần đầu ưu tiên việc **rẻ nhất mà hiệu quả nhất**: sửa tiêu đề trang giấy A4, gộp hai trang bàn làm việc. |
| **3:55** | **MẸO PRO** — `TEXT: Claude KHÔNG biết lượng tìm kiếm. Đừng tin con số "volume" AI tự đưa` | Mẹo quan trọng nhất của tập: Claude **không có** dữ liệu lượng tìm kiếm. Nếu AI nào đó tự đưa ra "từ khóa này mười nghìn lượt mỗi tháng" mà không có nguồn, đừng tin. Dữ liệu thật nằm trong Search Console, Google Keyword Planner, hoặc công cụ như Ahrefs. Xuất file từ đó, đưa cho Claude phân tích. |
| 4:15 | Tóm tắt: `Search Console = mỏ vàng miễn phí` · `Top 5 thật từ Google ẩn danh` · `Ý định tìm kiếm quyết định loại trang` | |
| 4:28 | `TEXT: BÀI TẬP: xuất Search Console của bạn → tìm 1 từ khóa vị trí 8–20` | Bài tập: xuất Search Console của website bạn, tìm một từ khóa ở vị trí tám đến hai mươi. Đó là bài viết tiếp theo của bạn. |
| 4:38 | Teaser: bài viết hiện ra, góc phải "Điểm SEO: 72 → 96" | Có brief rồi, tập sau Claude viết bài. Và mỗi lần viết xong, một "giám khảo" tự động chấm điểm SEO, chưa đạt thì Claude **tự sửa** đến khi đạt. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1**
```text
@gsc/ là dữ liệu Search Console 3 tháng của website (@website.md). Tìm 3 loại cơ hội, xuất co-hoi-seo.xlsx (mỗi loại 1 sheet):
1. Sát trang 1: vị trí TB 8–20 và hiển thị ≥ 2.000. Ước tính click tiềm năng nếu lên vị trí 5 (CTR chuẩn ~6,5%).
2. CTR thấp: vị trí ≤ 5 nhưng CTR < 40% CTR chuẩn của vị trí đó (1: 28%, 2: 16%, 3: 11%, 4: 8%, 5: 6,5%).
3. Tự cạnh tranh: ≥ 2 trang cùng một truy vấn, mỗi trang ≥ 500 hiển thị (dùng truy-van-theo-trang.csv).
Viết script Python để tính (không tính nhẩm). Tóm tắt 3 ưu tiên số 1, có liên hệ với mục tiêu trong website.md.
```

**PROMPT 2**
```text
/brief-seo ghế công thái học https://... https://... https://... https://... https://...
```

**PROMPT 3**
```text
Từ co-hoi-seo.xlsx và brief vừa làm, lập ke-hoach-noi-dung.xlsx 4 tuần, 2 đầu việc/tuần (đội 1 người):
cột Tuần | Từ khóa | Ý định | Loại trang | Việc cần làm (viết mới / viết lại tiêu đề-mô tả / gộp trang / tối ưu) | Click tiềm năng | Lý do ưu tiên.
Tuần 1 ưu tiên việc tốn ít công nhất mà nhiều click tiềm năng nhất.
```

## Gói đăng tải

- **Tiêu đề:** A: `Nghiên cứu từ khóa SEO bằng AI + Search Console: 3 mỏ vàng bị bỏ quên | Claude nâng cao #15` · B: `Top 3 Google mà không ai bấm? Sửa 1 dòng = +900 click`
- **Thumbnail:** Kết quả Google vị trí 11 với mũi tên vọt lên. Chữ: **"SÁT TRANG 1"**.
- **Shorts:** (1) 1:35–2:08 "Hai trang của mình tự đánh nhau", (2) 3:55–4:15 "AI không biết volume từ khóa".
