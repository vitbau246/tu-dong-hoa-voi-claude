# Thiết lập quay phim

## 1. Phần mềm

| Mục đích | Công cụ |
|---|---|
| Quay màn hình | OBS Studio: canvas 1920×1080, 30 fps, định dạng MKV (tự remux sang MP4) |
| Thu âm | Micro USB/XLR, khử ồn bằng filter *Noise Suppression (RNNoise)* trong OBS |
| Dựng | DaVinci Resolve / CapCut. Dùng *speed ramp* (tua x4–x10) cho các đoạn Claude đang chạy |
| Phóng to con trỏ, hiện phím | ZoomIt (Sysinternals) + Carnac (hiện phím tắt trên màn hình) |
| Dọn thông báo | Bật Focus Assist **trừ** tập 6 và tập 8 (cần quay thông báo Windows) |

## 2. Cấu hình VS Code cho quay phim

Tạo profile riêng để không ảnh hưởng máy làm việc: **File → New Window with Profile → "quay-phim"**. Sau đó dán `vscode-settings-quay-phim.json` vào *Preferences: Open User Settings (JSON)* của profile này.

Nguyên tắc:
- Chữ to (editor 18, terminal 16, giao diện zoom +1). Người xem trên điện thoại vẫn phải đọc được.
- Theme tương phản cao, cố định cả series (đề xuất: *Default Light Modern* cho video sáng sủa, hoặc *Default Dark Modern*).
- Ẩn minimap, breadcrumbs. Bật word wrap để không phải cuộn ngang.
- Bố cục: cây thư mục trái hẹp · editor giữa · **khung Claude bên phải rộng khoảng 40%**.

## 3. Quy trình mỗi tập

1. `cd tap-xx-... && python chuan-bi.py`, rồi mở `demo/` trong VS Code (profile "quay-phim").
2. Đọc phần **Chuẩn bị** trong `kich-ban.md` của tập.
3. Mở sẵn các prompt (copy từ `kich-ban.md`) trong một file nháp **ngoài khung hình** để dán.
4. **Quay demo trước, thu lời sau.** Chạy demo thật 2–3 lần, chọn lần tốt nhất. Thu lời thoại riêng theo kịch bản, rồi khớp hình theo lời.
5. Đối chiếu kết quả của Claude với `dap-an.json` **trước khi** thu lời. Nếu lần chạy tốt nhất ra con số khác đáp án, điều tra cho rõ, đừng đọc số sai.
6. Ghi lại **thời gian thật** của mỗi đoạn Claude chạy để điền vào các chữ trên màn hình `[thời gian thật]`.
7. Quay xong: chạy lại `python chuan-bi.py` nếu cần quay bổ sung.

## 4. Checklist an toàn trước khi đăng

- [ ] Không lộ email, tên tổ chức, đường dẫn thư mục cá nhân thật (đổi tên người dùng Windows hoặc làm mờ).
- [ ] Không lộ thông tin tài khoản Claude (email đăng nhập, gói) trong khung hình.
- [ ] Tất cả dữ liệu trong video là dữ liệu hư cấu từ `chuan-bi.py`.
- [ ] Tập 8: đã gỡ tác vụ hẹn giờ thử nghiệm. Tập 10: đã gỡ marketplace thử nghiệm.
- [ ] Mô tả có ghi phiên bản Claude Code dùng khi quay.
