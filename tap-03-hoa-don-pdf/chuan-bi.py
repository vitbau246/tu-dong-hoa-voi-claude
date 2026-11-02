"""Tập 3 - Tạo 30 hóa đơn PDF (hư cấu, 3 kiểu bố cục) để trích xuất vào Excel.

Chạy:  python chuan-bi.py
Kết quả: ./demo/hoa-don/*.pdf và ./dap-an.json

Bẫy được gài:
  - 2 hóa đơn có Tổng thanh toán KHÁC Cộng tiền hàng + Tiền thuế (cộng sai)
  - 1 hóa đơn bị nộp trùng (cùng nhà cung cấp + số hóa đơn, khác tên file)
Toàn bộ công ty, mã số thuế là hư cấu. Mỗi trang có dòng "MẪU DEMO - KHÔNG CÓ GIÁ TRỊ PHÁP LÝ".
"""
import json
import random
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
rng = random.Random(303)

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-B", "C:/Windows/Fonts/arialbd.ttf"))
W, H = A4

NGUOI_MUA = ("Công ty Cổ phần Demo Việt", "9100000001", "Tầng 5, 18 Phố Mẫu, Q. Cầu Giấy, Hà Nội")
NCC = [
    {"ten": "Công ty TNHH Thiết bị Văn phòng Minh An", "mst": "9101234567", "kh": "1C25TMA", "kieu": "A",
     "hang": [("Giấy in A4 Double A (thùng)", "Thùng", 385_000), ("Mực in HP 107A", "Hộp", 690_000),
              ("Bìa còng 7cm", "Cái", 45_000), ("Bút bi Thiên Long (hộp 20)", "Hộp", 72_000)], "thue": 8},
    {"ten": "Công ty CP Giải pháp Số Hưng Thịnh", "mst": "9302345678", "kh": "1C25THT", "kieu": "B",
     "hang": [("Bản quyền phần mềm diệt virus (năm)", "Bộ", 450_000), ("Dịch vụ bảo trì máy tính", "Lần", 1_200_000),
              ("Màn hình 24 inch", "Chiếc", 3_290_000), ("Chuột không dây", "Chiếc", 320_000)], "thue": 10},
    {"ten": "Công ty TNHH TM DV Bảo Long", "mst": "9403456789", "kh": "1C25TBL", "kieu": "C",
     "hang": [("Nước uống đóng bình 19L", "Bình", 65_000), ("Cà phê hạt (kg)", "Kg", 280_000),
              ("Dịch vụ vệ sinh văn phòng", "Tháng", 4_500_000)], "thue": 8},
    {"ten": "Công ty CP Vật tư Kỹ thuật Phương Nam", "mst": "9504567890", "kh": "1C25TPN", "kieu": "A",
     "hang": [("Ổ cắm điện Lioa 6 lỗ", "Cái", 185_000), ("Bóng đèn LED 18W", "Cái", 95_000),
              ("Dây cáp mạng Cat6 (cuộn)", "Cuộn", 1_650_000), ("Switch 8 cổng", "Chiếc", 780_000)], "thue": 10},
]

CHU_SO = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def doc_ba_so(n, day_du):
    tram, chuc, dv = n // 100, n // 10 % 10, n % 10
    s = []
    if day_du or tram:
        s.append(f"{CHU_SO[tram]} trăm")
    if chuc == 0:
        if dv and (day_du or tram):
            s.append("lẻ")
    elif chuc == 1:
        s.append("mười")
    else:
        s.append(f"{CHU_SO[chuc]} mươi")
    if dv:
        if dv == 1 and chuc > 1:
            s.append("mốt")
        elif dv == 5 and chuc > 0:
            s.append("lăm")
        elif dv == 4 and chuc > 1:
            s.append("tư")
        else:
            s.append(CHU_SO[dv])
    return " ".join(s)


def doc_so(n):
    if n == 0:
        return "Không đồng"
    nhom, don_vi = [], ["", "nghìn", "triệu", "tỷ"]
    while n:
        nhom.append(n % 1000)
        n //= 1000
    s = []
    for i in range(len(nhom) - 1, -1, -1):
        if nhom[i]:
            s.append(f"{doc_ba_so(nhom[i], i != len(nhom) - 1)} {don_vi[i]}".strip())
    kq = " ".join(s) + " đồng"
    return kq[0].upper() + kq[1:]


def so(x):
    return f"{x:,}".replace(",", ".")


def dong_demo(c):
    c.setFont("Arial", 7)
    c.setFillColorRGB(0.6, 0.6, 0.6)
    c.drawCentredString(W / 2, 20, "MẪU DEMO - KHÔNG CÓ GIÁ TRỊ PHÁP LÝ - dữ liệu hư cấu phục vụ video hướng dẫn")
    c.setFillColorRGB(0, 0, 0)


def ve_A(c, hd):  # Bố cục bảng cổ điển
    c.setFont("Arial-B", 15)
    c.drawCentredString(W / 2, H - 60, "HÓA ĐƠN GIÁ TRỊ GIA TĂNG")
    c.setFont("Arial", 10)
    c.drawCentredString(W / 2, H - 78, f"Ngày {hd['ngay'].day:02d} tháng {hd['ngay'].month:02d} năm {hd['ngay'].year}")
    c.drawRightString(W - 40, H - 60, f"Ký hiệu: {hd['kh']}")
    c.drawRightString(W - 40, H - 74, f"Số: {hd['so']}")
    y = H - 110
    for nhan, gt in [("Đơn vị bán hàng", hd["ncc"]), ("Mã số thuế", hd["mst"]),
                     ("Đơn vị mua hàng", NGUOI_MUA[0]), ("Mã số thuế", NGUOI_MUA[1]), ("Địa chỉ", NGUOI_MUA[2])]:
        c.drawString(40, y, f"{nhan}: {gt}")
        y -= 16
    y -= 10
    cot = [40, 70, 290, 340, 390, 470]
    c.setFont("Arial-B", 9)
    for x, t in zip(cot, ["STT", "Tên hàng hóa, dịch vụ", "ĐVT", "SL", "Đơn giá", "Thành tiền"]):
        c.drawString(x, y, t)
    c.line(40, y - 4, W - 40, y - 4)
    c.setFont("Arial", 9)
    for i, (ten, dvt, sl, gia) in enumerate(hd["hang"], 1):
        y -= 16
        for x, t in zip(cot, [str(i), ten, dvt, str(sl), so(gia), so(sl * gia)]):
            c.drawString(x, y, t)
    c.line(40, y - 6, W - 40, y - 6)
    y -= 24
    c.setFont("Arial", 10)
    for nhan, gt in [("Cộng tiền hàng:", hd["cong"]), (f"Thuế suất GTGT: {hd['thue']}%   Tiền thuế GTGT:", hd["tien_thue"]),
                     ("Tổng cộng tiền thanh toán:", hd["tong"])]:
        c.drawRightString(440, y, nhan)
        c.drawRightString(W - 40, y, so(gt))
        y -= 16
    c.drawString(40, y - 4, f"Số tiền viết bằng chữ: {doc_so(hd['tong'])}.")


def ve_B(c, hd):  # Bố cục hiện đại, nhãn khác hẳn
    c.setFillColorRGB(0.1, 0.3, 0.6)
    c.rect(0, H - 70, W, 70, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Arial-B", 14)
    c.drawString(40, H - 40, hd["ncc"].upper())
    c.setFont("Arial", 9)
    c.drawString(40, H - 56, f"MST {hd['mst']}  ·  HÓA ĐƠN ĐIỆN TỬ GTGT")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Arial", 10)
    c.drawString(40, H - 100, f"Invoice No. / Số HĐ: {hd['so']}      Mẫu - Ký hiệu: {hd['kh']}")
    c.drawString(40, H - 116, f"Issue date / Ngày lập: {hd['ngay'].strftime('%d/%m/%Y')}")
    c.drawString(40, H - 140, f"Khách hàng: {NGUOI_MUA[0]} (MST {NGUOI_MUA[1]})")
    y = H - 175
    c.setFont("Arial-B", 9)
    for x, t in zip([40, 300, 360, 450], ["Mô tả", "Số lượng", "Giá", "Số tiền"]):
        c.drawString(x, y, t)
    c.setFont("Arial", 9)
    for ten, dvt, sl, gia in hd["hang"]:
        y -= 15
        for x, t in zip([40, 300, 360, 450], [f"{ten} ({dvt})", str(sl), so(gia), so(sl * gia)]):
            c.drawString(x, y, t)
    y -= 30
    c.setFont("Arial", 10)
    for nhan, gt in [("Tổng tiền trước thuế", hd["cong"]), (f"VAT ({hd['thue']}%)", hd["tien_thue"])]:
        c.drawString(330, y, nhan)
        c.drawRightString(W - 40, y, so(gt) + " VND")
        y -= 16
    c.setFont("Arial-B", 11)
    c.drawString(330, y - 4, "TỔNG CỘNG")
    c.drawRightString(W - 40, y - 4, so(hd["tong"]) + " VND")
    c.setFont("Arial", 9)
    c.drawString(40, y - 30, f"Bằng chữ: {doc_so(hd['tong'])}")


def ve_C(c, hd):  # Bố cục dạng danh sách (hay gặp ở hóa đơn dịch vụ)
    c.setFont("Arial-B", 13)
    c.drawString(40, H - 60, hd["ncc"])
    c.setFont("Arial", 9)
    c.drawString(40, H - 74, f"Mã số thuế: {hd['mst']}")
    c.setFont("Arial-B", 12)
    c.drawString(40, H - 110, f"HÓA ĐƠN GTGT  {hd['kh']} - {hd['so']}")
    c.setFont("Arial", 10)
    c.drawString(40, H - 128, f"Lập ngày: {hd['ngay'].strftime('%d-%m-%Y')}")
    c.drawString(40, H - 144, f"Bên mua: {NGUOI_MUA[0]} - MST: {NGUOI_MUA[1]}")
    y = H - 175
    for i, (ten, dvt, sl, gia) in enumerate(hd["hang"], 1):
        c.drawString(50, y, f"{i}. {ten}: {sl} {dvt} x {so(gia)} = {so(sl * gia)} đ")
        y -= 16
    y -= 14
    c.drawString(50, y, f"Tiền hàng: {so(hd['cong'])} đ")
    c.drawString(50, y - 16, f"Thuế GTGT {hd['thue']}%: {so(hd['tien_thue'])} đ")
    c.setFont("Arial-B", 11)
    c.drawString(50, y - 36, f"Phải thanh toán: {so(hd['tong'])} đ")
    c.setFont("Arial", 9)
    c.drawString(50, y - 52, f"({doc_so(hd['tong'])})")


VE = {"A": ve_A, "B": ve_B, "C": ve_C}


def main():
    lam_moi(DEMO)
    (DEMO / "hoa-don").mkdir(parents=True)

    ds = []
    so_hd = {n["kh"]: rng.randint(120, 400) for n in NCC}
    ngay = date(2025, 9, 1)
    for i in range(29):
        n = NCC[i % 4] if i < 24 else rng.choice(NCC)
        so_hd[n["kh"]] += rng.randint(1, 30)
        ngay += timedelta(days=rng.randint(0, 2))
        hang = []
        for ten, dvt, gia in rng.sample(n["hang"], rng.randint(1, len(n["hang"]))):
            hang.append((ten, dvt, rng.randint(1, 3) if gia > 1_000_000 else rng.randint(2, 20), gia))
        cong = sum(sl * gia for _, _, sl, gia in hang)
        tien_thue = round(cong * n["thue"] / 100)
        ds.append({"ncc": n["ten"], "mst": n["mst"], "kh": n["kh"], "so": f"{so_hd[n['kh']]:08d}", "ngay": ngay,
                   "hang": hang, "cong": cong, "thue": n["thue"], "tien_thue": tien_thue, "tong": cong + tien_thue,
                   "kieu": n["kieu"], "van_de": None})

    # Bẫy 1, 2: cộng sai tổng
    ds[7]["tong"] += 100_000
    ds[7]["van_de"] = "Tổng thanh toán lớn hơn Cộng tiền hàng + Thuế 100.000 đ"
    s = list(str(ds[18]["tong"]))
    i = len(s) - 6  # đảo 2 chữ số khác nhau ở hàng chục nghìn / trăm nghìn trở lên
    while s[i] == s[i + 1]:
        i -= 1
    s[i], s[i + 1] = s[i + 1], s[i]
    ds[18]["tong"] = int("".join(s))
    chenh = ds[18]["tong"] - ds[18]["cong"] - ds[18]["tien_thue"]
    huong = "lớn hơn" if chenh > 0 else "nhỏ hơn"
    ds[18]["van_de"] = f"Tổng thanh toán bị đảo chữ số, {huong} Cộng tiền hàng + Thuế {so(abs(chenh))} đ"
    # Bẫy 3: nộp trùng hóa đơn số 11 dưới tên file khác
    trung = dict(ds[11])
    trung["van_de"] = f"Trùng hóa đơn {ds[11]['kh']}-{ds[11]['so']} (đã có ở file khác)"
    ds.append(trung)

    rng.shuffle(ds)
    ket_qua = []
    for i, hd in enumerate(ds, 1):
        ten_file = f"HD_{hd['kh']}_{hd['so']}.pdf" if not (hd["van_de"] or "").startswith("Trùng") else f"scan_{rng.randint(1000, 9999)}.pdf"
        c = canvas.Canvas(str(DEMO / "hoa-don" / ten_file), pagesize=A4)
        c.setTitle(f"Hoa don {hd['kh']} {hd['so']}")
        VE[hd["kieu"]](c, hd)
        dong_demo(c)
        c.save()
        ket_qua.append({"file": ten_file, "ncc": hd["ncc"], "ky_hieu": hd["kh"], "so": hd["so"],
                        "ngay": hd["ngay"].strftime("%d/%m/%Y"), "cong_tien_hang": hd["cong"], "thue_suat": hd["thue"],
                        "tien_thue": hd["tien_thue"], "tong_ghi_tren_hd": hd["tong"], "bo_cuc": hd["kieu"],
                        "van_de": hd["van_de"]})

    hop_le = [k for k in ket_qua if not (k["van_de"] or "").startswith("Trùng")]
    dap_an = {
        "so_file_pdf": len(ket_qua),
        "so_hoa_don_duy_nhat": len(hop_le),
        "tong_cong_tien_hang": sum(k["cong_tien_hang"] for k in hop_le),
        "tong_tien_thue": sum(k["tien_thue"] for k in hop_le),
        "tong_thanh_toan_DUNG": sum(k["cong_tien_hang"] + k["tien_thue"] for k in hop_le),
        "tong_thanh_toan_theo_so_ghi_tren_hd": sum(k["tong_ghi_tren_hd"] for k in hop_le),
        "tong_neu_nhap_ca_ban_trung": sum(k["tong_ghi_tren_hd"] for k in ket_qua),
        "can_kiem_tra": [{"file": k["file"], "so": f"{k['ky_hieu']}-{k['so']}", "van_de": k["van_de"]}
                         for k in ket_qua if k["van_de"]],
        "theo_nha_cung_cap": {n["ten"]: sum(k["cong_tien_hang"] + k["tien_thue"] for k in hop_le if k["ncc"] == n["ten"])
                              for n in NCC},
        "chi_tiet": ket_qua,
    }
    (GOC / "dap-an.json").write_text(json.dumps(dap_an, ensure_ascii=False, indent=2), encoding="utf-8")
    tom_tat = {k: v for k, v in dap_an.items() if k != "chi_tiet"}
    print(json.dumps(tom_tat, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
