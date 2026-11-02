"""Tập 19 - Brief landing page + 3 ảnh gốc nặng (giống ảnh chụp máy ảnh) để Claude dựng landing page chuẩn SEO.

Chạy:  python chuan-bi.py              -> demo/yeu-cau-landing.md, demo/CLAUDE.md, demo/anh-goc/*.jpg (~3-4 MB/ảnh)
       python chuan-bi.py --giai-phap  -> chép thêm toi-uu-anh.py + landing/ tham chiếu (index.html, robots.txt, sitemap.xml, ảnh WebP)
Xem: python -m http.server 8004 -d demo/landing
"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"

YEU_CAU = """# Brief landing page: "Văn phòng công thái học trọn gói cho doanh nghiệp"

- **Mục tiêu:** thu khách hàng doanh nghiệp (B2B) để lại thông tin nhận báo giá trang bị ghế + bàn công thái học cho cả văn phòng.
- **Từ khóa chính:** ghế công thái học cho doanh nghiệp · **phụ:** nội thất văn phòng công thái học, mua ghế công thái học số lượng lớn
- **Địa chỉ đăng:** https://vpp-anphat.example/doanh-nghiep/ (khi demo: thư mục landing/)
- **Đối tượng:** trưởng phòng hành chính, nhân sự, giám đốc công ty 20–200 nhân viên.

## Nội dung bắt buộc (theo thứ tự)
1. Hero: tiêu đề có từ khóa, 1 câu giá trị, nút "Nhận báo giá trong 24 giờ", ảnh `anh-goc/van-phong.jpg`
2. 3 lợi ích chính (giảm mỏi khi ngồi lâu, ngồi thử miễn phí tại văn phòng khách*, bảo hành rõ ràng)
3. 2 gói sản phẩm: Ergo Lite (3.290.000 đ) và Ergo Pro (5.400.000 đ), ảnh `anh-goc/ghe-ergo-pro.jpg`
4. Quy trình 4 bước: khảo sát → ngồi thử → báo giá → lắp đặt
5. Câu hỏi thường gặp (4 câu) + dữ liệu có cấu trúc FAQPage
6. Form: Tên công ty, Người liên hệ, Số điện thoại, Số nhân viên, Ghi chú → (demo: gửi tới https://formspree.io/f/DEMO, thay bằng form thật)
7. Footer: thông tin doanh nghiệp (tên, địa chỉ showroom, hotline) thống nhất với dữ liệu có cấu trúc

(*) "Ngồi thử miễn phí tại văn phòng khách" CHƯA có trong CLAUDE.md → phải hỏi lại trước khi đưa lên trang.

## Yêu cầu kỹ thuật
- 1 file HTML, CSS nhúng, KHÔNG dùng framework/JS nặng. Tổng dung lượng trang (cả ảnh, ở màn hình điện thoại) < 500 KB.
- Ảnh: WebP, có width/height, srcset cho điện thoại; ảnh dưới màn hình đầu: loading="lazy"; ảnh hero: fetchpriority="high".
- SEO: title ≤ 60, meta description 140–160, canonical, Open Graph + Twitter card, lang="vi", 1 H1, JSON-LD: Organization (LocalBusiness), Product + Offer cho 2 gói, FAQPage.
- Truy cập: tương phản màu đạt WCAG AA, label cho mọi ô form, nút bấm ≥ 44px trên điện thoại.
- Kèm robots.txt + sitemap.xml.
"""


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def anh_goc(path, mau1, mau2, hinh):
    """Ảnh 4000×2667 có nhiễu hạt như ảnh máy ảnh, lưu JPEG chất lượng cao (nặng vài MB)."""
    img = Image.linear_gradient("L").resize((4000, 2667)).convert("RGB")
    img = Image.merge("RGB", [ch.point(lambda v, a=a, b=b: a + (b - a) * v // 255) for ch, a, b in zip(img.split(), mau1, mau2)])
    d = ImageDraw.Draw(img)
    for x, y, w, h, c in hinh:
        d.rounded_rectangle([x, y, x + w, y + h], radius=60, fill=c)
    nhieu = Image.effect_noise((4000, 2667), 40).convert("RGB")
    Image.blend(img, nhieu, 0.18).filter(ImageFilter.GaussianBlur(0.6)).save(path, "JPEG", quality=95)


def main():
    lam_moi(DEMO)
    (DEMO / "anh-goc").mkdir()
    (DEMO / "yeu-cau-landing.md").write_text(YEU_CAU, encoding="utf-8")
    shutil.copy(GOC.parent / "tap-16-viet-bai-chuan-seo" / "du-lieu" / "CLAUDE.md", DEMO / "CLAUDE.md")
    anh_goc(DEMO / "anh-goc" / "van-phong.jpg", (230, 236, 245), (120, 150, 190),
            [(400, 1400, 1300, 700, (60, 60, 70)), (2100, 1300, 1400, 800, (70, 70, 80)), (1100, 500, 1800, 500, (250, 250, 250))])
    anh_goc(DEMO / "anh-goc" / "ghe-ergo-pro.jpg", (245, 245, 245), (200, 205, 215),
            [(1500, 400, 1000, 1300, (30, 30, 35)), (1600, 1700, 800, 250, (40, 40, 45)), (1900, 1950, 200, 500, (90, 90, 95))])
    anh_goc(DEMO / "anh-goc" / "ngoi-thu.jpg", (250, 240, 225), (210, 180, 150),
            [(900, 900, 900, 1400, (11, 83, 148)), (2100, 800, 900, 1500, (245, 166, 35))])

    if "--giai-phap" in sys.argv:
        shutil.copy(GOC / "giai-phap" / "toi-uu-anh.py", DEMO / "toi-uu-anh.py")
        shutil.copytree(GOC / "giai-phap" / "landing", DEMO / "landing")
        subprocess.run([sys.executable, str(DEMO / "toi-uu-anh.py"), str(DEMO / "anh-goc"), str(DEMO / "landing" / "anh")],
                       check=True, stdout=subprocess.DEVNULL)
        print("Đã chép toi-uu-anh.py + landing/ tham chiếu (ảnh WebP đã tối ưu)")
    tong = sum(f.stat().st_size for f in (DEMO / "anh-goc").iterdir()) / 1024 / 1024
    print(f"Đã tạo demo/: yeu-cau-landing.md, CLAUDE.md, anh-goc/ (3 ảnh, tổng {tong:.1f} MB)")


if __name__ == "__main__":
    main()
