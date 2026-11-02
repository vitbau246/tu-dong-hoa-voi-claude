"""Máy chủ GIẢ LẬP REST API của WordPress để tập dượt / kiểm thử khi chưa có site WordPress thử nghiệm.

Hỗ trợ đúng các endpoint mà dang-wordpress.py dùng (cùng đường dẫn và định dạng JSON như WordPress thật):
  GET/POST /wp-json/wp/v2/categories   GET/POST /wp-json/wp/v2/tags   (?search=)
  POST     /wp-json/wp/v2/media        POST /wp-json/wp/v2/media/<id>   (alt_text)
  GET/POST /wp-json/wp/v2/posts
Xem bài đã nhận: http://localhost:8080/  (danh sách) · http://localhost:8080/xem/<id> (xem trước bài nháp)
Tài khoản giả lập: user "bientap" / mật khẩu ứng dụng "demo demo demo demo"

Chạy: python wp-gia-lap.py   (Ctrl+C để dừng). Đây KHÔNG phải WordPress, chỉ mô phỏng phần API cần dùng.
"""
import base64
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
CONG = 8080
TAI_KHOAN = ("bientap", "demo demo demo demo")
KHO = {"categories": [{"id": 1, "name": "Chưa phân loại"}], "tags": [], "media": [], "posts": []}
THU_MUC_MEDIA = Path("wp-gia-lap-media")


class XuLy(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[WP giả lập] {self.command} {self.path}")

    def tra(self, ma, du_lieu, kieu="application/json; charset=utf-8"):
        body = du_lieu if isinstance(du_lieu, bytes) else json.dumps(du_lieu, ensure_ascii=False).encode()
        self.send_response(ma)
        self.send_header("Content-Type", kieu)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def dung_tai_khoan(self):
        h = self.headers.get("Authorization", "")
        if h.startswith("Basic "):
            user, _, mk = base64.b64decode(h[6:]).decode().partition(":")
            return (user, mk.replace(" ", "")) == (TAI_KHOAN[0], TAI_KHOAN[1].replace(" ", ""))
        return False

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/wp-json/wp/v2/users/me":
            if not self.dung_tai_khoan():
                return self.tra(401, {"code": "rest_not_logged_in", "message": "Bạn chưa đăng nhập."})
            return self.tra(200, {"id": 1, "name": "Biên tập viên (giả lập)"})
        if u.path == "/":
            ds = "".join(f'<li><a href="/xem/{p["id"]}">#{p["id"]} [{p["status"]}] {p["title"]["rendered"]}</a></li>' for p in KHO["posts"])
            return self.tra(200, f"<meta charset=utf-8><h2>WordPress GIẢ LẬP: bài đã nhận</h2><ul>{ds or 'Chưa có bài'}</ul>".encode(), "text/html; charset=utf-8")
        if m := re.fullmatch(r"/xem/(\d+)", u.path):
            p = next((p for p in KHO["posts"] if p["id"] == int(m.group(1))), None)
            if not p:
                return self.tra(404, {"code": "rest_post_invalid_id"})
            anh = next((f'<img src="/{x["file"]}" style="max-width:100%" alt="{x["alt_text"]}">' for x in KHO["media"] if x["id"] == p["featured_media"]), "")
            meta = "".join(f"<li><b>{k}</b>: {v}</li>" for k, v in p["meta"].items())
            html = (f'<meta charset=utf-8><div style="max-width:780px;margin:auto;font-family:Segoe UI">'
                    f'<p style="background:#fde68a;padding:6px">BẢN NHÁP (trạng thái: {p["status"]}) · slug: {p["slug"]}</p>{anh}'
                    f'<h1>{p["title"]["rendered"]}</h1><ul style="color:#555">{meta}</ul>{p["content"]["rendered"]}</div>')
            return self.tra(200, html.encode(), "text/html; charset=utf-8")
        if u.path.startswith("/wp-gia-lap-media/"):
            f = THU_MUC_MEDIA / Path(u.path).name
            return self.tra(200, f.read_bytes(), "image/jpeg") if f.exists() else self.tra(404, {})
        if m := re.fullmatch(r"/wp-json/wp/v2/(categories|tags|posts)", u.path):
            tim = parse_qs(u.query).get("search", [""])[0].lower()
            return self.tra(200, [x for x in KHO[m.group(1)] if tim in json.dumps(x, ensure_ascii=False).lower()])
        self.tra(404, {"code": "rest_no_route"})

    def do_POST(self):
        u = urlparse(self.path)
        du_lieu = self.rfile.read(int(self.headers.get("Content-Length", 0)))  # đọc hết body trước khi trả lời
        if not self.dung_tai_khoan():
            return self.tra(401, {"code": "rest_not_logged_in", "message": "Sai tên đăng nhập hoặc mật khẩu ứng dụng."})
        if m := re.fullmatch(r"/wp-json/wp/v2/(categories|tags)", u.path):
            x = {"id": len(KHO[m.group(1)]) + 10, "name": json.loads(du_lieu)["name"]}
            KHO[m.group(1)].append(x)
            return self.tra(201, x)
        if u.path == "/wp-json/wp/v2/media":
            ten = re.search(r'filename="([^"]+)"', self.headers.get("Content-Disposition", "")).group(1)
            THU_MUC_MEDIA.mkdir(exist_ok=True)
            (THU_MUC_MEDIA / ten).write_bytes(du_lieu)
            x = {"id": len(KHO["media"]) + 100, "file": f"wp-gia-lap-media/{ten}", "alt_text": "", "media_type": "image"}
            KHO["media"].append(x)
            return self.tra(201, x)
        if m := re.fullmatch(r"/wp-json/wp/v2/media/(\d+)", u.path):
            x = next(x for x in KHO["media"] if x["id"] == int(m.group(1)))
            x.update(json.loads(du_lieu))
            return self.tra(200, x)
        if u.path == "/wp-json/wp/v2/posts":
            j = json.loads(du_lieu)
            p = {"id": len(KHO["posts"]) + 1000, "status": j.get("status", "draft"), "slug": j.get("slug", ""),
                 "title": {"rendered": j["title"]}, "content": {"rendered": j["content"]}, "excerpt": {"rendered": j.get("excerpt", "")},
                 "featured_media": j.get("featured_media", 0), "categories": j.get("categories", []),
                 "tags": j.get("tags", []), "meta": j.get("meta", {})}
            KHO["posts"].append(p)
            return self.tra(201, p)
        self.tra(404, {"code": "rest_no_route"})


if __name__ == "__main__":
    print(f"WordPress GIẢ LẬP chạy tại http://localhost:{CONG}  (Ctrl+C để dừng)")
    print(f"Đặt: $env:WP_URL='http://localhost:{CONG}'; $env:WP_USER='{TAI_KHOAN[0]}'; $env:WP_APP_PASSWORD='{TAI_KHOAN[1]}'")
    ThreadingHTTPServer(("127.0.0.1", CONG), XuLy).serve_forever()
