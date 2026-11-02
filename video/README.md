# Dựng video "5 phút tự động hóa"

Video dạng **minh họa động + lồng tiếng tiếng Việt + phụ đề**, dữ liệu lấy từ **phiên Claude Code chạy thật** trên dữ liệu demo của từng tập. Cảnh nào dùng dữ liệu thật có huy hiệu xanh "Dữ liệu từ phiên chạy thật", cảnh còn lại ghi "Minh họa".

```powershell
python dung-video.py canh/tap-01.json              # bản chính 1920×1080 + các Reels 1080×1920 → xuat/
python dung-video.py canh/tap-01.json --chi reel-2 # dựng lại 1 bản
```

| Thành phần | Vai trò |
|---|---|
| `canh/<ten>.json` | Kịch bản cảnh: loại cảnh, nội dung, lời đọc (`loi`), bước, cờ `that` (dữ liệu thật), danh sách Reels |
| `khuon/canh.html` | Khuôn cảnh (tự co giãn 16:9 / 9:16), font Be Vietnam Pro + JetBrains Mono (OFL, giấy phép trong `fonts/`) |
| `dung-video.py` | edge-tts (giọng `vi-VN-NamMinhNeural`, có cache + thử lại) → Playwright chụp cảnh → ffmpeg: zoom chậm, phụ đề, chuẩn hóa −14 LUFS |
| `du-lieu-that/tap-XX/` | JSON kết quả các lần chạy Claude thật (kế hoạch, thực hiện, thời gian, chi phí) |
| `xuat/` | Video thành phẩm (H.264 + AAC 48 kHz, faststart) |

## Quy trình mỗi tập
1. `python ..\tap-XX-...\chuan-bi.py` → chạy Claude thật trên `demo/` theo prompt trong `kich-ban.md` (lưu JSON vào `du-lieu-that/`).
2. **Tự kiểm chứng** kết quả (đếm, hash, đối chiếu `dap-an.json`). Không đưa vào video con số chưa kiểm chứng.
3. Viết `canh/tap-XX.json` theo **kết quả thật** (sửa lời thoại nếu thực tế khác kịch bản, ví dụ thời gian chạy).
4. `python dung-video.py canh/tap-XX.json` → xem lại → chép sang `facebook/media/tap-XX/`.

## Giới hạn
- Không phải quay màn hình VS Code: đây là video minh họa dựng từ dữ liệu thật. Muốn có cảnh giao diện thật, quay bổ sung bằng OBS theo `00-chien-luoc/04-thiet-lap-quay.md` rồi chèn vào.
- Lời đọc gửi tới dịch vụ đọc của Microsoft (edge-tts). Chỉ dùng cho nội dung công khai.
