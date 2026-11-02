"""Tập 7 - Tạo website demo (chạy trên máy) + danh sách đại lý để Claude lái trình duyệt.

Chạy:  python chuan-bi.py              -> demo/web/ (website), demo/dai-ly.xlsx, dap-an.json
       python chuan-bi.py --giai-phap  -> chép thêm .mcp.json (Playwright MCP dùng Microsoft Edge)
Mở web: python -m http.server 8000 -d demo/web   rồi vào http://localhost:8000

Bẫy được gài:
  - Sản phẩm khuyến mãi hiển thị 2 giá (giá gốc gạch ngang + giá bán) -> phải lấy giá bán
  - 1 sản phẩm giá "Liên hệ" -> không được ghi thành 0
  - 1 đại lý có số điện thoại sai (9 chữ số) -> form từ chối, không được tự "sửa" số
"""
import json
import random
import shutil
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
WEB = DEMO / "web"
rng = random.Random(7)

SAN_PHAM = [
    ("Giấy A4 Double A 80gsm (thùng 5 ram)", 385_000), ("Giấy A4 IK Plus 70gsm (ram)", 72_000),
    ("Bút bi Thiên Long TL-027 (hộp 20)", 72_000), ("Bút ký Parker Jotter", 450_000),
    ("Bút dạ quang Stabilo (bộ 6)", 98_000), ("Sổ da A5 có khóa", 135_000),
    ("Kẹp giấy 32mm (hộp 100)", 18_000), ("Bìa còng 7cm Kingjim", 45_000),
    ("Bìa lá A4 (xấp 10)", 25_000), ("Ghim bấm số 10 (hộp)", 8_000),
    ("Máy bấm ghim Eagle 206", 65_000), ("Băng keo trong 5cm (cây 6 cuộn)", 78_000),
    ("Hộp mực HP 107A", 690_000), ("Hộp mực Canon 337", 820_000),
    ("Máy in laser HP 107w", 2_850_000), ("Máy in đa năng Brother DCP-L2540", 5_490_000),
    ("Máy hủy tài liệu Bonsaii 3S16", 2_150_000), ("Máy chiếu Epson EB-X51", 11_900_000),
    ("Bảng trắng 1.2x2.4m", 1_250_000), ("Bút lông bảng Thiên Long (hộp 10)", 85_000),
    ("Ghế xoay văn phòng lưới", 1_390_000), ("Ghế công thái học Ergo Pro", 5_400_000),
    ("Bàn làm việc 1m2 chân sắt", 2_750_000), ("Tủ hồ sơ sắt 4 ngăn", 3_650_000),
    ("Đèn bàn LED chống cận", 420_000), ("Bàn phím cơ không dây", 1_150_000),
    ("Chuột không dây Logitech M331", 320_000), ("Màn hình 24 inch IPS", 3_290_000),
]
KHUYEN_MAI = {2, 8, 13, 20, 26}  # giảm giá 10-20%
LIEN_HE = {17}                   # máy chiếu: giá "Liên hệ"
HET_HANG = {4, 15, 23}
SAP_HET = {7: 2, 21: 3}

CSS = """
body{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f5f6f8;color:#222}
header{background:#0b5394;color:#fff;padding:14px 32px;display:flex;justify-content:space-between;align-items:center}
header a{color:#fff;margin-left:18px;text-decoration:none;font-weight:600}
main{max-width:1100px;margin:24px auto;padding:0 16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.sp{background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 3px #0002}
.sp h3{font-size:15px;margin:0 0 6px}.ma{color:#888;font-size:12px}
.gia{font-size:18px;color:#c00;font-weight:700;margin:8px 0}.goc{color:#999;text-decoration:line-through;font-size:13px;margin-right:6px}
.tt{font-size:13px}.het{color:#999}.con{color:#0a7d2c}.sap{color:#d97706}
.sao{color:#f5a623;font-size:13px}.trang{margin:24px 0;text-align:center}.trang a{margin:0 8px}
form{background:#fff;padding:24px;border-radius:10px;max-width:560px}
label{display:block;margin-top:12px;font-weight:600}input,select,textarea{width:100%;padding:8px;margin-top:4px;box-sizing:border-box}
button{margin-top:18px;background:#0b5394;color:#fff;border:0;padding:10px 22px;border-radius:6px;font-size:15px;cursor:pointer}
.loi{background:#fde2e2;color:#a00;padding:10px;border-radius:6px;margin-top:12px;display:none}
.ok{background:#dcfce7;color:#065f46;padding:14px;border-radius:6px;margin-top:12px;display:none}
.demo{font-size:11px;color:#999;text-align:center;margin:30px}
table{border-collapse:collapse;background:#fff;width:100%}td,th{border:1px solid #ddd;padding:8px;font-size:14px}
"""
HEADER = """<header><b>🖊️ Văn phòng phẩm An Phát (DEMO)</b><nav>
<a href="index.html">Sản phẩm</a><a href="dang-ky-dai-ly.html">Đăng ký đại lý</a><a href="danh-sach-dai-ly.html">Đại lý đã đăng ký</a></nav></header>"""
FOOTER = '<p class="demo">Website hư cấu phục vụ video hướng dẫn, chạy trên máy cá nhân.</p>'


def trang(tieu_de, than):
    return (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{tieu_de}</title>'
            f"<style>{CSS}</style></head><body>{HEADER}<main>{than}</main>{FOOTER}</body></html>")


def vnd(x):
    return f"{x:,}".replace(",", ".") + " đ"


def main():
    lam_moi(DEMO)
    WEB.mkdir(parents=True)

    ds = []
    for i, (ten, gia) in enumerate(SAN_PHAM):
        ma = f"AP-{1001 + i}"
        sao = round(rng.uniform(3.6, 5.0), 1)
        luot = rng.randint(3, 480)
        if i in LIEN_HE:
            gia_ban, gia_goc = None, None
        elif i in KHUYEN_MAI:
            gia_goc, gia_ban = gia, int(round(gia * rng.choice([0.8, 0.85, 0.9]), -3))
        else:
            gia_goc, gia_ban = None, gia
        if i in HET_HANG:
            tt = ("het", "Hết hàng")
        elif i in SAP_HET:
            tt = ("sap", f"Chỉ còn {SAP_HET[i]}")
        else:
            tt = ("con", "Còn hàng")
        ds.append({"ma": ma, "ten": ten, "gia_ban": gia_ban, "gia_goc": gia_goc, "tinh_trang": tt[1], "lop": tt[0],
                   "sao": sao, "luot": luot})

    trang_sp = [ds[0:10], ds[10:20], ds[20:]]
    for so, nhom in enumerate(trang_sp, 1):
        the = []
        for sp in nhom:
            if sp["gia_ban"] is None:
                gia_html = '<div class="gia">Liên hệ</div>'
            elif sp["gia_goc"]:
                gia_html = f'<div class="gia"><span class="goc">{vnd(sp["gia_goc"])}</span>{vnd(sp["gia_ban"])}</div>'
            else:
                gia_html = f'<div class="gia">{vnd(sp["gia_ban"])}</div>'
            the.append(f'<div class="sp" data-ma="{sp["ma"]}"><h3>{sp["ten"]}</h3><div class="ma">Mã: {sp["ma"]}</div>'
                       f'{gia_html}<div class="tt {sp["lop"]}">● {sp["tinh_trang"]}</div>'
                       f'<div class="sao">★ {sp["sao"]} ({sp["luot"]} đánh giá)</div></div>')
        dieu_huong = []
        if so > 1:
            dieu_huong.append(f'<a href="{"index" if so == 2 else f"trang-{so - 1}"}.html">← Trang trước</a>')
        dieu_huong.append(f"Trang {so}/3")
        if so < 3:
            dieu_huong.append(f'<a href="trang-{so + 1}.html">Trang sau →</a>')
        ten_file = "index.html" if so == 1 else f"trang-{so}.html"
        (WEB / ten_file).write_text(trang(f"Sản phẩm - Trang {so}",
                                          f'<h2>Danh mục sản phẩm</h2><div class="grid">{"".join(the)}</div>'
                                          f'<div class="trang">{" · ".join(dieu_huong)}</div>'), encoding="utf-8")

    tinh = ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ", "Bắc Ninh", "Khánh Hòa", "Nghệ An"]
    form = f"""<h2>Đăng ký làm đại lý</h2>
<form id="f" novalidate>
<label for="ten">Tên đại lý *</label><input id="ten" name="ten">
<label for="lienhe">Người liên hệ *</label><input id="lienhe" name="lienhe">
<label for="sdt">Số điện thoại * (10 chữ số, bắt đầu bằng 0)</label><input id="sdt" name="sdt">
<label for="email">Email *</label><input id="email" name="email">
<label for="tinh">Tỉnh/Thành phố *</label><select id="tinh" name="tinh"><option value="">-- Chọn --</option>
{"".join(f"<option>{t}</option>" for t in tinh)}</select>
<label for="doanhso">Doanh số dự kiến/tháng *</label><select id="doanhso" name="doanhso"><option value="">-- Chọn --</option>
<option>Dưới 50 triệu</option><option>50 - 200 triệu</option><option>Trên 200 triệu</option></select>
<label for="ghichu">Ghi chú</label><textarea id="ghichu" name="ghichu" rows="2"></textarea>
<button type="submit">Gửi đăng ký</button>
<div class="loi" id="loi"></div><div class="ok" id="ok"></div>
</form>
<script>
document.getElementById('f').addEventListener('submit', e => {{
  e.preventDefault();
  const v = id => document.getElementById(id).value.trim();
  const loi = [];
  ['ten','lienhe','sdt','email','tinh','doanhso'].forEach(id => {{ if (!v(id)) loi.push('Thiếu: ' + document.querySelector('label[for='+id+']').textContent.replace(' *','').split(' (')[0]); }});
  if (v('sdt') && !/^0\\d{{9}}$/.test(v('sdt'))) loi.push('Số điện thoại không hợp lệ: phải gồm đúng 10 chữ số và bắt đầu bằng 0');
  if (v('email') && !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(v('email'))) loi.push('Email không hợp lệ');
  const boxLoi = document.getElementById('loi'), boxOk = document.getElementById('ok');
  if (loi.length) {{ boxOk.style.display='none'; boxLoi.innerHTML = '❌ ' + loi.join('<br>❌ '); boxLoi.style.display='block'; return; }}
  const ds = JSON.parse(localStorage.getItem('daily') || '[]');
  const ma = 'DL-2026-' + String(1001 + ds.length);
  ds.push({{ma, ten:v('ten'), lienhe:v('lienhe'), sdt:v('sdt'), email:v('email'), tinh:v('tinh'), doanhso:v('doanhso'), luc:new Date().toLocaleString('vi-VN')}});
  localStorage.setItem('daily', JSON.stringify(ds));
  boxLoi.style.display='none';
  boxOk.innerHTML = '✅ Đăng ký thành công! Mã đăng ký: <b id="ma">' + ma + '</b><br>Đại lý: ' + v('ten');
  boxOk.style.display='block';
  document.getElementById('f').reset();
}});
</script>"""
    (WEB / "dang-ky-dai-ly.html").write_text(trang("Đăng ký đại lý", form), encoding="utf-8")
    (WEB / "danh-sach-dai-ly.html").write_text(trang("Đại lý đã đăng ký", """<h2>Đại lý đã đăng ký</h2>
<table id="t"><tr><th>Mã</th><th>Tên đại lý</th><th>Người liên hệ</th><th>SĐT</th><th>Tỉnh</th><th>Doanh số</th><th>Thời gian</th></tr></table>
<script>
JSON.parse(localStorage.getItem('daily') || '[]').forEach(d => {
  document.getElementById('t').insertAdjacentHTML('beforeend',
    `<tr><td>${d.ma}</td><td>${d.ten}</td><td>${d.lienhe}</td><td>${d.sdt}</td><td>${d.tinh}</td><td>${d.doanhso}</td><td>${d.luc}</td></tr>`);
});
</script>"""), encoding="utf-8")

    dai_ly = [
        ("Nhà sách Minh Khai Demo", "Nguyễn Thị Hoa", "0912345678", "hoa.nt@minhkhai.example", "Hà Nội", "50 - 200 triệu"),
        ("VPP Sài Gòn Xanh Demo", "Trần Quốc Bảo", "0987654321", "bao.tq@saigonxanh.example", "TP. Hồ Chí Minh", "Trên 200 triệu"),
        ("Cửa hàng Hồng Phát Demo", "Lê Văn Phát", "0905111222", "phat.lv@hongphat.example", "Đà Nẵng", "Dưới 50 triệu"),
        ("Đại lý Cảng Xanh Demo", "Phạm Thu Hà", "09123 4567", "ha.pt@cangxanh.example", "Hải Phòng", "50 - 200 triệu"),
        ("VPP Tây Đô Demo", "Võ Minh Tâm", "0939888777", "tam.vm@taydo.example", "Cần Thơ", "Dưới 50 triệu"),
    ]
    wb = Workbook()
    ws = wb.active
    ws.title = "Dai-ly"
    ws.append(["Tên đại lý", "Người liên hệ", "Số điện thoại", "Email", "Tỉnh/Thành phố", "Doanh số dự kiến/tháng"])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="0B5394")
    for d in dai_ly:
        ws.append(list(d))
    for col, w in zip("ABCDEF", (28, 20, 15, 30, 18, 22)):
        ws.column_dimensions[col].width = w
    wb.save(DEMO / "dai-ly.xlsx")

    if "--giai-phap" in sys.argv:
        shutil.copy(GOC / "giai-phap" / ".mcp.json", DEMO / ".mcp.json")
        print("Đã chép .mcp.json vào demo/")

    co_gia = [s for s in ds if s["gia_ban"]]
    dap_an = {
        "so_san_pham": len(ds),
        "so_trang": 3,
        "het_hang": [s["ten"] for s in ds if s["lop"] == "het"],
        "sap_het": {s["ten"]: s["tinh_trang"] for s in ds if s["lop"] == "sap"},
        "khuyen_mai": {s["ten"]: {"gia_goc": s["gia_goc"], "gia_ban": s["gia_ban"]} for s in ds if s["gia_goc"]},
        "gia_lien_he": [s["ten"] for s in ds if s["gia_ban"] is None],
        "gia_trung_binh_cac_sp_co_gia": round(sum(s["gia_ban"] for s in co_gia) / len(co_gia)),
        "sp_danh_gia_cao_nhat": max(ds, key=lambda s: (s["sao"], s["luot"]))["ten"],
        "dang_ky_dai_ly": {"thanh_cong": 4, "that_bai": 1,
                           "ly_do_that_bai": "Đại lý Cảng Xanh Demo: SĐT '09123 4567' chỉ có 9 chữ số -> phải báo lại, KHÔNG tự sửa"},
        "san_pham": ds,
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in dap_an.items() if k != "san_pham"}, ensure_ascii=False, indent=2))


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


if __name__ == "__main__":
    main()
