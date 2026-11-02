"""Dựng video từ kịch bản cảnh (JSON): lồng tiếng tiếng Việt (edge-tts) + hình cảnh (HTML → PNG) + phụ đề + ghép bằng ffmpeg.

Dùng:  python dung-video.py canh/tap-01.json            -> xuat/tap-01.mp4 (1920×1080) + xuat/tap-01-<reel>.mp4 (1080×1920)
       python dung-video.py canh/tap-01.json --chi reel-1  -> chỉ dựng một bản (tên bản chính là "chinh")
Kịch bản cảnh: xem canh/tap-01.json. Mỗi cảnh: loai (hook/the/prompt/claude/bang/cay/danh-sach/so-lieu/canh-bao/ket),
nội dung theo loại, "loi" (lời đọc), "buoc" (chỉ số bước đang sáng, tùy chọn), "that": true nếu dữ liệu lấy từ phiên chạy thật.
"""
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import edge_tts
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
FPS = 30
KHUNG = {"ngang": (1920, 1080, 56, 2, 44, 90), "doc": (1080, 1920, 30, 3, 52, 260)}  # w, h, ký tự/dòng, dòng/khúc, cỡ chữ, cách đáy


def chay(cmd):
    r = subprocess.run(cmd, cwd=GOC, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit(f"Lỗi lệnh: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-1500:]}")
    return r.stdout


def thoi_luong(f):
    return float(chay(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).strip())


def tts(chu, giong, toc_do):
    f = GOC / "cache" / "tts" / (hashlib.sha1(f"{giong}|{toc_do}|{chu}".encode()).hexdigest()[:16] + ".mp3")
    if f.exists() and f.stat().st_size == 0:
        f.unlink()  # file hỏng từ lần lỗi trước
    if not f.exists():
        f.parent.mkdir(parents=True, exist_ok=True)
        for lan in range(4):  # máy chủ đọc đôi khi không trả âm thanh (mạng/giới hạn tạm thời): thử lại
            try:
                asyncio.run(edge_tts.Communicate(chu, giong, rate=toc_do, proxy=os.environ.get("HTTPS_PROXY")).save(str(f)))
                break
            except edge_tts.exceptions.EdgeTTSException as e:
                f.unlink(missing_ok=True)
                if lan == 3:
                    sys.exit(f"Lồng tiếng thất bại sau 4 lần: {e}\nĐoạn: {chu[:120]}")
                time.sleep(5 * (lan + 1))
    return f


def khuc_phu_de(loi, ky_tu, so_dong):
    """Chia lời đọc thành các khúc phụ đề (mỗi khúc ≤ so_dong dòng × ky_tu ký tự)."""
    cau = [c.strip() for c in re.split(r"(?<=[.!?…])\s+", loi) if c.strip()]
    khuc = []
    for c in cau:
        dong = textwrap.wrap(c, ky_tu)
        for i in range(0, len(dong), so_dong):
            khuc.append("\n".join(dong[i:i + so_dong]))
    return khuc


def dung_ban(kb, ten_ban, canh_list, huong, trang):
    w, h, ky_tu, so_dong, co_chu, day = KHUNG[huong]
    tam = GOC / "cache" / kb["ten"] / ten_ban
    tam.mkdir(parents=True, exist_ok=True)
    meta = {"tap": kb["tap"], "phien_ban": kb.get("phien_ban", ""), "buoc": kb.get("buoc")}
    trang.set_viewport_size({"width": w, "height": h})
    trang.goto((GOC / "khuon" / "canh.html").as_uri())
    trang.wait_for_function("document.fonts.ready.then(() => true)")
    clip = []
    for i, c in enumerate(canh_list):
        trang.evaluate("([c, m]) => render(c, m)", [c, meta])
        trang.wait_for_timeout(120)
        nen = tam / f"{i:02d}.png"
        trang.screenshot(path=str(nen))
        am = tts(c["loi"], kb.get("giong", "vi-VN-NamMinhNeural"), kb.get("toc_do", "+6%"))
        d_am = thoi_luong(am)
        d = round(d_am + c.get("nghi", 0.45), 2)
        n = int(d * FPS)
        khuc = khuc_phu_de(c["loi"], ky_tu, so_dong)
        tong = sum(len(k) for k in khuc)
        loc, t = [], 0.0
        for j, k in enumerate(khuc):
            f = tam / f"{i:02d}-{j}.txt"
            f.write_bytes(k.encode("utf-8"))  # khong dung write_text: Windows doi xuong dong thanh CRLF, drawtext hien thanh dong trong
            dk = d_am * len(k) / tong
            loc.append(f"drawtext=fontfile=fonts/BeVietnamPro-Medium.ttf:textfile={f.relative_to(GOC).as_posix()}:"
                       f"fontsize={co_chu}:fontcolor=white:line_spacing=14:text_align=C:box=1:boxcolor=black@0.62:boxborderw=22:"
                       f"x=(w-text_w)/2:y=h-text_h-{day}:enable='between(t,{t:.2f},{t + dk:.2f})'")
            t += dk
        zoom = f"scale={int(w * 1.5)}:-1,zoompan=z='1+0.03*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={FPS}"
        ra = tam / f"{i:02d}.mp4"
        chay(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-t", str(d), "-i", str(nen.relative_to(GOC)),
              "-i", str(am), "-filter_complex", f"[0:v]{zoom},{','.join(loc)},format=yuv420p[v];[1:a]apad,aresample=48000[a]",
              "-map", "[v]", "-map", "[a]", "-t", str(d), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
              "-c:a", "aac", "-b:a", "160k", "-ac", "2", str(ra.relative_to(GOC))])
        clip.append(ra)
        print(f"  cảnh {i + 1:>2}/{len(canh_list)} · {c['loai']:<9} · {d:5.1f}s", flush=True)
    ds = tam / "ds.txt"
    ds.write_text("".join(f"file '{p.name}'\n" for p in clip), encoding="utf-8")
    ra = GOC / "xuat" / (f"{kb['ten']}.mp4" if ten_ban == "chinh" else f"{kb['ten']}-{ten_ban}.mp4")
    ra.parent.mkdir(exist_ok=True)
    # Ghép + chuẩn hóa âm lượng về -14 LUFS (mức phổ biến của mạng xã hội); hình giữ nguyên, không mã hóa lại
    chay(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(ds.relative_to(GOC)), "-c:v", "copy",
          "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
          str(ra.relative_to(GOC))])
    print(f"✅ {ra.relative_to(GOC)} · {thoi_luong(ra):.1f} giây · {ra.stat().st_size / 1e6:.1f} MB")
    return ra


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    kb = json.loads((GOC / sys.argv[1]).read_text(encoding="utf-8"))
    chi = sys.argv[sys.argv.index("--chi") + 1] if "--chi" in sys.argv else None
    # Lồng tiếng TRƯỚC khi mở Playwright (Playwright sync chiếm event loop, asyncio.run không chạy được bên trong)
    tat_ca = kb["canh"] + [x for r in kb.get("reels", []) for x in r["canh"] if isinstance(x, dict)]
    for i, c in enumerate(tat_ca, 1):
        tts(c["loi"], kb.get("giong", "vi-VN-NamMinhNeural"), kb.get("toc_do", "+6%"))
        print(f"\r  lồng tiếng {i}/{len(tat_ca)}", end="", flush=True)
    print()
    with sync_playwright() as p:
        trinh_duyet = p.chromium.launch(channel="msedge")
        trang = trinh_duyet.new_page()
        if chi in (None, "chinh"):
            print(f"Dựng bản chính {kb['ten']} (16:9)")
            dung_ban(kb, "chinh", kb["canh"], "ngang", trang)
        for r in kb.get("reels", []):
            if chi in (None, r["ten"]):
                print(f"Dựng {r['ten']} (9:16)")
                canh = [kb["canh"][x] if isinstance(x, int) else x for x in r["canh"]]
                dung_ban({**kb, "buoc": None}, r["ten"], canh, "doc", trang)
        trinh_duyet.close()


if __name__ == "__main__":
    main()
