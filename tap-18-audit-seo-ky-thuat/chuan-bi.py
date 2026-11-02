"""Tập 18 - Website tĩnh 15 trang (hư cấu) gài sẵn 12 loại lỗi SEO kỹ thuật để audit và tự sửa.

Chạy:  python chuan-bi.py              -> demo/website/ (mã nguồn site), dap-an.json
       python chuan-bi.py --giai-phap  -> chép thêm kiem-tra-ky-thuat.py
Mở web: python -m http.server 8002 -d demo/website   -> http://localhost:8002
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
WEB = DEMO / "website"
SITE = "https://vpp-anphat.example"

# đường dẫn: (title, meta_description hoặc None, nội dung chính, các link nội bộ)
TRANG = {
    "index.html": ("Văn phòng phẩm An Phát - Thiết bị văn phòng chính hãng", "Văn phòng phẩm, ghế công thái học, máy in, giấy A4 chính hãng cho doanh nghiệp tại Hà Nội và TP.HCM. Giao nhanh trong ngày, bảo hành rõ ràng.",
                   "Chào mừng đến An Phát", ["ghe-cong-thai-hoc/index.html", "san-pham/ghe-ergo-pro.html", "san-pham/may-in-hp-107w.html", "blog/index.html", "khuyen-mai-cu.html", "lien-he.html"]),
    "ghe-cong-thai-hoc/index.html": ("Ghế công thái học chính hãng - An Phát", "Ghế công thái học chính hãng, bảo hành 24 tháng khung và cơ cấu. Ngồi thử tại showroom Hà Nội, TP.HCM. Giao miễn phí nội thành đơn từ 2 triệu.",
                                     "Ghế công thái học", ["san-pham/ghe-ergo-pro.html", "san-pham/ghe-ergo-lite.html", "blog/cach-chon-ghe.html"]),
    "san-pham/ghe-ergo-pro.html": ("Ghế công thái học Ergo Pro - An Phát", "Ghế Ergo Pro tay vịn 4D, tựa đầu, đỡ thắt lưng chỉnh được. Bảo hành 24 tháng. Giá 5.400.000 đ, giao miễn phí nội thành Hà Nội và TP.HCM.",
                                   "Ergo Pro", ["ghe-cong-thai-hoc/index.html", "san-pham/ghe-ergo-lite.html"]),
    "san-pham/ghe-ergo-lite.html": ("Ghế công thái học Ergo Pro - An Phát", "Ghế Ergo Lite gọn nhẹ, lưng lưới thoáng khí, đỡ thắt lưng chỉnh được, bảo hành 24 tháng. Giá 3.290.000 đ, lựa chọn tốt cho ngân sách vừa phải.",
                                    "Ergo Lite", ["ghe-cong-thai-hoc/index.html"]),
    "san-pham/may-in-hp-107w.html": ("Máy in laser HP 107w chính hãng giá tốt nhất thị trường năm 2026 tại Hà Nội và TPHCM - An Phát", None,
                                     "Máy in HP 107w", ["san-pham/hop-muc-hp-107a.html", "san-pham/may-chieu-epson.html"]),
    "san-pham/hop-muc-hp-107a.html": ("Hộp mực HP 107A chính hãng - An Phát", "Hộp mực HP 107A chính hãng cho máy in HP 107w, in khoảng 1.000 trang. Giao nhanh trong ngày tại Hà Nội và TP.HCM, xuất hóa đơn VAT đầy đủ.",
                                      "Hộp mực HP 107A", ["san-pham/may-in-hp-107w.html"]),
    "san-pham/ban-nang-ha.html": ("Bàn nâng hạ điện - An Phát", None, "Bàn nâng hạ điện", ["ghe-cong-thai-hoc/index.html"]),
    "blog/index.html": ("Blog kinh nghiệm văn phòng - An Phát", "Kinh nghiệm chọn ghế công thái học, máy in, bố trí văn phòng hiệu quả từ đội ngũ tư vấn của An Phát. Cập nhật mỗi tuần, đọc miễn phí.",
                        "Blog", ["blog/cach-chon-ghe.html", "blog/bo-tri-van-phong.html", "blog/bai-da-xoa.html"]),
    "blog/cach-chon-ghe.html": ("Cách chọn ghế công thái học cho người Việt - An Phát", "Hướng dẫn chọn ghế công thái học theo chiều cao, cân nặng và ngân sách: 7 tiêu chí quan trọng, bảng so sánh và kinh nghiệm ngồi thử trước khi mua.",
                                "Cách chọn ghế công thái học", ["san-pham/ghe-ergo-pro.html", "ghe-cong-thai-hoc/index.html"]),
    "blog/bo-tri-van-phong.html": ("Bố trí văn phòng 20m2 hiệu quả cho 6 người làm việc thoải mái và chuyên nghiệp nhất - An Phát", "Gợi ý bố trí văn phòng 20m2 cho 6 người: kích thước bàn, lối đi, ánh sáng, ổ điện và những lỗi hay gặp khiến văn phòng nhỏ trở nên chật chội.",
                                   "Bố trí văn phòng 20m2", ["san-pham/ban-nang-ha.html"]),
    "blog/huong-dan-bao-quan-ghe.html": ("Hướng dẫn bảo quản ghế lưới văn phòng - An Phát", "Cách vệ sinh và bảo quản ghế lưới văn phòng đúng cách để lưới không chùng, piston bền: tần suất vệ sinh, dung dịch nên dùng và những điều cần tránh.",
                                         "Bảo quản ghế lưới", ["ghe-cong-thai-hoc/index.html"]),
    "lien-he.html": ("Liên hệ - An Phát", "Liên hệ Văn phòng phẩm An Phát: hotline, địa chỉ showroom Hà Nội và TP.HCM, giờ mở cửa. Ngồi thử ghế công thái học trước khi mua.",
                     "Liên hệ", ["index.html", "chinh-sach-bao-hanh.html"]),
    "chinh-sach-bao-hanh.html": ("Chính sách bảo hành - An Phát", "Chính sách bảo hành An Phát: ghế công thái học 24 tháng khung và cơ cấu, 12 tháng đệm và lưới; đổi trả trong 7 ngày nếu lỗi nhà sản xuất.",
                                 "Chính sách bảo hành", ["lien-he.html"]),
    "gioi-thieu.html": ("Giới thiệu - An Phát", "Văn phòng phẩm An Phát: hơn 10 năm cung cấp thiết bị văn phòng cho doanh nghiệp. Showroom ngồi thử tại Hà Nội và TP.HCM, tư vấn tận tâm.",
                        "Giới thiệu An Phát", ["lien-he.html"]),
    "khuyen-mai.html": ("Khuyến mãi tháng 11 - An Phát", "Chương trình khuyến mãi tháng 11 tại An Phát: ưu đãi ghế công thái học, combo giấy A4 và hộp mực cho doanh nghiệp. Số lượng có hạn, xem ngay.",
                        "Khuyến mãi", ["san-pham/ghe-ergo-lite.html"]),
}
# Lỗi gài thêm (ngoài title trùng / quá dài / thiếu mô tả đã nằm trong bảng trên)
NOINDEX = ["ghe-cong-thai-hoc/index.html"]
HAI_H1 = ["blog/cach-chon-ghe.html"]
KHONG_H1 = ["khuyen-mai.html"]
KHONG_CANONICAL = ["lien-he.html", "gioi-thieu.html", "khuyen-mai.html"]
CANONICAL_SAI = {"san-pham/ghe-ergo-lite.html": "index.html"}
KHONG_VIEWPORT = ["blog/bo-tri-van-phong.html"]
ANH_THIEU_ALT = {"index.html": 1, "san-pham/ghe-ergo-pro.html": 2, "blog/bo-tri-van-phong.html": 1}


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def html(duong_dan, title, meta, h, links):
    sau = duong_dan.count("/")
    goc = "../" * sau
    head = [f"<title>{title}</title>"]
    if duong_dan not in KHONG_VIEWPORT:
        head.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    if meta:
        head.append(f'<meta name="description" content="{meta}">')
    if duong_dan in NOINDEX:
        head.append('<meta name="robots" content="noindex, follow">')
    if duong_dan in CANONICAL_SAI:
        head.append(f'<link rel="canonical" href="{SITE}/{CANONICAL_SAI[duong_dan]}">')
    elif duong_dan not in KHONG_CANONICAL:
        head.append(f'<link rel="canonical" href="{SITE}/{duong_dan}">')
    tieu_de = "" if duong_dan in KHONG_H1 else f"<h1>{h}</h1>"
    if duong_dan in HAI_H1:
        tieu_de += f"<h1>{h}: 7 tiêu chí</h1>"
    anh = ""
    so_thieu = ANH_THIEU_ALT.get(duong_dan, 0)
    for i in range(2 if duong_dan in ANH_THIEU_ALT else 1):
        alt = "" if i < so_thieu else f' alt="{h} - ảnh {i + 1}"'
        src = f"{goc}anh/hero.png" if duong_dan == "index.html" and i == 0 else f"{goc}anh/anh-nho.jpg"
        anh += f'<img src="{src}"{alt} width="600">'
    lk = "".join(f'<li><a href="{goc}{l}">{l}</a></li>' for l in links)
    noi_dung = (f"<p>{h} - nội dung mẫu của website hư cấu phục vụ video hướng dẫn audit SEO kỹ thuật. " * 6) + "</p>"
    return (f'<!doctype html><html lang="vi"><head><meta charset="utf-8">{"".join(head)}</head>'
            f"<body><nav><a href='{goc}index.html'>Trang chủ</a></nav>{tieu_de}{anh}{noi_dung}<ul>{lk}</ul></body></html>")


def main():
    lam_moi(DEMO)
    (WEB / "anh").mkdir(parents=True)
    for duong_dan, (title, meta, h, links) in TRANG.items():
        f = WEB / duong_dan
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(html(duong_dan, title, meta, h, links), encoding="utf-8")
    # Ảnh hero quá nặng (PNG không nén, ~2,7 MB) và một ảnh nhỏ bình thường
    Image.effect_noise((1600, 600), 90).convert("RGB").save(WEB / "anh" / "hero.png", optimize=False)
    Image.new("RGB", (600, 400), (11, 83, 148)).save(WEB / "anh" / "anh-nho.jpg", quality=80)
    (WEB / "robots.txt").write_text("User-agent: *\nDisallow: /san-pham/\nDisallow: /admin/\n", encoding="utf-8")

    if "--giai-phap" in sys.argv:
        shutil.copy(GOC / "giai-phap" / "kiem-tra-ky-thuat.py", DEMO / "kiem-tra-ky-thuat.py")
        print("Đã chép kiem-tra-ky-thuat.py vào demo/")

    dap_an = {
        "so_trang": len(TRANG),
        "NGHIEM_TRONG": {"robots.txt chặn /san-pham/ (5 trang sản phẩm)": True, "noindex trên danh mục chính": NOINDEX},
        "CAO": {"canonical trỏ sai": CANONICAL_SAI, "link nội bộ gãy": ["khuyen-mai-cu.html (từ index)", "blog/bai-da-xoa.html (từ blog)", "san-pham/may-chieu-epson.html (từ máy in)"],
                "trùng title": ["san-pham/ghe-ergo-pro.html", "san-pham/ghe-ergo-lite.html"], "không có sitemap.xml": True},
        "TRUNG_BINH": {"thiếu meta description": ["san-pham/may-in-hp-107w.html", "san-pham/ban-nang-ha.html"],
                       "H1: 2 thẻ": HAI_H1, "H1: không có": KHONG_H1, "trang mồ côi (không có link trỏ tới)": ["blog/huong-dan-bao-quan-ghe.html", "gioi-thieu.html", "khuyen-mai.html"],
                       "thiếu viewport (mobile)": KHONG_VIEWPORT, "ảnh hero quá nặng": "anh/hero.png (~2,7 MB PNG)"},
        "THAP": {"title > 60 ký tự": ["san-pham/may-in-hp-107w.html", "blog/bo-tri-van-phong.html"],
                 "thiếu canonical": KHONG_CANONICAL, "ảnh thiếu alt": f"{sum(ANH_THIEU_ALT.values())} ảnh"},
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã tạo demo/website/ ({len(TRANG)} trang, robots.txt, ảnh), dap-an.json")


if __name__ == "__main__":
    main()
