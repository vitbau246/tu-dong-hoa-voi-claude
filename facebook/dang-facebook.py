"""Đẩy lịch đăng lên Fanpage "5 phút tự động hóa" qua Graph API: LUÔN là bài HẸN GIỜ, không bao giờ đăng ngay.

Lệnh:
  python dang-facebook.py                    # (mặc định) chạy thử: in những gì SẼ được lên lịch, không gửi gì
  python dang-facebook.py --kiem-tra         # kiểm tra token + đúng tên trang
  python dang-facebook.py --duyet tap-01     # đánh dấu đã duyệt (mã bài, "tap-01", "trailer-phan-1" hoặc "tat-ca")
  python dang-facebook.py --len-lich         # lên lịch THẬT các bài: đã duyệt + có media + trong cửa sổ 28 ngày
  python dang-facebook.py --binh-luan        # đăng bình luận "prompt + file mẫu" dưới video ĐÃ lên sóng (người tự ghim)
Cấu hình trong file .env (KHÔNG đưa lên git):
  FB_PAGE_ID=...            FB_PAGE_TOKEN=...      (Page access token, xem huong-dan-token.md)
  GRAPH_URL=https://graph.facebook.com   RUPLOAD_URL=https://rupload.facebook.com   GRAPH_VERSION=v26.0   (tùy chọn)

An toàn:
  - Facebook chỉ nhận hẹn giờ 10 phút → 30 ngày (Reels: 29 ngày) nên dùng cửa sổ 20 phút → 28 ngày, chạy lại mỗi ngày (cuốn chiếu).
  - Bài đã qua giờ mà chưa lên lịch: đánh dấu "Lỡ giờ", KHÔNG đăng bù.
  - Bài mồi chỉ lên lịch khi video của tập đó đã có file (không quảng bá video chưa tồn tại).
  - Mọi bài hẹn giờ hiện trong Meta Business Suite → Lịch: xem, sửa hoặc xóa trước giờ lên sóng.
"""
import csv
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
LICH = GOC / "lich-dang.csv"
CH = json.loads((GOC / "cau-hinh.json").read_text(encoding="utf-8"))
SOM_NHAT, MUON_NHAT = timedelta(minutes=20), timedelta(days=28)


def doc_env():
    f = GOC / ".env"
    if f.exists():
        for dong in f.read_text(encoding="utf-8").splitlines():
            if "=" in dong and not dong.lstrip().startswith("#"):
                k, v = dong.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))


def doc_lich():
    with open(LICH, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def ghi_lich(ds):
    with open(LICH, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(ds[0].keys()))
        w.writeheader()
        w.writerows(ds)


class Graph:
    def __init__(self):
        self.page, self.token = os.environ.get("FB_PAGE_ID"), os.environ.get("FB_PAGE_TOKEN")
        if not self.page or not self.token:
            sys.exit("Thiếu FB_PAGE_ID / FB_PAGE_TOKEN trong .env (xem huong-dan-token.md)")
        ver = os.environ.get("GRAPH_VERSION", "v26.0")
        self.api = f"{os.environ.get('GRAPH_URL', 'https://graph.facebook.com').rstrip('/')}/{ver}"
        self.rupload = f"{os.environ.get('RUPLOAD_URL', 'https://rupload.facebook.com').rstrip('/')}/video-upload/{ver}"
        self.s = requests.Session()
        if any(h in self.api for h in ("localhost", "127.0.0.1")):
            self.s.trust_env = False  # máy giả lập: không đi qua proxy công ty

    def goi(self, method, path, url=None, **kw):
        kw.setdefault("timeout", 600)
        data = kw.pop("data", {}) or {}
        if "headers" not in kw:
            data["access_token"] = self.token
        try:
            r = self.s.request(method, url or f"{self.api}/{path}", data=data if method == "POST" else None,
                               params=data if method == "GET" else None, **kw)
        except requests.RequestException as e:
            raise RuntimeError(f"không kết nối được {url or self.api} ({type(e).__name__}). Kiểm tra mạng/proxy công ty") from e
        try:
            j = r.json()
        except ValueError:
            j = {"error": {"message": r.text[:300]}}
        if r.status_code >= 400 or "error" in j:
            raise RuntimeError(f"{method} {path or url}: {j.get('error', {}).get('message', r.text[:300])}")
        return j

    def ten_trang(self):
        return self.goi("GET", self.page, data={"fields": "id,name"})["name"]

    def bai_anh(self, anh, chu, luc):
        # Theo tài liệu Meta: ảnh cho bài hẹn giờ tải lên dạng published=false + temporary=true, rồi gắn vào bài /feed
        with open(anh, "rb") as f:
            p = self.goi("POST", f"{self.page}/photos", data={"published": "false", "temporary": "true"}, files={"source": f})
        return self.goi("POST", f"{self.page}/feed", data={
            "message": chu, "published": "false", "scheduled_publish_time": str(luc),
            "attached_media": json.dumps([{"media_fbid": p["id"]}])})["id"]

    def video(self, file, tieu_de, chu, luc):
        with open(file, "rb") as f:
            return self.goi("POST", f"{self.page}/videos", files={"source": f}, data={
                "title": tieu_de, "description": chu, "published": "false", "scheduled_publish_time": str(luc)})["id"]

    def reel(self, file, chu, luc):
        bat_dau = self.goi("POST", f"{self.page}/video_reels", data={"upload_phase": "start"})
        vid = bat_dau["video_id"]
        noi_dung = Path(file).read_bytes()
        self.goi("POST", None, url=f"{self.rupload}/{vid}", data=noi_dung,
                 headers={"Authorization": f"OAuth {self.token}", "offset": "0", "file_size": str(len(noi_dung))})
        self.goi("POST", f"{self.page}/video_reels", data={
            "upload_phase": "finish", "video_id": vid, "video_state": "SCHEDULED",
            "scheduled_publish_time": str(luc), "description": chu})
        return vid

    def binh_luan(self, obj_id, chu):
        return self.goi("POST", f"{obj_id}/comments", data={"message": chu})["id"]


def co_media(r):
    return (GOC / r["file_media"]).exists() and (GOC / r["file_media"]).stat().st_size > 0


def can_len_lich(r, ds, bay_gio):
    """Trả về (được lên lịch?, lý do)."""
    luc = datetime.fromisoformat(r["thoi_gian"])
    if r["trang_thai"] in ("Đã lên lịch", "Đã đăng", "Đã bình luận"):
        return False, r["trang_thai"]
    if luc < bay_gio + SOM_NHAT:
        return False, "Lỡ giờ" if luc < bay_gio else "Quá sát giờ (< 20 phút)"
    if luc > bay_gio + MUON_NHAT:
        return False, "Ngoài cửa sổ 28 ngày (chạy lại sau)"
    if not co_media(r):
        return False, f"Chưa có media: {r['file_media']}"
    if r["loai"] == "bai-moi":
        video = next((x for x in ds if x["ma"] == r["ma"].replace("bai-moi", "video")), None)
        if not video or not co_media(video):
            return False, "Chờ video của tập (không quảng bá video chưa có)"
    if r["duyet"].strip().lower() != "x":
        return False, "Chưa duyệt (python dang-facebook.py --duyet <mã>)"
    return True, "Sẵn sàng"


def main():
    try:
        chay()
    except RuntimeError as e:
        sys.exit(f"❌ Facebook từ chối: {e}\n   Token sai/hết hạn hoặc thiếu quyền? Xem huong-dan-token.md (mục Xử lý lỗi).")


def chay():
    doc_env()
    ds = doc_lich()
    bay_gio = datetime.now(timezone.utc)
    lenh = sys.argv[1] if len(sys.argv) > 1 else "--thu"

    if lenh == "--duyet":
        muc = sys.argv[2] if len(sys.argv) > 2 else sys.exit("Ví dụ: --duyet tap-01  |  --duyet tap-01-reel-1  |  --duyet tat-ca")
        n = 0
        for r in ds:
            if muc == "tat-ca" or r["ma"] == muc or r["ma"].startswith(muc + "-"):
                r["duyet"], n = "x", n + 1
        ghi_lich(ds)
        print(f"Đã duyệt {n} bài khớp '{muc}'. Nhớ đọc nội dung trong bai-dang/ trước khi duyệt.")
        return

    if lenh == "--kiem-tra":
        ten = Graph().ten_trang()
        dung = ten.strip().lower() == CH["ten_trang_mong_doi"].lower()
        print(f"Token hợp lệ · Trang: \"{ten}\" · {'✅ ĐÚNG trang' if dung else '❌ SAI trang, mong đợi: ' + CH['ten_trang_mong_doi']}")
        sys.exit(0 if dung else 1)

    if lenh in ("--thu", "--len-lich"):
        that = lenh == "--len-lich"
        g = None
        if that:
            g = Graph()
            ten = g.ten_trang()
            if ten.strip().lower() != CH["ten_trang_mong_doi"].lower():
                sys.exit(f"DỪNG: token đang trỏ tới trang \"{ten}\", không phải \"{CH['ten_trang_mong_doi']}\".")
        dem = {}
        for r in ds:
            ok, ly_do = can_len_lich(r, ds, bay_gio)
            if that and ly_do == "Lỡ giờ" and r["trang_thai"] != "Lỡ giờ":
                r["trang_thai"] = "Lỡ giờ"
            if not ok:
                dem[ly_do.split(":")[0]] = dem.get(ly_do.split(":")[0], 0) + 1
                continue
            luc = int(datetime.fromisoformat(r["thoi_gian"]).timestamp())
            chu = (GOC / r["file_noi_dung"]).read_text(encoding="utf-8")
            nhan = f"{r['thoi_gian'][:16].replace('T', ' ')} · {r['khung']:<16} · {r['ma']}"
            if not that:
                print(f"[THỬ] sẽ lên lịch  {nhan}")
                dem["Sẽ lên lịch"] = dem.get("Sẽ lên lịch", 0) + 1
                continue
            try:
                if r["loai"] == "bai-moi":
                    pid = g.bai_anh(GOC / r["file_media"], chu, luc)
                elif r["loai"] == "video":
                    tieu_de = chu.splitlines()[0][:100] if r["ma"].startswith("trailer") else \
                        next(t["ten"] for t in json.loads((GOC / "noi-dung-tap.json").read_text(encoding="utf-8")) if t["tap"] == int(r["tap"]))
                    pid = g.video(GOC / r["file_media"], tieu_de, chu, luc)
                else:
                    pid = g.reel(GOC / r["file_media"], chu, luc)
                r.update(trang_thai="Đã lên lịch", post_id=pid, ghi_chu=f"lên lịch lúc {datetime.now():%d/%m %H:%M}")
                print(f"✅ đã lên lịch  {nhan}  → id {pid}")
                dem["Đã lên lịch mới"] = dem.get("Đã lên lịch mới", 0) + 1
            except RuntimeError as e:
                r["ghi_chu"] = f"LỖI: {e}"[:300]
                print(f"❌ lỗi        {nhan}: {e}")
                dem["Lỗi"] = dem.get("Lỗi", 0) + 1
            ghi_lich(ds)  # ghi ngay sau mỗi bài: lỗi giữa chừng cũng không mất trạng thái
        if that:
            ghi_lich(ds)
        print("\nTÓM TẮT: " + " · ".join(f"{v} {k}" for k, v in sorted(dem.items(), key=lambda kv: -kv[1])))
        if not that:
            print("(Chạy thử: chưa gửi gì. Lên lịch thật: python dang-facebook.py --len-lich)")
        return

    if lenh == "--binh-luan":
        g = Graph()
        for r in ds:
            if r["loai"] == "video" and r["trang_thai"] == "Đã lên lịch" and not r["ma"].startswith("trailer") \
                    and datetime.fromisoformat(r["thoi_gian"]) <= bay_gio:
                chu = (GOC / "bai-dang" / f"{r['ma']}-binh-luan.txt").read_text(encoding="utf-8")
                try:
                    cid = g.binh_luan(r["post_id"], chu)
                    r.update(trang_thai="Đã bình luận", ghi_chu=f"bình luận {cid} - NHỚ GHIM TAY")
                    print(f"💬 {r['ma']}: đã bình luận ({cid}). Vào bài viết để GHIM bình luận này.")
                except RuntimeError as e:
                    print(f"❌ {r['ma']}: {e}")
        ghi_lich(ds)
        return

    sys.exit(__doc__)


if __name__ == "__main__":
    main()
