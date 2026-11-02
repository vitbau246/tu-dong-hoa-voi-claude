# Nghiên cứu khung giờ đăng: Fanpage "5 phút tự động hóa" (FoxFlow)

> Cập nhật 02/11/2026. Múi giờ: **Việt Nam (UTC+7)**.

## 1. Dữ liệu hiện có nói gì

| Nguồn | Phạm vi dữ liệu | Kết luận về Facebook | Độ tin cậy |
|---|---|---|---|
| Buffer 2026 (theo bài tổng hợp) | khoảng 14 triệu bài, toàn cầu | **Sáng ngày thường** tốt hơn chiều. Đỉnh: **Thứ 5, 9:00**. Thứ 4 > Thứ 5 > Thứ 3. **Thứ 7 kém nhất** | Trung bình: dữ liệu khách hàng của Buffer, mình đọc qua bài tổng hợp, chưa đọc báo cáo gốc |
| Sprout Social 2026 (theo bài tổng hợp) | khoảng 2 tỉ lượt tương tác | **Thứ 3, Thứ 4, 12:00–20:00**. **Chủ nhật kém nhất** | Trung bình |
| RecurPost (01/2026) | khoảng 2 triệu bài | **13:00–15:00**, tốt nhất Thứ 4 và Chủ nhật 14:00 | Thấp–trung bình |
| Hootsuite 2025 | 118 quốc gia | Hoạt động đỉnh **5:00–8:00** sáng | Ngoại lệ so với các nguồn khác |
| Blog Việt Nam (24hStore, MISA eShop, Sapo, Brands Vietnam…) | Không công bố dữ liệu gốc | 7–8h sáng · 11–13h trưa · 19–22h tối. Với nhóm B2B/văn phòng: 10:00–11:30 và 14:00–15:30 | Thấp: kinh nghiệm, không có số liệu |
| DataReportal Digital 2026 Vietnam / NapoleonCat | Quy mô người dùng | 79 triệu danh tính mạng xã hội (10/2025). Khoảng 86–89 triệu người dùng Facebook (số liệu quảng cáo Meta, ước tính) | Cao (quy mô), không nói về giờ |

**Kết luận trung thực:** không có nghiên cứu công khai đáng tin nào về giờ đăng **riêng cho Việt Nam**, và các nghiên cứu toàn cầu **mâu thuẫn nhau** (sáng sớm, sáng muộn hay trưa–tối). Những gì nhất quán:
1. **Ngày thường tốt hơn cuối tuần** (Thứ 7, Chủ nhật bị xếp kém nhất ở 2/3 nghiên cứu lớn).
2. **Giữa tuần (Thứ 3–Thứ 5)** là nhóm ngày tốt nhất.
3. Thuật toán dựa vào **tương tác sớm** (30–60 phút đầu), nên đăng **trước** đỉnh lướt mạng một chút.
4. **Dữ liệu của chính trang** (Meta Business Suite → Thông tin chi tiết) quan trọng hơn mọi trung bình. Nhưng trang mới chưa có dữ liệu, nên phải **thử nghiệm**.

## 2. Suy luận theo khán giả của trang

Khán giả mục tiêu: **dân văn phòng, chuyên viên, marketer** (xem `00-chien-luoc/01-nghien-cuu.md`).

| Khung giờ | Hành vi | Hợp với loại bài |
|---|---|---|
| 07:30–08:30 (đi làm, cà phê) | Lướt nhanh, hay tắt tiếng | Bài ảnh + câu hỏi (đọc 5 giây), Reels có phụ đề |
| 11:45–13:00 (nghỉ trưa) | Có thời gian, thường đeo tai nghe | **Video 5 phút**, Reels |
| 20:00–22:00 (ở nhà) | Xem lâu, có tiếng, chủ động học | **Video 5 phút**, bài hướng dẫn |
| Giờ làm việc 9:00–11:30, 14:00–17:00 | Bận, nhưng nội dung "công việc" lại hợp ngữ cảnh | Chưa ưu tiên. Thử sau nếu dữ liệu ủng hộ |

## 3. Lịch giả thuyết + thử nghiệm A/B 4 tuần đầu

| Loại bài | Khi nào | 4 tuần đầu (A/B) | Từ tuần 5 |
|---|---|---|---|
| **Bài mồi** (ảnh 4:5 + câu hỏi về nỗi đau của tập sắp ra) | **Thứ 2, 07:45** | Cố định | Giữ nguyên |
| **Video tập chính** (5 phút, 16:9) | **Thứ 3** | Tuần lẻ **11:45** · tuần chẵn **20:00** | Khung thắng (sửa `cau-hinh.json`) |
| **Reel 1** (cắt từ tập, ≤ 90 giây, 9:16) | **Thứ 5, 12:15** | Cố định | Giữ nguyên |
| **Reel 2** | Cuối tuần | Tuần lẻ **Thứ 6 20:30** · tuần chẵn **Thứ 7 09:00** | Khung thắng |
| **Bình luận ghim** (prompt + link file mẫu) | Ngay sau khi video lên (script tự đăng, **người ghim tay**) | | |

- Giờ lẻ (07:45, 11:45, 12:15) là cố ý: bài lên **trước** đỉnh lướt mạng 15 phút để kịp có tương tác ban đầu.
- **Nghỉ Tết Nguyên đán Đinh Mùi** (Mùng 1 = 06/02/2027): tạm dừng 03/02–12/02/2027. Kỳ nghỉ trải qua 2 tuần nên lịch tự lùi **2 tuần** (tập 11: 26/01, tập 12: 16/02).

## 4. Đo thế nào để chốt khung giờ

Sau mỗi bài **24 giờ**, ghi vào `theo-doi-hieu-qua.csv` các chỉ số trong Meta Business Suite → Nội dung: **Lượt xem / người tiếp cận**, **tương tác**, **thời gian xem trung bình** (video), **lượt chia sẻ**. Sau 4 tuần chạy `python phan-tich-khung-gio.py`:
- So **trung bình theo khung giờ** cho cùng loại bài (2 bài/khung, nên chỉ coi là tín hiệu sớm).
- Khung giờ nào hơn **≥ 20%** ở cả tiếp cận và thời gian xem thì chốt. Nếu chênh nhỏ hơn thì giữ thử nghiệm thêm 4 tuần.
- Đồng thời xem biểu đồ **"Thời điểm người theo dõi trực tuyến"** trong Business Suite khi trang đạt khoảng 1.000 người theo dõi.

## 5. Nguồn

- Buffer / Sprout / Hootsuite (qua tổng hợp): [eclincher.com](https://www.eclincher.com/articles/best-time-to-post-on-facebook-in-2026) · [iqfluence.io](https://iqfluence.io/public/blog/best-time-to-post-on-facebook) · [bloggingwizard.com](https://bloggingwizard.com/best-times-to-post-on-social-media/) · [nealschaffer.com](https://nealschaffer.com/best-time-to-post-on-facebook/) · [socialpilot.co](https://www.socialpilot.co/blog/best-time-to-post-on-facebook) · [recurpost.com](https://recurpost.com/?p=162435) · [timetopost.co (Reels vs ảnh)](https://timetopost.co/best-time-to-post/facebook/reels-vs-photo-posts/)
- Việt Nam: [Advertising Vietnam 2025](https://advertisingvietnam.com/article/khung-gio-vang-dang-bai-tren-cac-nen-tang-mang-xa-hoi-nam-2025-thoi-gian-tuong-tac-cao-diem-cua-facebook-roi-vao-8-9-gio-sang-khung-gio-ly-tuong-tren-tiktok-la-tu-14-17-gio-chieu-thu-tu-p26236) · [Brands Vietnam](https://www.brandsvietnam.com/congdong/topic/cap-nhat-thoi-diem-dang-noi-dung-tot-nhat-tren-facebook-theo-nganh-2025) · [MISA eShop](https://www.misaeshop.vn/?p=8859) · [24hStore](https://24hstore.vn/huong-dan-ky-thuat/gio-vang-dang-bai-facebook-n4962) · [Sapo](https://www.sapo.vn/blog/gio-vang-dang-facebook) · [timetopost.co (Việt Nam)](https://timetopost.co/best-time-to-post/facebook/vietnam/)
- Quy mô người dùng: [DataReportal Digital 2026 Vietnam](https://datareportal.com/reports/digital-2026-vietnam) · [NapoleonCat](https://stats.napoleoncat.com/facebook-users-in-viet_nam/2026/05/)
- Kỹ thuật (Graph API v26.0): [Page posts](https://developers.facebook.com/docs/pages-api/posts) · [Reels publishing](https://developers.facebook.com/docs/video-api/guides/reels-publishing) · [Page videos](https://developers.facebook.com/docs/graph-api/reference/page/videos) · [Page photos](https://developers.facebook.com/docs/graph-api/reference/page/photos)
