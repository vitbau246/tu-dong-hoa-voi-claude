# Tập 12: Đội nghiên cứu 5 AI: phân tích chiến lược trong 15 phút (Deep Research)

| | |
|---|---|
| **Mục tiêu người xem** | Tự dựng một quy trình "deep research": chia đề tài theo góc → nhiều subagent nghiên cứu **song song** → kiểm chứng viên soát mọi trích dẫn → báo cáo chiến lược có **ma trận độ tin cậy** |
| **Tính năng dạy** | Skill điều phối gọi subagent song song, phân vùng file để các agent không ghi đè nhau, agent kiểm chứng dùng model mạnh hơn, giới hạn 200 lượt tìm kiếm/phiên |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/de-bai-chien-luoc.md` ("Có nên mở TikTok Shop năm 2026?") + script kiểm chứng từ tập 11. `--giai-phap` chép 2 agent + skill `/nghien-cuu-sau` |
| **Lưu ý** | Nghiên cứu thật trên Internet nên kết quả và thời gian mỗi lần khác. **Chạy tập dượt 1 lần trước khi quay** để biết thời gian và chi phí hạn mức |

## Chuẩn bị

1. `python chuan-bi.py --giai-phap` (hoặc không có `--giai-phap` nếu muốn quay cảnh tạo agent), rồi mở `tap-12-doi-nghien-cuu-song-song/demo`. Mở **cuộc trò chuyện mới** sau khi có `.claude/`.
2. Tập dượt: `/nghien-cuu-sau @de-bai-chien-luoc.md`. Ghi lại thời gian, số nguồn, số trích dẫn bị gỡ để điền vào chữ trên màn hình.
3. Một lần chạy dùng khoảng 40–80 lượt tìm kiếm (giới hạn 200/phiên). Dùng `/clear` giữa các lần chạy.
4. Đặt Claude ở chế độ **Auto**, hoặc cấp sẵn quyền WebFetch, để các agent chạy song song không bị dừng chờ duyệt.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Màn hình chia 4 ô: 4 nhà nghiên cứu (TT, DT, KH, CS) đang chạy cùng lúc, mỗi ô một luồng tìm kiếm. Đồng hồ góc phải | Bốn nhà nghiên cứu đang làm việc cùng lúc. Thị trường. Đối thủ. Khách hàng. Chính sách và chi phí. |
| 0:07 | Báo cáo cuối: "Ma trận độ tin cậy" với nhãn Cao/Trung bình/Thấp, mục "Điểm vênh giữa các nguồn". `TEXT: [N] nguồn · [M] trích dẫn · đã gỡ [K] số không có nguồn` | Mười lăm phút sau: một báo cáo chiến lược, mỗi kết luận được chấm độ tin cậy, và những con số không có nguồn đã bị **gỡ bỏ**. |
| 0:15 | Người dẫn | Tập trước một Claude nghiên cứu một câu hỏi. Hôm nay là câu hỏi cỡ Ban Giám đốc: "Có nên mở TikTok Shop năm 2026?". Một người làm sẽ mất vài ngày. Mình dựng một đội năm AI, và quan trọng hơn, chỉ cho bạn **cách tổ chức** đội đó để chúng không giẫm chân lên nhau. |
| 0:32 | Thanh 3 bước: `① Thiết kế đội ② Chạy song song ③ Kiểm chứng & tổng hợp` | |
| **0:35** | **① THIẾT KẾ ĐỘI** — Sơ đồ: `Skill điều phối /nghien-cuu-sau` → `4 × nha-nghien-cuu (song song)` → `kiem-chung-vien` → `báo cáo` | Đội gồm ba vai. Một "trưởng nhóm" là skill nghiên-cứu-sâu, lo chia việc và tổng hợp. Bốn "nhà nghiên cứu" cùng một mẫu, mỗi người một góc. Và một "kiểm chứng viên" độc lập. |
| 0:52 | Mở `nha-nghien-cuu.md`: zoom "Mã đánh số `<MÃ>1, <MÃ>2…` để không trùng" + "Không sửa file của góc khác" | Bí quyết đầu tiên khi cho nhiều AI chạy cùng lúc: **mỗi người một file riêng**. Nhà nghiên cứu "TT" ghi vào nguồn-TT, đánh mã TT1, TT2. Không ai ghi đè lên ai. Đây là lỗi kinh điển khi làm việc nhóm, kể cả nhóm người. |
| 1:12 | Mở `kiem-chung-vien.md`: zoom `model: opus` + "thà thiếu còn hơn sai" | Kiểm chứng viên dùng model mạnh nhất, và chỉ có một nguyên tắc: thà thiếu còn hơn sai. Nó dùng lại đúng script kiểm chứng của tập trước. |
| 1:25 | Mở `SKILL.md` của `nghien-cuu-sau`: zoom Bước 1 "chờ đồng ý" + Bước 2 "trong CÙNG một lượt, để chạy song song" | Trưởng nhóm có hai điểm then chốt. Một: chia góc xong phải **chờ bạn đồng ý**, vì chia góc sai thì cả đội làm sai. Hai: giao việc cho tất cả **trong cùng một lượt** thì chúng mới chạy song song, nếu không sẽ chạy lần lượt. |
| **1:42** | **② CHẠY SONG SONG** — Gõ `/nghien-cuu-sau @de-bai-chien-luoc.md` → Claude đề xuất 4 góc với phạm vi và "không thuộc phạm vi" | Chạy. Trưởng nhóm đề xuất bốn góc, mỗi góc ghi rõ cái gì **không** thuộc phạm vi để các góc không chồng lấn. Ổn. Mình đồng ý. |
| 2:00 | 4 subagent chạy cùng lúc `[TUA x12]`, đồng hồ thật. Cây thư mục `nghien-cuu/tiktok-shop-2026/` lần lượt hiện `phan-TT.md`, `nguon-TT.csv`… | Bốn nhà nghiên cứu xuất phát cùng lúc. Mỗi người có bộ nhớ riêng, đọc vài chục trang mà không làm rối cuộc trò chuyện chính. File kết quả hiện ra lần lượt. |
| 2:22 | Mở `phan-CS.md` mục "Điểm vênh": ví dụ hai nguồn nêu mức phí khác nhau | Xem góc chính sách và chi phí: nó ghi lại cả **điểm vênh**, hai nguồn nói hai mức phí khác nhau. Với người ra quyết định, biết chỗ nào chưa chắc chắn quan trọng không kém biết chỗ nào chắc chắn. |
| **2:38** | **③ KIỂM CHỨNG & TỔNG HỢP** — Kiểm chứng viên chạy script trên mọi `nguon-*.csv` → bảng: góc / trích dẫn / đã sửa / đã gỡ | Kiểm chứng viên vào việc: chạy script trên tất cả file nguồn, sửa trích dẫn gần đúng, và **gỡ** những con số không tìm thấy trong nguồn. |
| 2:55 | Zoom danh sách "những con số đã gỡ" | Đây là danh sách số liệu bị gỡ. Nếu không có bước này, chúng đã nằm trong báo cáo gửi Ban Giám đốc. |
| 3:05 | Mở `bao-cao-chien-luoc.md`: "Trả lời ngắn" → "Ma trận độ tin cậy" → "Rủi ro và câu hỏi còn bỏ ngỏ → đề xuất cách trả lời" | Báo cáo cuối: trả lời ngắn ba câu. Ma trận độ tin cậy: kết luận nào có hai nguồn gốc độc lập thì "Cao", chỉ một nguồn thì "Thấp". Và phần mình thích nhất: những câu hỏi AI **không** trả lời được, kèm đề xuất cách tìm câu trả lời, như khảo sát khách hàng hay hỏi chuyên gia. |
| 3:28 | `TEXT: AI giỏi nhất khi nói rõ điều nó KHÔNG biết` | Một báo cáo tốt không phải báo cáo trả lời mọi thứ, mà là báo cáo nói rõ điều gì chưa biết. |
| **3:38** | **MẸO PRO** — Bảng 3 dòng: `Song song: nhanh hơn ~3–4 lần` · `Chi phí: ~4–5 lần hạn mức một người` · `Giới hạn: 200 lượt tìm/phiên, dùng chung cả đội` | Nói thật về chi phí: năm AI thì tốn hạn mức gấp bốn, năm lần. Và cả đội dùng chung giới hạn hai trăm lượt tìm kiếm mỗi phiên. Dùng đội cho những câu hỏi đáng giá, đừng dùng cho câu hỏi tra cứu đơn giản. |
| 4:00 | `TEXT: Chạy hằng tháng = claude -p "/nghien-cuu-sau ..." + Task Scheduler (tập 8)` | Mẹo cuối: kết hợp với tập tám, bạn có thể cho đội này chạy **mỗi tháng**, theo dõi thị trường đều đặn mà không phải nhớ. |
| 4:15 | Tóm tắt: `Mỗi agent một file` · `Giao việc trong cùng một lượt` · `Kiểm chứng viên độc lập` · `Báo cáo nói rõ điều chưa biết` | |
| 4:28 | `TEXT: BÀI TẬP: chạy /nghien-cuu-sau cho 1 câu hỏi chiến lược của phòng bạn` | Bài tập: lấy một câu hỏi chiến lược của phòng bạn, cho đội chạy, rồi so với báo cáo bạn từng làm tay. |
| 4:38 | Teaser: trình duyệt mở trang cần đăng nhập, cuộn vô hạn, nội dung hiện ra bằng JavaScript | Có một loại trang web mà WebFetch và script tập trước đều **mù**: trang dùng JavaScript, trang cần đăng nhập, trang cuộn vô hạn. Tập sau mình xử lý cả ba. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt và lệnh dùng trong tập

**PROMPT tạo đội** (nếu quay cảnh tạo, thay cho `--giai-phap`)
```text
Tạo đội nghiên cứu:
1. Agent .claude/agents/nha-nghien-cuu.md (sonnet; WebSearch, WebFetch, Read, Write, Bash, PowerShell): nghiên cứu MỘT góc,
   ghi nguon-<MÃ>.csv (ma,nhan_dinh,trich_dan,url; mã <MÃ>1, <MÃ>2...) và phan-<MÃ>.md (phát hiện, Điểm vênh, Câu hỏi bỏ ngỏ).
   Trích dẫn NGUYÊN VĂN, không sửa file của góc khác.
2. Agent .claude/agents/kiem-chung-vien.md (opus; Read, Edit, Bash, PowerShell, WebFetch, Glob): chạy kiem-chung-trich-dan.py trên mọi nguon-*.csv,
   sửa trích dẫn, gỡ số không có nguồn, lặp tới khi sạch.
3. Skill .claude/skills/nghien-cuu-sau/ (disable-model-invocation: true): chia 3–5 góc và chờ tôi đồng ý → gọi các nha-nghien-cuu
   SONG SONG trong cùng một lượt → kiem-chung-vien → tổng hợp bao-cao-chien-luoc.md có ma trận độ tin cậy, điểm vênh, câu hỏi bỏ ngỏ.
   Chép kiem-chung-trich-dan.py vào scripts/ của skill.
```

**Lệnh chạy**
```text
/nghien-cuu-sau @de-bai-chien-luoc.md
```

## Xử lý sự cố

| Tình huống | Cách xử lý |
|---|---|
| Các agent chạy lần lượt, không song song | Nhắc: "gọi tất cả nha-nghien-cuu trong cùng một lượt" |
| Hết 200 lượt tìm kiếm giữa chừng | `/clear` rồi chạy lại với ít góc hơn, hoặc đặt biến môi trường `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION=400` |
| Agent dừng chờ duyệt WebFetch | Dùng chế độ Auto, hoặc thêm `WebFetch(domain:...)` vào `permissions.allow` |
| Hai agent nghiên cứu trùng nội dung | Bước 1 chưa ghi rõ "không thuộc phạm vi". Sửa phạm vi rồi chạy lại |

## Gói đăng tải

- **Tiêu đề:** A: `Đội 5 AI nghiên cứu chiến lược trong 15 phút: Deep Research tự dựng | Claude nâng cao #12` · B: `Có nên bán trên TikTok Shop? Để 5 AI nghiên cứu và tự kiểm chứng`
- **Thumbnail:** 4 ô AI + 1 ô kính lúp, chữ **"ĐỘI 5 AI"**.
- **Shorts:** (1) 0:52–1:12 "Mỗi agent một file: lỗi kinh điển khi làm nhóm", (2) 3:05–3:38 "Báo cáo tốt nói rõ điều chưa biết".
