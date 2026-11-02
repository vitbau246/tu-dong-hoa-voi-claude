"""Đăng bài Markdown (định dạng tập 16) lên WordPress qua REST API, LUÔN ở trạng thái BẢN NHÁP.

Làm gì:
  1. Markdown → HTML (bảng, danh sách); ảnh chưa có file → khối "ẢNH CẦN CHỤP" nổi bật cho biên tập viên
  2. Tạo ảnh bìa 1200×630 (dùng làm ảnh đại diện + ảnh chia sẻ mạng xã hội), tải lên kèm alt text
  3. Tìm/tạo chuyên mục và thẻ
  4. Thêm schema FAQPage (JSON-LD) từ phần faq trong frontmatter
  5. Tạo bài: status=draft, slug, tóm tắt (excerpt) = mô tả SEO, meta Yoast (cần mu-plugin seo-meta-rest.php)

Cấu hình (biến môi trường; KHÔNG ghi mật khẩu vào code):
  WP_URL=https://staging.website.vn   WP_USER=ten-dang-nhap   WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
  (Mật khẩu ứng dụng: WordPress → Người dùng → Hồ sơ → Application Passwords)
Dùng:
  python dang-wordpress.py bai-viet/bai.md --chuyen-muc "Kinh nghiệm chọn mua" --the "ghế công thái học,văn phòng"
  python dang-wordpress.py bai-viet/bai.md --thu      # chạy thử: chỉ in dữ liệu sẽ gửi, không đăng
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import markdown
import requests
import yaml
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def tach(md):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", md, re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else ({}, md)


def anh_bia(tieu_de, dich):
    """Ảnh bìa 1200×630 đơn giản, đúng tỉ lệ chia sẻ Facebook/LinkedIn."""
    img = Image.new("RGB", (1200, 630), (11, 83, 148))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, 1200, 630], fill=(245, 166, 35))
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 64)
    font_nho = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)
    dong, hien = [], ""
    for tu in tieu_de.split():  # tự xuống dòng theo bề rộng
        thu = f"{hien} {tu}".strip()
        if d.textlength(thu, font=font) > 1060:
            dong.append(hien)
            hien = tu
        else:
            hien = thu
    dong.append(hien)
    y = 300 - len(dong) * 40
    for dg in dong:
        d.text((70, y), dg, font=font, fill="white")
        y += 82
    d.text((70, 577), "Văn phòng phẩm An Phát", font=font_nho, fill=(11, 83, 148))
    img.save(dich, "JPEG", quality=88)
    return dich


def html_tu_markdown(body, thu_muc_bai):
    body = re.sub(r"^# .*\n", "", body, count=1)  # H1 = tiêu đề bài trên WordPress, không lặp trong nội dung

    def anh(m):
        alt, src = m.group(1), m.group(2)
        if (thu_muc_bai / src).exists():
            return m.group(0)
        return (f'\n<p style="border:2px dashed #f5a623;padding:12px;background:#fff8e6">'
                f"<strong>ẢNH CẦN CHỤP:</strong> {alt}</p>\n")

    body = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", anh, body)
    return markdown.markdown(body, extensions=["tables", "sane_lists"])


def schema_faq(faq):
    if not faq:
        return ""
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]}
    # Khối HTML tùy biến của trình soạn thảo Gutenberg (cần tài khoản có quyền unfiltered_html, ví dụ Quản trị viên)
    return f'\n<!-- wp:html -->\n<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n<!-- /wp:html -->\n'


class WP:
    def __init__(self, url, user, mat_khau):
        self.api = url.rstrip("/") + "/wp-json/wp/v2"
        self.s = requests.Session()
        self.s.auth = (user, mat_khau)
        if re.match(r"https?://(localhost|127\.)", url):
            self.s.trust_env = False  # máy có proxy công ty: địa chỉ nội bộ đi thẳng

    def goi(self, method, path, **kw):
        r = self.s.request(method, f"{self.api}/{path}", timeout=60, **kw)
        if r.status_code >= 400:
            sys.exit(f"Lỗi WordPress {r.status_code} khi {method} {path}: {r.text[:300]}")
        return r.json()

    def kiem_tra_dang_nhap(self):
        """Gọi /users/me trước khi tải gì lên: sai mật khẩu thì báo ngay, rõ ràng."""
        r = self.s.get(f"{self.api}/users/me", timeout=30)
        if r.status_code in (401, 403):
            sys.exit("Không đăng nhập được WordPress: kiểm tra WP_USER và mật khẩu ỨNG DỤNG (không phải mật khẩu đăng nhập).")
        if r.status_code >= 400:
            sys.exit(f"Lỗi WordPress {r.status_code}: {r.text[:200]}")
        return r.json().get("name", "")

    def tim_hoac_tao(self, loai, ten):
        for t in self.goi("GET", loai, params={"search": ten, "per_page": 100}):
            if t["name"].lower() == ten.lower():
                return t["id"]
        return self.goi("POST", loai, json={"name": ten})["id"]

    def tai_anh(self, path, alt):
        media = self.goi("POST", "media", data=Path(path).read_bytes(),
                         headers={"Content-Disposition": f'attachment; filename="{Path(path).name}"', "Content-Type": "image/jpeg"})
        self.goi("POST", f"media/{media['id']}", json={"alt_text": alt})
        return media["id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bai")
    ap.add_argument("--chuyen-muc", default="Kinh nghiệm chọn mua")
    ap.add_argument("--the", default="")
    ap.add_argument("--thu", action="store_true", help="chạy thử, không đăng")
    a = ap.parse_args()

    bai = Path(a.bai)
    fm, body = tach(bai.read_text(encoding="utf-8"))
    h1 = re.search(r"^# (.*)$", body, re.M)
    tieu_de_bai = h1.group(1).strip() if h1 else fm["title"]
    noi_dung = html_tu_markdown(body, bai.parent) + schema_faq(fm.get("faq"))
    bia = anh_bia(fm["title"], bai.with_suffix(".bia.jpg"))
    the = [t.strip() for t in a.the.split(",") if t.strip()]
    meta = {"_yoast_wpseo_title": fm["title"], "_yoast_wpseo_metadesc": fm["meta_description"],
            "_yoast_wpseo_focuskw": fm.get("focus_keyword", "")}

    print(f"Bài: {tieu_de_bai}\nSlug: {fm['slug']} · Chuyên mục: {a.chuyen_muc} · Thẻ: {the}")
    print(f"Ảnh bìa: {bia} · FAQ schema: {len(fm.get('faq') or [])} câu · HTML: {len(noi_dung):,} ký tự")
    con_cho_anh = noi_dung.count("ẢNH CẦN CHỤP")
    if a.thu:
        print(f"[--thu] Không đăng. {con_cho_anh} ảnh còn cần chụp. Meta SEO: {json.dumps(meta, ensure_ascii=False)}")
        return

    url, user, mk = (os.environ.get(k) for k in ("WP_URL", "WP_USER", "WP_APP_PASSWORD"))
    if not all((url, user, mk)):
        sys.exit("Thiếu WP_URL / WP_USER / WP_APP_PASSWORD trong biến môi trường")
    wp = WP(url, user, mk)
    print(f"Đăng nhập WordPress: {wp.kiem_tra_dang_nhap()} ✓")
    anh_id = wp.tai_anh(bia, f"Ảnh bìa bài viết: {tieu_de_bai}")
    bai_wp = wp.goi("POST", "posts", json={
        "title": tieu_de_bai, "slug": fm["slug"], "status": "draft",
        "content": noi_dung, "excerpt": fm["meta_description"], "featured_media": anh_id,
        "categories": [wp.tim_hoac_tao("categories", a.chuyen_muc)],
        "tags": [wp.tim_hoac_tao("tags", t) for t in the],
        "meta": meta,
    })
    print(f"\n✅ Đã tạo BẢN NHÁP #{bai_wp['id']} (status={bai_wp['status']})")
    print(f"   Xem trước / duyệt: {url.rstrip('/')}/wp-admin/post.php?post={bai_wp['id']}&action=edit")
    if con_cho_anh:
        print(f"   ⚠️ Còn {con_cho_anh} ảnh cần chụp và thay trước khi xuất bản")


if __name__ == "__main__":
    main()
