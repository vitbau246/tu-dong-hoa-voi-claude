# Tập 16: Viết bài chuẩn SEO, "giám khảo" tự chấm điểm, AI tự sửa đến khi đạt

| | |
|---|---|
| **Mục tiêu người xem** | Viết bài SEO bằng AI **đúng giọng thương hiệu, không bịa chính sách**, và dựng vòng lặp chất lượng tự động: viết → máy chấm điểm → AI tự sửa → đạt ngưỡng |
| **Tính năng dạy** | CLAUDE.md làm "bộ sự thật thương hiệu", trình chấm điểm on-page 17 tiêu chí, **hook PostToolUse thoát mã 2 → Claude nhận lỗi và tự sửa**, skill `/viet-bai-seo` |
| **Dữ liệu** | `python chuan-bi.py` tạo `demo/` với CLAUDE.md (giọng văn + sự thật + điều cấm), `san-pham.csv` (liên kết nội bộ), `brief/ghe-cong-thai-hoc.md`, `bai-viet/ban-nhap-cu.md`, `cham-diem-seo.py`. `--giai-phap` chép hook + skill |
| **Đã kiểm thử** | Bài nháp cũ: **14/100** · Bài mẫu: **100/100** (1.381 từ, mật độ 2,0%, 6 liên kết nội bộ), xem `giai-phap/ket-qua-mau/` · **Chạy thật với Claude** (`/viet-bai-seo`, khoảng 4 phút, khoảng $0,97): bài **100/100**, bảo hành đúng 24/12 tháng, tự bỏ câu "ngồi thử **miễn phí**" vì không có trong bộ sự thật · **Vòng phản hồi đã xác nhận**: Claude sửa tiêu đề bài cũ → hook trả "34/100 + 12 lỗi" → Claude đọc được nguyên văn, còn tự chỉ ra "chữa đau lưng", "bảo hành trọn đời", "rẻ nhất thị trường" vi phạm CLAUDE.md |

## Chuẩn bị

1. `pip install pyyaml`, sau đó `python chuan-bi.py`, mở `tap-16-viet-bai-chuan-seo/demo`.
2. Prompt tạo `cham-diem-seo.py` nằm ở mục **PROMPT phụ** (đưa vào mô tả). Khi quay, dùng bản có sẵn.
3. Bước 2 cần hook: tạo bằng PROMPT 2, hoặc dùng `--giai-phap`. Sau khi có `.claude/settings.json` thì **mở cuộc trò chuyện mới**.
4. Lần đầu Claude viết thường được khoảng 70–88 điểm (hay thiếu độ dài hoặc liên kết). Đó chính là cảnh "tự sửa" cần quay. Nếu Claude đạt 90 ngay lần đầu, quay cảnh `ban-nhap-cu.md` được sửa từ 14 lên ≥ 90.

## Kịch bản

| Thời gian | HÌNH | LỜI |
|---|---|---|
| 0:00 | Khung chat: Claude lưu bài → hộp đỏ từ hook `ĐIỂM SEO: 76/100 ✗ -8 Độ dài… ✗ -6 Liên kết nội bộ…` → Claude: "Tôi sẽ bổ sung mục… và 3 liên kết" → lưu lại → `ĐIỂM SEO: 96/100 - đạt ngưỡng` `SFX: ding` | AI viết xong, giám khảo chấm bảy mươi sáu điểm. Không ai nhắc, AI tự đọc lỗi, tự sửa. Chín mươi sáu. |
| 0:10 | Người dẫn | Viết bài bằng AI thì ai cũng làm được. Cái khó là bài đó phải chuẩn SEO, đúng giọng thương hiệu, và **không bịa**. Hôm nay mình dựng một quy trình mà chất lượng được đảm bảo bằng máy, không phụ thuộc vào việc bạn soát kỹ đến đâu. |
| 0:25 | Thanh 3 bước: `① Bộ sự thật thương hiệu ② Giám khảo tự động ③ Viết và tự sửa` | |
| **0:28** | **① BỘ SỰ THẬT** — Mở `CLAUDE.md`: zoom "SỰ THẬT DUY NHẤT được phép nêu: bảo hành 24 tháng…", "Không khẳng định công dụng y tế" | Lỗi đáng sợ nhất khi AI viết bài bán hàng không phải sai chính tả, mà là **bịa chính sách**: "bảo hành trọn đời", "trả góp không phần trăm". Khách đọc rồi đòi, công ty phải chịu. Vì vậy mình viết sẵn một "bộ sự thật": những gì được phép nói về công ty, và những gì cấm nói. |
| 0:50 | Zoom dòng "Không khẳng định công dụng y tế ('chữa đau lưng')" | Với ngành ghế công thái học, câu "chữa đau lưng" là vi phạm quy định quảng cáo. AI không tự biết điều này. Bạn phải dạy nó. |
| **1:00** | **② GIÁM KHẢO** — Mở `cham-diem-seo.py`, cuộn danh sách 17 tiêu chí (tiêu đề 30–60 ký tự, mô tả 140–160, 1 thẻ H1, từ khóa trong 100 từ đầu, ≥ 3 liên kết nội bộ, ảnh có alt, FAQ…) | Bước hai: giám khảo. Một script chấm mười bảy tiêu chí SEO on-page, giống các plugin như Yoast hay RankMath, thang một trăm điểm. Claude viết script này cho mình, prompt ở phần mô tả. |
| 1:15 | Terminal: `python cham-diem-seo.py bai-viet/ban-nhap-cu.md` → **14/100** với danh sách ✗ đỏ | Thử với một bài viết cũ của website: mười bốn điểm. Tiêu đề dài trăm ký tự, mô tả có tám ký tự, từ khóa bị nhồi tới hai mươi phần trăm, và câu "chữa đau lưng". |
| 1:32 | Dán PROMPT 2 → Claude tạo `.claude/settings.json` với hook PostToolUse. Zoom `"matcher": "Write\|Edit"` + `--hook` | Giờ biến giám khảo thành **hook**. Mỗi lần Claude ghi một file trong thư mục bài viết, script tự chấm. Dưới chín mươi điểm thì trả về mã hai, và tập sáu đã dạy: với PostToolUse, mã hai nghĩa là **lỗi được đưa thẳng cho Claude**. |
| 1:52 | Sơ đồ vòng lặp: `Claude viết → Hook chấm → <90: lỗi về Claude → Claude sửa → Hook chấm → ≥90 ✓` | Đây là vòng lặp tự sửa. Bạn không cần ngồi soát và nhắc. Máy nhắc máy. |
| **2:05** | **③ VIẾT VÀ TỰ SỬA** — Cuộc trò chuyện mới. Dán PROMPT 3 (tạo skill) → mở SKILL.md, zoom bước 4 "sửa đúng các mục đó (không độn chữ)" | Bước ba: đóng gói thành lệnh viết-bài-SEO. Câu quan trọng trong skill: sửa đúng lỗi, **không độn chữ**, không nhồi từ khóa. Nếu không có câu này, AI có thể "lách luật" bằng cách thêm chữ vô nghĩa cho đủ độ dài. |
| 2:22 | `/viet-bai-seo brief/ghe-cong-thai-hoc.md` → Claude đọc brief + CLAUDE.md + san-pham.csv → viết `[TUA x10]` → hook: ✗ … → sửa → ✓ 9x/100 (cảnh mở đầu) | Gọi lệnh với brief tập trước. Claude đọc brief, bộ sự thật, danh sách trang để đặt liên kết, rồi viết. Lưu lần một: giám khảo trả lỗi. Nó sửa. Lưu lần hai: đạt. |
| 2:50 | Mở bài viết: frontmatter (title 55 ký tự, meta 142, FAQ) → bảng so sánh → mục "Bảo hành: 24 tháng khung…, 12 tháng lưới" + link `/chinh-sach-bao-hanh` → FAQ "không phải dụng cụ chữa bệnh… hỏi ý kiến bác sĩ" | Xem kết quả. Tiêu đề năm mươi lăm ký tự. Bảng so sánh. Bảo hành đúng hai mươi tư tháng như bộ sự thật, kèm liên kết tới trang chính sách. Và câu hỏi "có hết đau lưng không" được trả lời thận trọng, khuyên gặp bác sĩ, **không** hứa chữa bệnh. |
| 3:15 | Cuối bài: `<!-- ANH CAN CHUP: … -->` | Ảnh thì AI không chụp thay được. Nó để chỗ trống và liệt kê ảnh thật cần chụp. Ảnh thật tại showroom là một tín hiệu tin cậy mà Google đánh giá cao. |
| **3:28** | **MẸO PRO 1** — `TEXT: 100 điểm on-page ≠ lên top` | Nói thật: một trăm điểm on-page **không** đảm bảo lên top Google. Nó chỉ là điều kiện cần, như đề bài trình bày đúng mẫu. Nội dung có thật sự hữu ích hơn đối thủ hay không, có kinh nghiệm thực tế hay không, mới là thứ quyết định. Đó là lý do tập trước mình đi tìm **khoảng trống** của đối thủ. |
| 3:50 | **MẸO PRO 2** — `TEXT: Giám khảo dùng được cho mọi tiêu chuẩn: văn bản hành chính, email, hợp đồng…` | Công thức "viết, máy chấm, tự sửa" dùng được cho mọi thứ có tiêu chuẩn rõ ràng: văn bản hành chính đúng thể thức, email đúng mẫu, báo cáo đủ mục. Chỉ cần viết được tiêu chí thành script. |
| 4:08 | Tóm tắt: `CLAUDE.md = bộ sự thật + điều cấm` · `Script chấm điểm = giám khảo` · `Hook mã 2 = AI tự sửa` | |
| 4:20 | `TEXT: BÀI TẬP: chạy cham-diem-seo.py cho 3 bài cũ trên website của bạn` | Bài tập: lấy ba bài cũ trên website của bạn, chuyển sang Markdown và cho giám khảo chấm. Bài điểm thấp nhất là bài cần sửa đầu tiên. |
| 4:32 | Teaser: WordPress admin, bài nháp xuất hiện kèm ảnh bìa, chuyên mục, thẻ, mô tả SEO | Bài đã đạt. Tập sau, một lệnh đưa nó lên WordPress: ảnh bìa, chuyên mục, thẻ, mô tả SEO, schema FAQ. Kèm bài đăng Facebook, LinkedIn và email bản tin. |
| 4:50 | Màn hình kết | Việc lặp lại, để máy làm. Việc cần suy nghĩ, để bạn làm. |

## Prompt dùng trong tập

**PROMPT 2** (hook)
```text
Tạo .claude/settings.json với hook PostToolUse (matcher Write|Edit) chạy: "command": "python",
"args": ["${CLAUDE_PROJECT_DIR}/cham-diem-seo.py", "--hook"]. Giải thích ngắn hook sẽ làm gì.
```

**PROMPT 3** (skill)
```text
Tạo skill .claude/skills/viet-bai-seo: nhận file brief; đọc CLAUDE.md (giọng văn, sự thật, điều cấm) và san-pham.csv;
viết bài vào bai-viet/<slug>.md đúng định dạng frontmatter của cham-diem-seo.py; ưu tiên các mục ★ trong brief;
có bảng so sánh, ≥ 2 ảnh giữ chỗ có alt, 3–5 liên kết nội bộ, FAQ trong frontmatter;
khi hook báo lỗi thì sửa đúng mục đó, KHÔNG độn chữ, KHÔNG nhồi từ khóa; lặp tới ≥ 90; rà soát lần cuối với CLAUDE.md.
```

**PROMPT 4** `/viet-bai-seo brief/ghe-cong-thai-hoc.md`

**PROMPT phụ** (cho mô tả video)
```text
Viết cham-diem-seo.py chấm bài Markdown có YAML frontmatter (title, meta_description, slug, focus_keyword, min_words, faq) thang 100:
title 30–60 ký tự (10), từ khóa trong title (10), meta 140–160 (8), từ khóa trong meta (5), slug không dấu chứa từ khóa (5),
đúng 1 H1 (5), từ khóa trong H1 (5), từ khóa trong 100 từ đầu (8), cấp tiêu đề không nhảy cóc (5), ≥ 4 H2 (4), số từ ≥ min_words (8),
mật độ từ khóa 0,5–2,5% (5), ≥ 3 liên kết nội bộ (6), mọi ảnh có alt (5), ≥ 3 FAQ (5), câu TB ≤ 25 từ (3), đoạn ≤ 120 từ (3).
Chế độ --hook: đọc JSON stdin, chỉ chấm file bai-viet/*.md, dưới 90 thì in lỗi + gợi ý sửa ra stderr và thoát mã 2.
```

## Xử lý sự cố (rút ra từ lần chạy thật)

| Tình huống | Nguyên nhân và cách xử lý |
|---|---|
| Claude nói "hook không phản hồi gì" khi bài đã đạt | Với PostToolUse, stdout khi thoát mã 0 **không** tới được Claude. Script đã trả JSON `hookSpecificOutput.additionalContext`. Nếu tự viết hook, nhớ làm như vậy |
| Claude bị chặn khi chạy `python cham-diem-seo.py` | Trên Windows, Claude chạy lệnh qua công cụ **PowerShell**, nên `Bash(python *)` không áp dụng. Skill đã có cả `PowerShell(python *)` |
| `claude -p "/viet-bai-seo ..."` từ Git Bash báo không thấy skill | Git Bash đổi `/viet-bai-seo` thành đường dẫn. Chạy từ PowerShell, hoặc đặt `MSYS_NO_PATHCONV=1` |
| Muốn xem lịch sử điểm (cảnh 76 → 96) | Mở `.claude/nhat-ky-cham-diem.csv`, hook ghi lại mỗi lần chấm |

## Gói đăng tải

- **Tiêu đề:** A: `AI viết bài chuẩn SEO, máy tự chấm điểm, tự sửa tới 96/100 | Claude nâng cao #16` · B: `Viết bài SEO bằng AI mà không sợ bịa chính sách (vòng lặp tự sửa)`
- **Thumbnail:** Đồng hồ điểm 76 → 96 màu xanh. Chữ: **"TỰ SỬA ĐẾN KHI ĐẠT"**.
- **Shorts:** (1) 0:00–0:10 "AI tự sửa bài khi bị chấm trượt", (2) 0:28–1:00 "Đừng để AI bịa chính sách bảo hành".
