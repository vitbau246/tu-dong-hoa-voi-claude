# Tập 1: Dọn 318 file lộn xộn, không mất một file (hoàn tác được 100%)

> **Kết quả lần chạy thật 02/11/2026 (Claude Code 2.1.312, dùng để dựng video):** lập kế hoạch 107 giây + thực hiện 520 giây (khoảng 10,5 phút, phần lớn là Claude tự kiểm tra trên bản sao). 318/318 file, 27 nhóm trùng, 0 file xóa. Hai chi tiết thật đã đưa vào video: (1) Claude hỏi lại chỗ mơ hồ "tên gọn nhất" trong prompt; (2) phần mềm diệt virus khóa file ở 242/318, Claude dùng `hoan-tac.ps1` khôi phục rồi chạy lại. **Bỏ mọi câu "1 phút".** Dữ liệu gốc: `video/du-lieu-that/tap-01/`. Video: `video/xuat/tap-01*.mp4`.

| | |
|---|---|
| **Mục tiêu người xem** | Cài xong Claude Code trong VS Code, chạy được tác vụ tự động đầu tiên một cách an toàn |
| **Tính năng dạy** | Cài extension, mở Claude, chế độ **Plan**, file hoàn tác (vì Rewind không hoàn tác lệnh di chuyển file) |
| **Thời lượng** | 5:00 |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/Downloads` (318 file, 27 bản trùng nội dung). Đáp án nằm trong `dap-an.json` |

## Chuẩn bị trước khi quay

1. `python chuan-bi.py`. Chạy lại lệnh này trước **mỗi lần quay lại cảnh**.
2. VS Code: **File → Open Folder → `tap-01-don-dep-downloads/demo`**. Áp dụng cấu hình quay phim trong `00-chien-luoc/04-thiet-lap-quay.md`.
3. Gỡ extension Claude Code nếu muốn quay cảnh cài đặt thật, hoặc quay cảnh cài trên máy/profile sạch (`code --profile quay-phim`).
4. Mở sẵn File Explorer của Windows ở `demo/Downloads`, chế độ xem *Details*, để làm cảnh "trước".
5. ⚠️ Các con số thời gian trên màn hình ("58 giây", "1 phút") là **chỗ trống**. Thay bằng thời gian thật đo được ở lần quay dùng để dựng. Nếu lần chạy thật lâu hơn 1 phút, đổi tiêu đề thành "trong 2 phút".

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Màn hình chia đôi. Trái: File Explorer cuộn qua 318 file lộn xộn. Phải: cây thư mục gọn gàng sau khi dọn. `TEXT: 318 file → 7 thư mục · 58 giây` | Thư mục Downloads của bạn có bao nhiêu file? Của mình là ba trăm mười tám. |
| 0:05 | Zoom vào thư mục `_Trung-lap`. `TEXT: 27 file trùng — dù khác tên` | Một phút sau, mọi thứ vào đúng chỗ. Và AI còn tìm ra hai mươi bảy file trùng, kể cả những file bị đổi tên. |
| 0:12 | Người dẫn (hoặc chữ lớn) | Hôm nay mình sẽ cài Claude vào VS Code và cho nó làm việc đầu tiên. Quan trọng hơn, mình sẽ chỉ bạn cách để AI **không bao giờ** làm mất file của bạn. Mẹo đó nằm ở cuối video. |
| 0:25 | Logo series + thanh 3 bước: `① Cài đặt ② Lập kế hoạch ③ Kiểm chứng & hoàn tác` | Ba bước, năm phút. Bắt đầu. |
| **0:30** | **① CÀI ĐẶT** — VS Code, nhấn `Ctrl+Shift+X`, gõ "Claude Code", chọn bản của **Anthropic**, Install | Mở VS Code, nhấn Ctrl Shift X, tìm "Claude Code". Chọn đúng bản của Anthropic rồi bấm Install. |
| 0:42 | Bấm biểu tượng tia lửa góc trên phải → đăng nhập trình duyệt `[TUA x4]`. `TEXT: Cần gói Claude Pro trở lên` | Bấm vào biểu tượng tia lửa rồi đăng nhập tài khoản Claude. Lưu ý: bạn cần gói Pro trở lên, gói miễn phí không dùng được Claude Code. |
| 0:55 | File → Open Folder → chọn thư mục `demo`. Cây thư mục hiện bên trái | Bước quan trọng nhất là mở đúng thư mục. Claude chỉ làm việc trong thư mục bạn mở, nên mình mở thư mục chứa bản sao Downloads. |
| 1:05 | `⚠️ TEXT: Luôn làm trên BẢN SAO trong lần đầu` | Lần đầu thử, hãy làm trên bản sao. Thói quen này rẻ mà cứu bạn nhiều lần. |
| **1:12** | **② LẬP KẾ HOẠCH** — Zoom vào chỉ báo chế độ dưới ô nhập, chọn **Plan** | Giờ đến bí quyết thứ nhất. Đừng để AI làm ngay. Chuyển sang chế độ **Plan**: Claude chỉ được đọc, lên kế hoạch, và chờ bạn duyệt. |
| 1:22 | Dán **PROMPT 1** (giữ trên màn hình 3 giây) | Mình yêu cầu: xếp file theo loại, chia theo năm, tìm file trùng **nội dung** chứ không chỉ trùng tên, không xóa gì cả, và ghi nhật ký mọi thao tác. |
| 1:35 | Claude đọc thư mục `[TUA x6]`, hiện bản kế hoạch dạng tài liệu | Claude quét ba trăm file, đọc ngày sửa đổi, tính "vân tay" của từng file để so nội dung. Rồi nó đưa ra kế hoạch. |
| 1:50 | Cuộn bản kế hoạch, highlight: bảng thư mục đích, cách so trùng bằng hash, danh sách file sẽ di chuyển | Đọc nhanh: bảy thư mục, chia theo năm. Đây là điểm hay: để tìm file trùng, nó so **hash**, tức dấu vân tay nội dung. File bị đổi tên thành "tai-ve-năm-chữ-số" vẫn bị phát hiện. |
| 2:05 | Highlight dòng về file `data (1234).csv`. `TEXT: Tên giống bản sao — nhưng KHÔNG phải` | Còn file tên "data mở ngoặc một hai ba bốn" này nhìn giống bản sao, nhưng nội dung khác nên Claude giữ nguyên. Người làm tay rất dễ xóa nhầm chỗ này. |
| 2:15 | Bấm duyệt kế hoạch (cho phép Claude tự thực hiện các bước) → Claude chạy `[TUA x8]`, đồng hồ góc phải chạy thật | Kế hoạch ổn, mình duyệt. Và giờ thì ngồi xem. |
| 2:35 | Cây thư mục trái đổi thành `Tai-lieu/2024, 2025, 2026`, `Hinh-anh/...`, `_Trung-lap`. Đồng hồ dừng ở thời gian thật. `SFX: ding` | Xong. Bảy thư mục, chia theo năm, hai mươi bảy bản trùng nằm riêng một chỗ, chưa file nào bị xóa. |
| **2:45** | **③ KIỂM CHỨNG & HOÀN TÁC** — Mở `nhat-ky-don-dep.csv`: cột tên cũ, đường dẫn mới, lý do | Đừng tin AI, hãy kiểm tra AI. Mọi thao tác nằm trong file nhật ký này: file nào, từ đâu, đến đâu, vì sao. |
| 3:00 | Gõ PROMPT 2: hỏi đối chiếu số lượng. Claude trả lời: tổng trước = tổng sau = 318 | Mình hỏi thêm một câu: tổng số file trước và sau có khớp không? Ba trăm mười tám, khớp. Không mất file nào. |
| 3:15 | Mở terminal (`` Ctrl+` ``), chạy `powershell -ExecutionPolicy Bypass -File .\hoan-tac.ps1` → cây thư mục trở về lộn xộn như cũ `[TUA x4]` | Còn đây là cái mình thích nhất: file hoàn tác. Chạy nó, và mọi thứ trở về đúng như ban đầu. Một trăm phần trăm. |
| 3:30 | Chạy lại lệnh dọn (hoặc cắt sang kết quả đã dọn) | Yên tâm rồi thì mình làm lại, lần này là thật. |
| **3:40** | **MẸO PRO** — Hover lên một tin nhắn, hiện nút Rewind. `TEXT: Rewind ≠ hoàn tác mọi thứ` | Đây là bí mật mình hứa ở đầu video. Claude có nút **Rewind** để tua lại. Nhưng nó chỉ khôi phục những file mà Claude **sửa nội dung**. Thao tác di chuyển hay xóa bằng lệnh thì Rewind **không** đưa về được. |
| 4:00 | Tóm tắt 3 dòng trên màn hình: `Plan trước khi làm` · `Không xóa — chỉ di chuyển` · `Luôn đòi nhật ký + file hoàn tác` | Vì thế, với mọi việc động tới nhiều file, hãy nhớ công thức ba câu: lập kế hoạch trước, không xóa mà chỉ di chuyển, và luôn đòi nhật ký kèm file hoàn tác. Thêm ba câu này vào prompt là bạn có lưới an toàn. |
| 4:25 | `TEXT: BÀI TẬP: dọn thư mục Desktop của bạn (trên bản sao!)` | Bài tập năm phút: copy thư mục Desktop của bạn ra một chỗ khác, rồi cho Claude dọn bằng đúng công thức này. |
| 4:35 | Teaser: 12 file Excel lộn xộn chạy vào một bảng có biểu đồ | Tập sau: mười hai file Excel, mỗi file một kiểu, có cả bốn cách viết chữ "Hà Nội", gộp thành một báo cáo có biểu đồ, không cần một công thức nào. |
| 4:50 | Màn hình kết: đăng ký + link tải file mẫu | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. Hẹn gặp ở tập hai. |

## Prompt dùng trong tập

**PROMPT 1** (chế độ Plan)
```text
Thư mục Downloads này rất lộn xộn. Hãy lập kế hoạch dọn dẹp:
1. Xếp file vào các thư mục theo loại: Tai-lieu (pdf, docx, txt), Bang-tinh (xlsx, csv),
   Trinh-chieu (pptx), Hinh-anh (png, jpg), Nen (zip), Cai-dat (exe, msi), Media (mp4, m4a).
2. Trong mỗi thư mục, chia tiếp theo NĂM của ngày sửa đổi cuối cùng.
3. Tìm file trùng NỘI DUNG (so hash, không dựa vào tên). Giữ bản có tên gọn nhất,
   chuyển các bản thừa vào thư mục _Trung-lap.
4. TUYỆT ĐỐI không xóa file nào, chỉ di chuyển.
5. Ghi mọi thao tác vào nhat-ky-don-dep.csv (ten_cu, duong_dan_moi, ly_do)
   và tạo hoan-tac.ps1 để đưa mọi thứ về như cũ.
Chỉ lập kế hoạch, chưa thực hiện.
```

**PROMPT 2** (kiểm chứng)
```text
Đếm lại: tổng số file trước khi dọn và sau khi dọn (gồm cả _Trung-lap) có khớp không?
Liệt kê 5 nhóm file trùng làm ví dụ.
```

## Đối chiếu (dap-an.json)

- Tổng **318** file, **27** bản sao thừa trùng nội dung (27 nhóm).
- Phân bổ theo năm sửa đổi: xem `theo_nam_sua_doi` trong `dap-an.json`. Lời thoại không đọc số theo năm, nên quay lại bao nhiêu lần cũng không bị lệch.
- Bẫy: các file `data (xxxx).csv` **không** phải bản sao.

## Xử lý sự cố khi quay

| Tình huống | Cách xử lý |
|---|---|
| PowerShell chặn chạy script | Dùng `powershell -ExecutionPolicy Bypass -File .\hoan-tac.ps1` |
| Claude định xóa file trùng | Nhắc lại "không xóa, chỉ di chuyển" (đã có trong prompt). Đây cũng là chất liệu tốt để dẫn sang tập 6 về Hooks |
| Claude dùng `LastAccessTime` thay vì `LastWriteTime` | Bổ sung vào prompt: "ngày sửa đổi = LastWriteTime" |

## Gói đăng tải

- **Tiêu đề (thử A/B):**
  - A: `Dọn 318 file lộn xộn bằng Claude + VS Code: không mất một file (có cả sự cố thật)`
  - B: `AI tìm ra 27 file trùng mà mình không biết | Tự động hóa với Claude #1`
- **Thumbnail:** Trái là Explorer đỏ rực "318 FILE". Mũi tên. Phải là 7 thư mục xanh. Chữ lớn: **"0 FILE MẤT"**. Góc nhỏ: logo VS Code + Claude.
- **Mô tả (đoạn đầu):** Cài Claude Code vào VS Code và dọn sạch thư mục Downloads bằng một yêu cầu, có kế hoạch duyệt trước, nhật ký và file hoàn tác để không bao giờ mất dữ liệu. ⏱ 0:30 Cài đặt · 1:12 Lập kế hoạch · 2:45 Hoàn tác · 3:40 Bí mật về Rewind. Yêu cầu: VS Code ≥ 1.94, gói Claude Pro/Max/Team/Enterprise. Phiên bản dùng trong video: Claude Code 2.1.312.
- **Bình luận ghim:** Prompt 1 đầy đủ + link tải file mẫu + câu hỏi "Downloads của bạn có bao nhiêu file? 👇"
- **Shorts cắt ra:** (1) 2:05–2:35 "Bẫy file trông như bản sao", (2) 3:40–4:20 "Rewind không cứu được bạn trong trường hợp này".
