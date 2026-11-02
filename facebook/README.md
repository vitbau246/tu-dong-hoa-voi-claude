# Đăng bài Fanpage "5 phút tự động hóa" (FoxFlow)

Hệ thống lên lịch đăng **82 bài** cho series 20 tập lên Fanpage qua Graph API v26.0: trailer, bài mồi, video tập chính, 2 Reels mỗi tập, và bình luận "prompt + file mẫu". Mọi bài đều **hẹn giờ** (không đăng ngay), chỉ bài **đã duyệt** mới được đẩy lên, và bạn vẫn xem/sửa/xóa được trong Meta Business Suite trước giờ lên sóng.

## Lịch tuần (giả thuyết + thử A/B 4 tuần đầu, xem `nghien-cuu-gio-dang.md`)

| Thứ | Giờ | Bài |
|---|---|---|
| Thứ 2 | 07:45 | Bài mồi: ảnh 4:5 + câu hỏi về nỗi đau của tập |
| Thứ 3 | **11:45** (tuần lẻ) / **20:00** (tuần chẵn) | Video tập chính (5 phút) + bình luận prompt/file mẫu |
| Thứ 5 | 12:15 | Reel 1 |
| Thứ 6 20:30 (tuần lẻ) / Thứ 7 09:00 (tuần chẵn) | | Reel 2 |
| Thứ 6 trước tập 1 và tập 11 | 20:00 | Trailer phần 1 / phần 2 |

Bắt đầu **16/11/2026** (trailer 13/11), kết thúc 17/04/2027, **nghỉ Tết 03–12/02/2027** (lùi 2 tuần). Đổi ngày bắt đầu, giờ, hashtag, link file mẫu trong `cau-hinh.json` rồi chạy `python lap-lich.py`.

## Quy trình mỗi tuần

```powershell
# 1. Đặt file media đúng tên:
#    media/trailer-phan-1.mp4 · media/tap-01/video.mp4 · media/tap-01/reel-1.mp4 · media/tap-01/reel-2.mp4
#    (bai-moi.jpg đã được tạo sẵn). Reels: MP4 9:16, 1080×1920, 3–90 giây.
# 2. Đọc nội dung trong bai-dang/tap-01-*.txt (sửa trực tiếp nếu muốn), rồi DUYỆT:
python dang-facebook.py --duyet tap-01
# 3. Xem trước (không gửi gì):
python dang-facebook.py
# 4. Đẩy lên Facebook (hẹn giờ):
python dang-facebook.py --len-lich
# 5. Sau khi video lên sóng: tự đăng bình luận prompt + file mẫu → VÀO GHIM TAY bình luận đó
python dang-facebook.py --binh-luan
```
Tự động bước 4–5 mỗi 30 phút: `powershell -ExecutionPolicy Bypass -File .\chay-hang-ngay.ps1 -DangKy`. Bước 1–2 (media + duyệt) vẫn do **người** làm.

## Thiết lập lần đầu
1. `pip install requests pillow`
2. Lấy Page token → `.env` theo `huong-dan-token.md` → `python dang-facebook.py --kiem-tra` phải ra **✅ ĐÚNG trang**.
3. Sửa `link_file_mau` trong `cau-hinh.json` (hiện là `https://github.com/vitbau246/tu-dong-hoa-voi-claude`) → `python lap-lich.py`.
4. **Thử với 1 bài trước:** duyệt riêng `trailer-phan-1`, `--len-lich`, rồi vào Meta Business Suite → Lịch để xem bài hẹn giờ hiển thị đúng chưa (chữ, ảnh, giờ).

## Sau 4 tuần: chốt khung giờ
`python phan-tich-khung-gio.py` (lần đầu tạo `theo-doi-hieu-qua.csv` để bạn điền số liệu từ Business Suite) → khung thắng ≥ 20% thì điền vào `cau-hinh.json` (`gio_sau_thu_nghiem`, `sau_thu_nghiem`) → `python lap-lich.py`. Bài đã lên lịch giữ nguyên giờ.

## Tập dượt không cần trang thật
`python gia-lap-graph.py` (Graph API giả lập: kiểm tra đúng luật hẹn giờ của Meta), rồi trong `.env` đặt:
`GRAPH_URL=http://localhost:8090`, `RUPLOAD_URL=http://localhost:8090`, `FB_PAGE_ID=1234567890`, `FB_PAGE_TOKEN=token-gia-lap`.

## File
| File | Vai trò |
|---|---|
| `nghien-cuu-gio-dang.md` | Nghiên cứu khung giờ, nguồn, kế hoạch thử A/B |
| `cau-hinh.json` · `noi-dung-tap.json` | Cấu hình lịch/thương hiệu · nội dung 20 tập |
| `lap-lich.py` | Sinh `lich-dang.csv`, `bai-dang/*.txt`, `media/tap-XX/bai-moi.jpg` |
| `dang-facebook.py` | Duyệt, chạy thử, lên lịch, bình luận |
| `chay-hang-ngay.ps1` | Task Scheduler mỗi 30 phút |
| `phan-tich-khung-gio.py` | Chốt khung giờ sau thử nghiệm |
| `gia-lap-graph.py` | Graph API giả lập để tập dượt |
| `huong-dan-token.md` | Lấy Page token an toàn |

## Giới hạn cần biết
- Facebook chỉ nhận hẹn giờ trong **30 ngày** (Reels 29), nên script đẩy cuốn chiếu **28 ngày**, chạy hằng ngày.
- **Ghim bình luận** không làm được qua API: phải ghim tay (script nhắc trong nhật ký).
- Tối đa **30 bài đăng qua API / 24 giờ** (giới hạn của Meta). Lịch này tối đa 7 bài/tuần, không chạm ngưỡng.
- Graph API chỉ đăng lên **Trang** (Page), không đăng lên trang cá nhân. "5 phút tự động hóa" phải là một Fanpage do profile FoxFlow quản trị.
