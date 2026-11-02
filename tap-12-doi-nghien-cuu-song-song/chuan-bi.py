"""Tập 12 - Đề bài chiến lược cho đội nghiên cứu song song.

Chạy:  python chuan-bi.py              -> demo/de-bai-chien-luoc.md + demo/kiem-chung-trich-dan.py (từ tập 11)
       python chuan-bi.py --giai-phap  -> chép thêm .claude/agents/ (2 agent) và .claude/skills/nghien-cuu-sau/
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).resolve().parent
DEMO = GOC / "demo"
KIEM_CHUNG = GOC.parent / "tap-11-nghien-cuu-trich-nguon" / "giai-phap" / "kiem-chung-trich-dan.py"

DE_BAI = """# Đề bài: Có nên mở kênh bán hàng trên TikTok Shop năm 2026?

**Bối cảnh:** Công ty CP Demo Việt bán văn phòng phẩm và thiết bị văn phòng, doanh thu 2025 khoảng 10,6 tỷ đồng
(xem tập 2), hiện chỉ bán trực tiếp cho doanh nghiệp (B2B) và qua website riêng.

**Câu hỏi cho Ban Giám đốc:** Có nên mở gian hàng trên TikTok Shop (và/hoặc Shopee) trong năm 2026 không?
Nếu có, kỳ vọng thực tế và rủi ro là gì?

**Các góc cần làm rõ (gợi ý)**
- Thị trường: quy mô, tăng trưởng TMĐT và thị phần các sàn tại Việt Nam
- Đối thủ: ngành hàng văn phòng phẩm trên sàn (thương hiệu nào, mức giá, khuyến mãi)
- Khách hàng: ai mua văn phòng phẩm online, B2C hay B2B, hành vi mua qua livestream/video ngắn
- Chính sách & chi phí: phí sàn, phí thanh toán, quy định thuế với người bán trên sàn

**Yêu cầu:** mọi con số có trích dẫn nguyên văn và được kiểm chứng; ghi rõ năm của số liệu; nêu điểm vênh giữa các nguồn.
"""


def lam_moi(thu_muc):
    """Xóa NỘI DUNG bên trong nhưng giữ thư mục (tránh lỗi khi VS Code/terminal đang mở thư mục này)."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    for p in thu_muc.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def main():
    lam_moi(DEMO)
    (DEMO / "de-bai-chien-luoc.md").write_text(DE_BAI, encoding="utf-8")
    shutil.copy(KIEM_CHUNG, DEMO / "kiem-chung-trich-dan.py")
    if "--giai-phap" in sys.argv:
        shutil.copytree(GOC / "giai-phap" / ".claude", DEMO / ".claude")
        scripts = DEMO / ".claude" / "skills" / "nghien-cuu-sau" / "scripts"
        scripts.mkdir(parents=True, exist_ok=True)
        shutil.copy(KIEM_CHUNG, scripts / "kiem-chung-trich-dan.py")
        print("Đã chép 2 agent + skill nghien-cuu-sau (kèm script kiểm chứng) vào demo/.claude/")
    print("Đã tạo demo/de-bai-chien-luoc.md và demo/kiem-chung-trich-dan.py")


if __name__ == "__main__":
    main()
