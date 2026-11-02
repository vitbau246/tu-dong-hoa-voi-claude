"""Tối ưu ảnh cho web: ảnh gốc từ máy ảnh/điện thoại (vài MB) -> WebP nhiều kích cỡ (vài chục KB).

Dùng: python toi-uu-anh.py anh-goc/ landing/anh/
  Mỗi ảnh tạo 2 bản: <ten>-1600.webp (máy tính) và <ten>-800.webp (điện thoại), dùng với srcset.
  In bảng trước/sau và đoạn <img> mẫu có width/height (tránh trang bị "giật" khi tải - CLS).
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
CO = (1600, 800)


def main(nguon, dich):
    nguon, dich = Path(nguon), Path(dich)
    dich.mkdir(parents=True, exist_ok=True)
    tong_truoc = tong_sau = 0
    for f in sorted(p for p in nguon.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")):
        img = ImageOps.exif_transpose(Image.open(f)).convert("RGB")  # xoay đúng chiều ảnh điện thoại
        truoc = f.stat().st_size
        tong_truoc += truoc
        sau = 0
        for w in CO:
            h = round(img.height * w / img.width)
            out = dich / f"{f.stem}-{w}.webp"
            img.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=72, method=6)
            sau += out.stat().st_size
        tong_sau += sau
        h1600 = round(img.height * 1600 / img.width)
        print(f"{f.name:28} {truoc / 1024 / 1024:6.1f} MB  →  2 bản WebP {sau / 1024:6.0f} KB")
        print(f'   <img src="anh/{f.stem}-1600.webp" srcset="anh/{f.stem}-800.webp 800w, anh/{f.stem}-1600.webp 1600w" '
              f'sizes="(max-width: 800px) 100vw, 1600px" width="1600" height="{h1600}" alt="..." loading="lazy">')
    print(f"\nTỔNG: {tong_truoc / 1024 / 1024:.1f} MB → {tong_sau / 1024:.0f} KB (giảm {100 - tong_sau / tong_truoc * 100:.1f}%)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
