"""Tập 8 - Tạo danh sách công việc (hạn tính theo NGÀY CHẠY script) cho bản tin sáng tự động.

Chạy:  python chuan-bi.py              -> demo/cong-viec.csv (UTF-8 BOM, mở được bằng Excel)
       python chuan-bi.py --giai-phap  -> chép thêm ban-tin-sang.ps1, dang-ky-lich.ps1 (UTF-8 BOM)
Hạn công việc được tính lệch so với hôm nay, nên quay ngày nào cũng có việc quá hạn / sắp đến hạn.
"""
import csv
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"

# (công việc, lệch so với hôm nay (ngày), trạng thái, người phối hợp)
VIEC = [
    ("Gửi báo cáo chi phí tháng cho Phòng Tài chính", -2, "Đang làm", "P.TC"),
    ("Ký duyệt tờ trình mua 15 màn hình", -1, "Chờ duyệt", "anh Hùng"),
    ("Họp chốt kế hoạch CNTT 2027", 0, "Chưa làm", "BGĐ"),
    ("Cập nhật hợp đồng bảo trì lên phần mềm QLVB", 1, "Đang làm", "IT"),
    ("Nhắc 2 phòng gửi nhu cầu kế hoạch 2027", 2, "Chưa làm", "P.KT, P.KD"),
    ("Chuẩn bị slide đào tạo QLVB đợt 3", 3, "Đang làm", "P.HCNS"),
    ("Rà soát danh sách 40 máy tính cần thay", 6, "Chưa làm", "IT"),
    ("Tổng hợp phản hồi sau đào tạo", 9, "Chưa làm", "P.HCNS"),
    ("Báo cáo quý IV", 30, "Chưa làm", "anh Hùng"),
]


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    hom_nay = date.today()
    with open(DEMO / "cong-viec.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Công việc", "Hạn", "Trạng thái", "Phối hợp"])
        for ten, lech, tt, ph in VIEC:
            w.writerow([ten, (hom_nay + timedelta(days=lech)).strftime("%d/%m/%Y"), tt, ph])

    if "--giai-phap" in sys.argv:
        for ten in ("ban-tin-sang.ps1", "dang-ky-lich.ps1"):
            noi_dung = (GOC / "giai-phap" / ten).read_text(encoding="utf-8-sig")
            (DEMO / ten).write_text(noi_dung, encoding="utf-8-sig")  # PowerShell 5.1 cần BOM
        print("Đã chép ban-tin-sang.ps1, dang-ky-lich.ps1 vào demo/")

    qua_han = sum(1 for v in VIEC if v[1] < 0)
    sap_den = sum(1 for v in VIEC if 0 <= v[1] <= 3)
    print(f"Đã tạo demo/cong-viec.csv: {len(VIEC)} việc, {qua_han} quá hạn, {sap_den} đến hạn trong 3 ngày (tính từ {hom_nay:%d/%m/%Y})")


if __name__ == "__main__":
    main()
