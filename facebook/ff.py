"""Gọi API điều khiển trang của FoxFlow (profile đang chạy) từ dòng lệnh.

  python ff.py shot [ten]                 # chụp màn hình -> anh-chup/<ten>.png
  python ff.py nav <url>
  python ff.py snap [max_chars]           # cây truy cập (accessibility snapshot) dạng chữ
  python ff.py click '<json body>'        # ví dụ '{"selector": "text=Tạo bài viết"}'
  python ff.py <action> '<json body>'     # type, press, click-at, keyboard, wait, evaluate
Biến môi trường: FOXFLOW_URL (mặc định http://127.0.0.1:8000), FF_PROFILE (mặc định Facebook)
"""
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
BASE = os.environ.get("FOXFLOW_URL", "http://127.0.0.1:8000") + "/api/v1/browser/" + os.environ.get("FF_PROFILE", "Facebook") + "/page"
NO_PROXY = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def goi(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, headers={"Content-Type": "application/json"},
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with NO_PROXY.open(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Lỗi {e.code}: {e.read().decode()[:500]}")


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "shot":
        r = goi("GET", "/screenshot?format=json")
        out = Path(__file__).parent / "anh-chup" / f"{a[1] if len(a) > 1 else 'man-hinh'}.png"
        out.parent.mkdir(exist_ok=True)
        out.write_bytes(base64.b64decode(r["png_base64"]))
        print(f"{out} · {r.get('url')} · {r.get('title')}")
    elif a[0] == "nav":
        print(goi("POST", "/navigate", {"url": a[1]}))
    elif a[0] == "snap":
        r = goi("GET", f"/snapshot?max_chars={a[1] if len(a) > 1 else 40000}")
        print(r.get("snapshot") or json.dumps(r, ensure_ascii=False)[:40000])
    else:
        print(json.dumps(goi("POST", "/" + a[0], json.loads(a[1]) if len(a) > 1 else {}), ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
