# Tập 5: Báo cáo tuần chỉ bằng MỘT lệnh (CLAUDE.md + Skills)

| | |
|---|---|
| **Mục tiêu người xem** | Dạy Claude **nhớ bối cảnh** (CLAUDE.md) và **đóng gói quy trình** thành lệnh `/ten-lenh` (Skill) |
| **Tính năng dạy** | `CLAUDE.md`, Skills (`.claude/skills/<ten>/SKILL.md`), tham số `$ARGUMENTS`, script đi kèm skill, `description` để Claude tự gọi skill |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/` với nhật ký 10 ngày (tuần 43, 44), `cong-viec.xlsx`, mẫu báo cáo. `python chuan-bi.py --giai-phap` chép thêm CLAUDE.md + skill hoàn chỉnh |
| **Kết quả tham chiếu** | `giai-phap/ket-qua-mau/bao-cao-tuan-44-2026.md` / `.docx`: báo cáo tốt trông như thế nào |

## Chuẩn bị

1. `python chuan-bi.py` (trạng thái ban đầu), sau đó mở `tap-05-skills-bao-cao-tuan/demo` trong VS Code.
2. Mở sẵn một file nhật ký, ví dụ `nhat-ky/2026-10-29.md`, để quay cảnh "nhật ký viết vội".
3. ⚠️ Thư mục `.claude/skills/` chưa tồn tại lúc mở phiên, nên sau khi Claude tạo skill, hãy **mở cuộc trò chuyện mới** (hoặc gõ `/reload-skills`) để skill hiện ra.
4. Nếu skill Claude tự viết chưa tốt khi quay, dùng bản trong `giai-phap/` (`python chuan-bi.py --giai-phap`) để quay cảnh bước 3.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Ô chat trống. Gõ `/bao-cao-tuan 44` → Enter `[TUA x4]` → file Word báo cáo tuần mở ra: bảng biểu, con số in đậm | Đây là toàn bộ công sức làm báo cáo tuần của mình: gõ một lệnh. |
| 0:06 | `TEXT: 45 phút → 1 lệnh` | Trước đây việc này mất bốn mươi lăm phút mỗi chiều thứ Sáu. |
| 0:10 | Người dẫn | Bốn tập trước, lần nào mình cũng phải dán một prompt dài. Hôm nay mình sẽ dạy Claude hai thứ: **nhớ** mình là ai, và **thuộc lòng** một quy trình. Sau video này, bạn sẽ tạo được lệnh riêng cho bất kỳ việc lặp lại nào. |
| 0:25 | Thanh 3 bước: `① Làm thủ công ② Dạy Claude nhớ ③ Đóng gói thành lệnh` | |
| **0:28** | **① LÀM THỦ CÔNG** — Mở nhật ký `2026-10-29.md`: "a Hùng", "P.KT", "KH 2027", "HĐ"... | Đây là nhật ký của mình: viết vội, viết tắt lung tung, chỉ mình hiểu. |
| 0:38 | Dán PROMPT 1 (dài) → kết quả `[TUA x6]` | Lần đầu, mình dùng một prompt dài: đọc nhật ký tuần bốn mươi tư, đọc bảng công việc, viết báo cáo theo mẫu. |
| 0:55 | Highlight trong báo cáo: "**a Hùng** góp ý...", "**P.KT** chưa gửi...", "**QLVB**". `TEXT: Gửi sếp thế này?` | Kết quả khá ổn, nhưng nhìn này: "a Hùng", "P.KT", "QLVB". Báo cáo gửi lên trên mà viết thế này thì không được. Claude không có lỗi: nó **không biết** a Hùng là ai. |
| **1:10** | **② DẠY CLAUDE NHỚ** — Dán PROMPT 2 | Bước hai: cho Claude một "trí nhớ". Mình nói cho nó biết mình là ai, sếp là ai, bảng chữ viết tắt, và quy ước trình bày, rồi bảo nó ghi tất cả vào file **CLAUDE.md**. |
| 1:25 | Mở `CLAUDE.md` vừa tạo: cuộn qua bảng viết tắt, quy ước số tiền, mục "An toàn" | CLAUDE.md là một file văn bản bình thường. Đặc biệt ở chỗ: **mỗi lần** bạn mở Claude trong thư mục này, nó tự đọc file này trước tiên. Bạn nói một lần, nó nhớ mãi. |
| 1:40 | `TEXT: CLAUDE.md = sổ tay bàn giao cho trợ lý mới` | Hãy hình dung nó như cuốn sổ bàn giao bạn đưa cho một trợ lý mới vào làm. |
| 1:48 | Mở **cuộc trò chuyện mới**, dán lại đúng PROMPT 1 → kết quả. Split screen trước/sau: "a Hùng" → "anh Nguyễn Văn Hùng – Trưởng phòng KH-TH", "47,28tr" → "47.280.000 đồng" | Mở phiên mới, dán đúng prompt cũ. Và giờ: anh Nguyễn Văn Hùng, Trưởng phòng. Phòng Kỹ thuật. Bốn mươi bảy triệu hai trăm tám mươi nghìn đồng. Cùng một yêu cầu, nhưng giờ Claude hiểu bối cảnh của bạn. |
| **2:15** | **③ ĐÓNG GÓI THÀNH LỆNH** — Dán PROMPT 3 | Nhưng mình vẫn phải dán cái prompt dài kia. Bước ba: bảo Claude **biến chính quy trình vừa làm thành một kỹ năng**, tức một Skill. |
| 2:28 | Claude tạo `.claude/skills/bao-cao-tuan/SKILL.md` + `scripts/md_sang_docx.py`. Mở SKILL.md, zoom: `name`, `description`, `argument-hint`, các bước, `$ARGUMENTS` | Đây là skill nó viết. Phần đầu có tên lệnh và mô tả. Phần thân là quy trình từng bước, giống hệt cách bạn hướng dẫn một đồng nghiệp. Chỗ `$ARGUMENTS` là nơi nhận số tuần bạn gõ vào. Claude còn tự viết kèm một script nhỏ để chuyển báo cáo sang Word. |
| 2:50 | Mở cuộc trò chuyện mới, gõ `/` → menu hiện `bao-cao-tuan` → gõ `/bao-cao-tuan 44` `[TUA x6]` | Phiên mới. Gõ dấu gạch chéo, lệnh của mình đã nằm trong danh sách. Bao-cáo-tuần, bốn mươi tư. Enter. |
| 3:10 | File `bao-cao/bao-cao-tuan-44-2026.docx` mở trong Word: kết quả nổi bật có số, hạn sắp tới in đậm, mỗi vướng mắc kèm đề xuất | Báo cáo Word. Kết quả nổi bật có con số. Hạn sắp đến được in đậm. Mỗi vướng mắc đi kèm một đề xuất. Không bịa số nào. |
| 3:25 | Gõ `/bao-cao-tuan 43` → báo cáo tuần 43 hiện ra | Tuần trước thì sao? Bốn mươi ba. Xong. |
| **3:35** | **MẸO PRO 1** — Gõ câu thường: "làm báo cáo tuần này giúp mình" → Claude tự dùng skill | Mẹo thứ nhất: bạn thậm chí không cần nhớ tên lệnh. Nói bình thường "làm báo cáo tuần giúp mình", Claude đọc phần **mô tả** của skill và tự biết phải dùng nó. Đó là lý do phần mô tả phải viết rõ: skill làm gì, dùng khi nào. |
| 3:55 | **MẸO PRO 2** — Sơ đồ 2 vị trí: `.claude/skills/` (chỉ thư mục này, chia sẻ qua git) · `~/.claude/skills/` (mọi thư mục trên máy bạn) | Mẹo thứ hai: skill đặt trong thư mục dự án thì chỉ dùng ở dự án đó, và cả nhóm dùng chung được. Đặt trong thư mục người dùng thì dùng ở mọi nơi trên máy bạn. |
| 4:10 | Tóm tắt: `CLAUDE.md = Claude NHỚ bạn là ai` · `Skill = Claude THUỘC quy trình` · `Làm 1 lần bằng tay → đóng gói → dùng mãi` | Tóm lại: CLAUDE.md để Claude nhớ bạn là ai. Skill để Claude thuộc quy trình. Công thức chung: làm một lần bằng tay cho tốt, rồi bảo Claude đóng gói lại. |
| 4:25 | `TEXT: BÀI TẬP: chọn 1 việc bạn làm MỖI TUẦN → làm 1 lần với Claude → "biến thành skill"` | Bài tập: chọn một việc bạn làm mỗi tuần, làm với Claude một lần, rồi nói đúng câu "biến quy trình này thành skill". |
| 4:38 | Teaser: Claude định chạy `Remove-Item du-lieu-goc` → hộp đỏ "BLOCKED" | Càng giao nhiều việc cho AI, câu hỏi càng lớn: lỡ nó xóa nhầm thì sao? Tập sau mình gắn "phanh an toàn" để AI **không thể** xóa dữ liệu gốc, dù có muốn. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 1** (làm thủ công)
```text
Đọc nhật ký tuần 44 (26/10 - 30/10/2026) trong @nhat-ky/ và bảng @cong-viec.xlsx,
viết báo cáo tuần theo đúng mẫu @mau/mau-bao-cao-tuan.md, lưu vào bao-cao/.
```

**PROMPT 2** (tạo CLAUDE.md)
```text
Tạo file CLAUDE.md để ghi nhớ bối cảnh làm việc của tôi:
- Tôi là Phạm Minh Đức, chuyên viên Phòng Kế hoạch – Tổng hợp (P.KH-TH). Sếp trực tiếp: anh Nguyễn Văn Hùng, Trưởng phòng.
- Chữ viết tắt hay dùng: a Hùng, c Lan (chị Trần Thị Lan – P.HCNS), BGĐ, P.KD, P.KT, P.TC, P.HCNS,
  NCC, HĐ, QLVB (phần mềm Quản lý văn bản), KH, bc, tk, SLA, tr (triệu đồng).
  Văn bản gửi đi luôn phải viết đầy đủ.
- Số tiền dạng 47.280.000 đồng, ngày dd/mm/yyyy, văn phong hành chính, không emoji.
- Mỗi vướng mắc phải kèm đề xuất. Không bịa số liệu, thiếu thì ghi "(cần bổ sung)".
- Không bao giờ xóa/ghi đè nhat-ky/ và cong-viec.xlsx. Báo cáo lưu vào bao-cao/.
Mô tả thêm cấu trúc thư mục hiện tại.
```

**PROMPT 3** (tạo skill)
```text
Biến quy trình làm báo cáo tuần vừa rồi thành một skill tên "bao-cao-tuan" trong .claude/skills/:
- Nhận tham số là số tuần ISO; bỏ trống thì lấy tuần hiện tại.
- Các bước rõ ràng: xác định ngày, đọc nhật ký + bảng công việc, viết theo mẫu, lưu .md
  rồi chuyển sang Word bằng một script Python đặt trong thư mục scripts/ của skill.
- Bước cuối: tự kiểm tra không bịa số, không còn chữ viết tắt.
- Viết phần description để tôi chỉ cần nói "làm báo cáo tuần" là bạn biết dùng skill này.
```

**PROMPT 4**
```text
/bao-cao-tuan 44
```

## Đối chiếu nhanh (tuần 44)

Báo cáo tốt phải có: HĐ bảo trì **186.000.000 đồng/năm** đã ký · tờ trình màn hình **47.280.000 đồng** (rẻ hơn 4,2%) · đào tạo QLVB **11 người** P.KD · KH 2027: **5/7 phòng**, dự kiến **1,2 tỷ**, hạn **13/11/2026** · vướng mắc P.KT, P.KD chậm gửi nhu cầu → đề xuất anh Hùng nhắc tại giao ban. Xem bản đầy đủ trong `giai-phap/ket-qua-mau/`.

## Gói đăng tải

- **Tiêu đề:**
  - A: `Báo cáo tuần chỉ bằng 1 lệnh: tạo Skill cho Claude trong 5 phút | Tự động hóa với Claude #5`
  - B: `Dạy AI nhớ sếp bạn là ai (CLAUDE.md + Skills cho người không biết code)`
- **Thumbnail:** Ô lệnh lớn `/bao-cao-tuan` → file Word. Chữ: **"45 PHÚT → 1 LỆNH"**.
- **Shorts:** (1) 0:55–1:10 + 1:48–2:15 "AI không biết a Hùng là ai", (2) 3:35–3:55 "Không cần nhớ tên lệnh".
- **Bình luận ghim:** link tải `SKILL.md` mẫu + "Bạn sẽ tạo lệnh gì đầu tiên?"
