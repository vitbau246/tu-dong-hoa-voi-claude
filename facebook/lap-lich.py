"""Sinh lịch đăng Facebook cho cả series + nội dung từng bài + ảnh bài mồi.

Chạy:  python lap-lich.py          -> lich-dang.csv, bai-dang/*.txt, media/tap-XX/bai-moi.jpg
Chạy lại an toàn: bài đã "Đã lên lịch"/"Đã đăng" giữ nguyên giờ, post_id và trạng thái duyệt.
Đổi giờ sau thử nghiệm: sửa cau-hinh.json rồi chạy lại.
"""
import csv
import json
import sys
import textwrap
from datetime import date, datetime, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
CH = json.loads((GOC / "cau-hinh.json").read_text(encoding="utf-8"))
TAP = json.loads((GOC / "noi-dung-tap.json").read_text(encoding="utf-8"))
THU_VN = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
THU_NGAN = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
COT = ["ma", "tuan", "tap", "loai", "thoi_gian", "khung", "file_noi_dung", "file_media", "duyet", "trang_thai", "post_id", "ghi_chu"]
THU_MUC_TAP = {int(p.name[4:6]): p.name for p in GOC.parent.glob("tap-[0-9][0-9]-*")}


def hashtag():
    return " ".join(CH["hashtag_chung"])


def dt(ngay, gio):
    return datetime.fromisoformat(f"{ngay.isoformat()}T{gio}:00{CH['mui_gio']}")


def trong_ky_nghi(ngay):
    return any(date.fromisoformat(a) <= ngay <= date.fromisoformat(b) for a, b, _ in CH["nghi"])


def cac_tuan():
    """Thứ 2 của tuần đăng từng tập, tự lùi qua kỳ nghỉ."""
    thu2 = date.fromisoformat(CH["ngay_bat_dau"])
    thu2 -= timedelta(days=thu2.weekday())
    ket_qua = []
    while len(ket_qua) < len(TAP):
        if not any(trong_ky_nghi(thu2 + timedelta(days=i)) for i in range(7)):
            ket_qua.append(thu2)
        thu2 += timedelta(days=7)
    return ket_qua


def anh_bai_moi(tap, gio_video, thu_video, dich):
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), (15, 23, 42))
    d = ImageDraw.Draw(img)
    f_to = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 66)
    f_vua = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 40)
    f_nho = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 34)
    d.rectangle([0, 0, W, 14], fill=(249, 115, 22))
    d.rounded_rectangle([70, 110, 330, 180], radius=35, fill=(249, 115, 22))
    d.text((200, 145), f"TẬP {tap['tap']}", font=f_vua, fill="white", anchor="mm")
    dong_chu = textwrap.wrap(tap["mo_dau"], width=24)[:8]
    y = 220 + (H - 320 - 220 - len(dong_chu) * 92) // 2  # căn giữa khối chữ theo chiều dọc
    for dong in dong_chu:
        d.text((70, y), dong, font=f_to, fill="white")
        y += 92
    d.line([70, H - 300, W - 70, H - 300], fill=(51, 65, 85), width=3)
    d.polygon([(72, H - 254), (72, H - 222), (100, H - 238)], fill=(249, 115, 22))  # biểu tượng "phát" (Arial không có ký tự ▶)
    d.text((118, H - 260), f"{thu_video} · {gio_video}", font=f_vua, fill=(249, 115, 22))
    d.text((70, H - 195), textwrap.shorten(tap["ten"], 52, placeholder="…"), font=f_nho, fill=(203, 213, 225))
    d.text((70, H - 110), "5 phút tự động hóa · FoxFlow", font=f_nho, fill=(148, 163, 184))
    dich.parent.mkdir(parents=True, exist_ok=True)
    img.save(dich, "JPEG", quality=90)


def noi_dung(loai, tap, tap_sau, gio_video, thu_video):
    n = tap["tap"]
    if loai == "bai-moi":
        return f"{tap['cau_hoi']}\n\n👉 {thu_video} này lúc {gio_video}: Tập {n}: {tap['ten']}\n\n{hashtag()}"
    if loai == "video":
        loi = "\n".join(f"✅ {x}" for x in tap["loi_ich"])
        sau = f"\n🔔 Theo dõi trang để không lỡ Tập {tap_sau['tap']}: {tap_sau['ten']}" if tap_sau else "\n🎉 Tập cuối của series: cảm ơn bạn đã đồng hành!"
        return (f"{tap['mo_dau']}\n\nTrong 5 phút, bạn sẽ biết:\n{loi}\n\n📌 Prompt + file mẫu để làm theo: ở bình luận đầu tiên.{sau}"
                f"\n\n{CH['chu_ky']}\n{hashtag()}")
    if loai == "binh-luan":
        return (f"📌 Prompt + file mẫu Tập {n}: {CH['link_file_mau']}/tree/main/{THU_MUC_TAP.get(n, '')}\n"
                f"Chạy python chuan-bi.py là có dữ liệu y hệt video.\n💬 {tap['cau_hoi']}")
    if loai in ("reel-1", "reel-2"):
        return f"{tap[loai.replace('-', '_')]}\n\n🎬 Bản đầy đủ 5 phút: Tập {n} trên trang: {tap['ten']}\n{hashtag()}"
    raise ValueError(loai)


def main():
    cu = {}
    if (GOC / "lich-dang.csv").exists():
        with open(GOC / "lich-dang.csv", encoding="utf-8-sig") as f:
            cu = {r["ma"]: r for r in csv.DictReader(f)}
    (GOC / "bai-dang").mkdir(exist_ok=True)
    kg = CH["khung_gio"]
    dong = []

    def them(ma, tuan, tap_so, loai, thoi_gian, khung, text, media):
        (GOC / "bai-dang" / f"{ma}.txt").write_text(text, encoding="utf-8")
        r = {"ma": ma, "tuan": tuan, "tap": tap_so, "loai": loai, "thoi_gian": thoi_gian.isoformat(), "khung": khung,
             "file_noi_dung": f"bai-dang/{ma}.txt", "file_media": media, "duyet": "", "trang_thai": "", "post_id": "", "ghi_chu": ""}
        if ma in cu:
            for k in ("duyet", "post_id", "ghi_chu"):
                r[k] = cu[ma].get(k, "")
            if cu[ma].get("trang_thai") in ("Đã lên lịch", "Đã đăng", "Đã bình luận"):
                r["trang_thai"], r["thoi_gian"] = cu[ma]["trang_thai"], cu[ma]["thoi_gian"]  # không đổi bài đã đẩy lên Facebook
        dong.append(r)

    tuan_list = cac_tuan()
    for i, (tap, thu2) in enumerate(zip(TAP, tuan_list)):
        tuan = i + 1
        le = tuan % 2 == 1
        thu_nghiem = tuan <= kg["so_tuan_thu_nghiem"]
        n = tap["tap"]
        tt = f"tap-{n:02d}"
        tap_sau = TAP[i + 1] if i + 1 < len(TAP) else None

        for tr in CH["trailer"]:
            if tr["truoc_tap"] == n:
                ngay = thu2 - timedelta(days=7) + timedelta(days=tr["thu"])
                ma = f"trailer-{'phan-1' if n == 1 else 'phan-2'}"
                text = (f"🎬 {tr['ten']}: series \"5 phút tự động hóa\" với VS Code và Claude.\n"
                        f"Mỗi tuần một việc thật, 5 phút, có file mẫu để làm theo.\n"
                        f"Tập {n} lên sóng {THU_VN[kg['video']['thu']]} tới.\n\n{CH['chu_ky']}\n{hashtag()}")
                them(ma, tuan - 1, n, "video", dt(ngay, tr["gio"]), "trailer", text, f"media/{ma}.mp4")

        # Video tập chính
        v = kg["video"]
        gio_v = (v["gio_tuan_le"] if le else v["gio_tuan_chan"]) if thu_nghiem or not v["gio_sau_thu_nghiem"] else v["gio_sau_thu_nghiem"]
        dang_ab = thu_nghiem or not v["gio_sau_thu_nghiem"]
        khung_v = f"{THU_NGAN[v['thu']]}-{gio_v}" + (" (A/B)" if dang_ab else "")
        ngay_v = thu2 + timedelta(days=v["thu"])
        thu_v = THU_VN[v["thu"]]

        b = kg["bai_moi"]
        anh = GOC / "media" / tt / "bai-moi.jpg"
        anh_bai_moi(tap, gio_v, thu_v, anh)
        them(f"{tt}-bai-moi", tuan, n, "bai-moi", dt(thu2 + timedelta(days=b["thu"]), b["gio"]), f"{THU_NGAN[b['thu']]}-{b['gio']}",
             noi_dung("bai-moi", tap, tap_sau, gio_v, thu_v), f"media/{tt}/bai-moi.jpg")
        them(f"{tt}-video", tuan, n, "video", dt(ngay_v, gio_v), khung_v,
             noi_dung("video", tap, tap_sau, gio_v, thu_v), f"media/{tt}/video.mp4")
        (GOC / "bai-dang" / f"{tt}-video-binh-luan.txt").write_text(noi_dung("binh-luan", tap, tap_sau, gio_v, thu_v), encoding="utf-8")

        r1 = kg["reel_1"]
        them(f"{tt}-reel-1", tuan, n, "reel", dt(thu2 + timedelta(days=r1["thu"]), r1["gio"]), f"{THU_NGAN[r1['thu']]}-{r1['gio']}",
             noi_dung("reel-1", tap, tap_sau, gio_v, thu_v), f"media/{tt}/reel-1.mp4")
        r2 = kg["reel_2"]
        if thu_nghiem or not r2["sau_thu_nghiem"]:
            thu_r2, gio_r2 = (r2["thu_tuan_le"], r2["gio_tuan_le"]) if le else (r2["thu_tuan_chan"], r2["gio_tuan_chan"])
        else:
            thu_r2, gio_r2 = r2["sau_thu_nghiem"]["thu"], r2["sau_thu_nghiem"]["gio"]
        them(f"{tt}-reel-2", tuan, n, "reel", dt(thu2 + timedelta(days=thu_r2), gio_r2),
             f"{THU_NGAN[thu_r2]}-{gio_r2}" + (" (A/B)" if thu_nghiem or not r2["sau_thu_nghiem"] else ""),
             noi_dung("reel-2", tap, tap_sau, gio_v, thu_v), f"media/{tt}/reel-2.mp4")

    dong.sort(key=lambda r: r["thoi_gian"])
    with open(GOC / "lich-dang.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COT)
        w.writeheader()
        w.writerows(dong)
    dau, cuoi = dong[0]["thoi_gian"][:10], dong[-1]["thoi_gian"][:10]
    print(f"Đã lập {len(dong)} bài · {dau} → {cuoi} · nghỉ: {', '.join(n for *_, n in CH['nghi'])}")
    print(f"Ảnh bài mồi: media/tap-XX/bai-moi.jpg ({len(TAP)} ảnh) · Nội dung: bai-dang/")


if __name__ == "__main__":
    main()
