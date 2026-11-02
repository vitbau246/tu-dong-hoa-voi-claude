"""Máy chủ GIẢ LẬP Graph API (v26.0) để thử dang-facebook.py mà không chạm vào Fanpage thật.

Kiểm tra đúng các luật trong tài liệu Meta:
  - Bài /feed: published=false + scheduled_publish_time trong 10 phút → 30 ngày; attached_media phải là ảnh temporary
  - /photos cho bài hẹn giờ: published=false + temporary=true (ảnh temporary không được có scheduled_publish_time)
  - /videos: scheduled_publish_time trong 10 phút → 6 tháng
  - /video_reels: start → upload (rupload, header Authorization/offset/file_size) → finish với video_state=SCHEDULED, ≤ 29 ngày
Chạy:  python gia-lap-graph.py   rồi đặt trong .env: GRAPH_URL=http://localhost:8090  RUPLOAD_URL=http://localhost:8090
       FB_PAGE_ID=1234567890  FB_PAGE_TOKEN=token-gia-lap
Xem các bài đã nhận: http://localhost:8090/
"""
import cgi
import json
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
CONG, PAGE, TOKEN, TEN = 8090, "1234567890", "token-gia-lap", "5 phút tự động hóa"
KHO = {"photos": {}, "posts": [], "reels": {}, "comments": []}
DEM = [100]


def moi_id():
    DEM[0] += 1
    return f"{PAGE}_{DEM[0]}"


class XuLy(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def tra(self, ma, j):
        b = json.dumps(j, ensure_ascii=False).encode()
        self.send_response(ma)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def loi(self, msg, ma=400):
        print(f"  ✗ TỪ CHỐI: {msg}")
        self.tra(ma, {"error": {"message": msg, "type": "OAuthException" if ma == 401 else "GraphMethodException"}})

    def tham_so(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        ct = self.headers.get("Content-Type", "")
        n = int(self.headers.get("Content-Length", 0))
        if ct.startswith("multipart/form-data"):
            fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": ct})
            for k in fs.keys():
                q[k] = fs[k].file.read() if fs[k].filename else fs[k].value
        elif n:
            raw = self.rfile.read(n)
            if "x-www-form-urlencoded" in ct:
                q.update({k: v[0] for k, v in parse_qs(raw.decode()).items()})
            else:
                q["_body"] = raw
        return u.path, q

    def kiem_cua_so(self, q, toi_da_ngay):
        if q.get("published") not in ("false", None) and "video_state" not in q:
            return "Bài phải published=false khi hẹn giờ"
        t = int(q.get("scheduled_publish_time", 0))
        con = t - time.time()
        if not 600 <= con <= toi_da_ngay * 86400:
            return f"scheduled_publish_time phải trong 10 phút → {toi_da_ngay} ngày (hiện cách {con / 86400:.1f} ngày)"
        return None

    def do_GET(self):
        path, q = self.tham_so()
        if path == "/":
            dong = "".join(f"<tr><td>{p['loai']}</td><td>{time.strftime('%d/%m/%Y %H:%M', time.localtime(p['luc']))}</td>"
                           f"<td>{p['id']}</td><td><pre>{p['chu'][:160]}</pre></td></tr>" for p in sorted(KHO["posts"], key=lambda p: p["luc"]))
            b = f"<meta charset=utf-8><h2>Graph API giả lập: {len(KHO['posts'])} bài hẹn giờ</h2><table border=1>{dong}</table>".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            return self.wfile.write(b)
        if q.get("access_token") != TOKEN:
            return self.loi("Invalid OAuth access token.", 401)
        if path == f"/v26.0/{PAGE}":
            return self.tra(200, {"id": PAGE, "name": TEN})
        self.loi("Unsupported get request", 404)

    def do_POST(self):
        path, q = self.tham_so()
        if path.startswith("/video-upload/v26.0/"):
            vid = path.rsplit("/", 1)[1]
            if self.headers.get("Authorization") != f"OAuth {TOKEN}":
                return self.loi("Thiếu/sai header Authorization: OAuth <token>", 401)
            if vid not in KHO["reels"] or int(self.headers.get("file_size", -1)) != len(q.get("_body", b"")) or self.headers.get("offset") != "0":
                return self.loi("Sai video_id, offset hoặc file_size")
            KHO["reels"][vid]["da_tai"] = True
            return self.tra(200, {"success": True})
        if q.get("access_token") != TOKEN:
            return self.loi("Invalid OAuth access token.", 401)
        if path == f"/v26.0/{PAGE}/photos":
            if not isinstance(q.get("source"), bytes):
                return self.loi("Thiếu file ảnh (source)")
            if q.get("temporary") == "true" and "scheduled_publish_time" in q:
                return self.loi("Ảnh temporary không được có scheduled_publish_time")
            pid = moi_id()
            KHO["photos"][pid] = {"temporary": q.get("temporary") == "true", "published": q.get("published")}
            return self.tra(200, {"id": pid})
        if path == f"/v26.0/{PAGE}/feed":
            if e := self.kiem_cua_so(q, 30):
                return self.loi(e)
            for m in json.loads(q.get("attached_media", "[]")):
                p = KHO["photos"].get(m["media_fbid"])
                if not p or not p["temporary"] or p["published"] != "false":
                    return self.loi("attached_media phải là ảnh đã tải với published=false, temporary=true")
            pid = moi_id()
            KHO["posts"].append({"id": pid, "loai": "bài ảnh", "luc": int(q["scheduled_publish_time"]), "chu": q.get("message", "")})
            print(f"  ✓ bài ảnh hẹn giờ {pid}")
            return self.tra(200, {"id": pid})
        if path == f"/v26.0/{PAGE}/videos":
            if not isinstance(q.get("source"), bytes):
                return self.loi("Thiếu file video (source)")
            if e := self.kiem_cua_so(q, 183):
                return self.loi(e)
            vid = moi_id().split("_")[1]
            KHO["posts"].append({"id": vid, "loai": "video", "luc": int(q["scheduled_publish_time"]), "chu": f"[{q.get('title')}] {q.get('description', '')}"})
            print(f"  ✓ video hẹn giờ {vid} ({len(q['source']):,} byte)")
            return self.tra(200, {"id": vid})
        if path == f"/v26.0/{PAGE}/video_reels":
            if q.get("upload_phase") == "start":
                vid = moi_id().split("_")[1]
                KHO["reels"][vid] = {"da_tai": False}
                return self.tra(200, {"video_id": vid, "upload_url": f"http://localhost:{CONG}/video-upload/v26.0/{vid}"})
            if q.get("upload_phase") == "finish":
                r = KHO["reels"].get(q.get("video_id"))
                if not r or not r["da_tai"]:
                    return self.loi("Chưa tải file lên rupload trước khi finish")
                if q.get("video_state") != "SCHEDULED":
                    return self.loi("Hẹn giờ Reel cần video_state=SCHEDULED")
                if e := self.kiem_cua_so(q, 29):
                    return self.loi(e)
                KHO["posts"].append({"id": q["video_id"], "loai": "reel", "luc": int(q["scheduled_publish_time"]), "chu": q.get("description", "")})
                print(f"  ✓ reel hẹn giờ {q['video_id']}")
                return self.tra(200, {"success": True})
        if m := re.fullmatch(r"/v26.0/([\w_]+)/comments", path):
            cid = moi_id()
            KHO["comments"].append({"id": cid, "obj": m.group(1), "chu": q.get("message", "")})
            print(f"  ✓ bình luận {cid} dưới {m.group(1)}")
            return self.tra(200, {"id": cid})
        self.loi(f"Unsupported post request: {path}", 404)


if __name__ == "__main__":
    print(f"Graph API GIẢ LẬP tại http://localhost:{CONG} · trang \"{TEN}\" (id {PAGE}) · token \"{TOKEN}\"")
    ThreadingHTTPServer(("127.0.0.1", CONG), XuLy).serve_forever()
