---
name: nghien-cuu
description: Nghiên cứu một câu hỏi trên Internet và viết báo cáo ngắn mà MỌI con số đều có nguồn và trích dẫn nguyên văn, sau đó tự kiểm chứng từng trích dẫn bằng cách mở lại nguồn gốc. Dùng khi người dùng cần tìm hiểu thị trường, số liệu, đối thủ, quy định, hoặc bất kỳ báo cáo nào cần dẫn nguồn.
argument-hint: "<câu hỏi nghiên cứu hoặc đường dẫn file đề bài>"
allowed-tools: WebSearch WebFetch Read Write Bash(python *) PowerShell(python *)
---

# Nghiên cứu có trích nguồn

Đề bài: **$ARGUMENTS**

## 1. Lập kế hoạch (trình bày ngắn trước khi tìm)
- Tách câu hỏi thành 3–5 câu hỏi con.
- Với mỗi câu hỏi con: loại nguồn ưu tiên (cơ quan nhà nước, tổ chức nghiên cứu, báo cáo doanh nghiệp, rồi mới tới báo chí) và 2–3 truy vấn tìm kiếm, cả tiếng Việt và tiếng Anh.

## 2. Tìm và đọc
- Dùng WebSearch để tìm, WebFetch để đọc. **Lưu ý:** WebFetch trả về bản tóm tắt, nên khi lấy câu trích, yêu cầu WebFetch "trích NGUYÊN VĂN câu chứa con số", không diễn đạt lại.
- Ghi lại ngày công bố của nguồn. Số liệu cũ hơn 2 năm phải ghi chú "(số liệu năm ...)".
- Các nguồn đưa ra số khác nhau: ghi **tất cả**, không tự chọn.

## 3. Viết kết quả vào thư mục `nghien-cuu/<slug-chu-de>/`
- `nguon.csv` (UTF-8) với các cột chính xác: `ma,nhan_dinh,trich_dan,url`. Mỗi con số trong báo cáo là một dòng, `trich_dan` là câu **nguyên văn** từ nguồn.
- `bao-cao.md`: tối đa 1 trang A4. Mỗi con số gắn mã nguồn `[N1]`. Tách rõ hai phần **Số liệu** và **Nhận định** (nhận định là của người viết, không cần nguồn nhưng phải dựa trên số liệu đã nêu). Có mục "Điểm vênh giữa các nguồn" nếu có.

## 4. Kiểm chứng (bắt buộc, không được bỏ qua)
```
python "${CLAUDE_SKILL_DIR}/scripts/kiem-chung-trich-dan.py" nghien-cuu/<slug>/nguon.csv
```
- `KHÔNG THẤY`: mở lại nguồn, lấy đúng câu nguyên văn. Nếu nguồn không có con số đó thì **xóa con số khỏi báo cáo**.
- `GẦN ĐÚNG`: sửa trích dẫn cho khớp nguyên văn.
- `KHÔNG TẢI ĐƯỢC` (trang chặn bot hoặc cần JavaScript): giữ lại nhưng đánh dấu "(chưa kiểm chứng tự động)" trong báo cáo.
- Chạy lại cho tới khi không còn `KHÔNG THẤY`.

## 5. Bàn giao
Trả lời 4 dòng: đường dẫn báo cáo · số nguồn / số trích dẫn · kết quả kiểm chứng (KHỚP / chưa kiểm chứng) · 1 câu trả lời ngắn nhất cho câu hỏi gốc.
