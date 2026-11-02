"""Chấm điểm SEO on-page cho bài viết Markdown (có YAML frontmatter). Thang 100 điểm, 17 tiêu chí.

Dùng tay:   python cham-diem-seo.py bai-viet/ten-bai.md [--nguong 90]
Dùng làm hook PostToolUse (Claude tự sửa tới khi đạt):
            python cham-diem-seo.py --hook      (đọc JSON từ stdin, chỉ chấm file trong bai-viet/*.md)
            -> điểm < ngưỡng: in lỗi ra stderr + thoát mã 2 => Claude Code đưa lỗi cho Claude để sửa

Định dạng bài:
---
title: "Tiêu đề SEO (30-60 ký tự)"
meta_description: "Mô tả 140-160 ký tự"
slug: duong-dan-khong-dau
focus_keyword: từ khóa chính
min_words: 1200            # tùy chọn, mặc định 1200
faq:
  - q: Câu hỏi?
    a: Trả lời.
---
# H1 ...
"""
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
NGUONG_MAC_DINH = 90


def khong_dau(s):
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def tach(md):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", md, re.S)
    if not m:
        return {}, md
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def cham(path):
    fm, body = tach(Path(path).read_text(encoding="utf-8"))
    kw = str(fm.get("focus_keyword", "")).lower().strip()
    title = str(fm.get("title", ""))
    meta = str(fm.get("meta_description", ""))
    slug = str(fm.get("slug", ""))
    faq = fm.get("faq") or []
    min_words = int(fm.get("min_words", 1200))

    dong = body.splitlines()
    h = [(len(m.group(1)), m.group(2).strip()) for d in dong if (m := re.match(r"^(#{1,6})\s+(.*)", d))]
    van_ban = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)            # bỏ ảnh
    van_ban = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", van_ban)       # link -> chữ
    van_ban = re.sub(r"^\|?\s*:?-{2,}.*$", " ", van_ban, flags=re.M)  # bỏ dòng kẻ |---| của bảng
    van_ban = re.sub(r"<!--.*?-->", " ", van_ban, flags=re.S)                    # bỏ ghi chú ẩn
    van_ban = re.sub(r"^#{1,6}\s+.*$|[*_`>|]", " ", van_ban, flags=re.M)        # bỏ tiêu đề, giữ chữ trong bảng
    tu = re.findall(r"\w+", van_ban)
    so_tu = len(tu)
    dau_100 = " ".join(tu[:100]).lower()
    so_lan_kw = van_ban.lower().count(kw) if kw else 0
    mat_do = so_lan_kw * max(1, len(kw.split())) / max(so_tu, 1) * 100
    link_noi = re.findall(r"\[[^\]]+\]\((/[^)]*|https?://vpp-anphat\.example[^)]*)\)", body)
    anh = re.findall(r"!\[([^\]]*)\]\([^)]*\)", body)
    cau = [c for c in re.split(r"[.!?…]\s+", van_ban) if len(c.split()) > 3]
    tb_cau = sum(len(c.split()) for c in cau) / max(len(cau), 1)
    doan = [p for p in re.split(r"\n\s*\n", body) if p.strip() and not p.lstrip().startswith(("#", "|", "-", "!", "*"))]
    doan_dai = [p for p in doan if len(p.split()) > 120]
    nhay_cap = [f"H{a}→H{b}" for (a, _), (b, _) in zip(h, h[1:]) if b > a + 1]
    h1 = [t for lv, t in h if lv == 1]
    h2 = [t for lv, t in h if lv == 2]

    tieu_chi = [  # (điểm, đạt?, mô tả, gợi ý sửa)
        (10, 30 <= len(title) <= 60, f"Tiêu đề SEO 30–60 ký tự (hiện {len(title)})", "Rút gọn/viết lại title"),
        (10, bool(kw) and kw in title.lower(), "Từ khóa chính có trong tiêu đề SEO", "Đưa từ khóa chính vào title, càng gần đầu càng tốt"),
        (8, 140 <= len(meta) <= 160, f"Mô tả 140–160 ký tự (hiện {len(meta)})", "Viết lại meta_description"),
        (5, bool(kw) and kw in meta.lower(), "Từ khóa chính có trong mô tả", "Thêm từ khóa vào meta_description"),
        (5, bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug)) and len(slug) <= 75 and khong_dau(kw).replace(" ", "-") in slug,
         "Slug không dấu, gạch nối, ≤ 75 ký tự, chứa từ khóa", "Sửa slug theo dạng tu-khoa-chinh-..."),
        (5, len(h1) == 1, f"Đúng 1 thẻ H1 (hiện {len(h1)})", "Chỉ giữ một dòng '# ...'"),
        (5, bool(h1) and kw in h1[0].lower(), "Từ khóa chính có trong H1", "Thêm từ khóa vào H1"),
        (8, bool(kw) and kw in dau_100, "Từ khóa xuất hiện trong 100 từ đầu", "Nhắc từ khóa chính ngay đoạn mở bài"),
        (5, not nhay_cap, "Cấp tiêu đề không nhảy cóc" + (f" (lỗi: {', '.join(nhay_cap)})" if nhay_cap else ""), "Không đi từ H2 thẳng xuống H4"),
        (4, len(h2) >= 4, f"Ít nhất 4 mục H2 (hiện {len(h2)})", "Chia nội dung thành ≥ 4 mục H2"),
        (8, so_tu >= min_words, f"Độ dài ≥ {min_words} từ (hiện {so_tu})", "Viết sâu hơn theo dàn ý brief, không độn chữ"),
        (5, 0.5 <= mat_do <= 2.5, f"Mật độ từ khóa 0,5–2,5% (hiện {mat_do:.1f}%)", "Dùng từ khóa tự nhiên, thay bằng biến thể nếu quá dày"),
        (6, len(link_noi) >= 3, f"Ít nhất 3 liên kết nội bộ (hiện {len(link_noi)})", "Liên kết tới trang sản phẩm/danh mục liên quan"),
        (5, bool(anh) and all(a.strip() for a in anh), f"Mọi ảnh có alt mô tả ({len(anh)} ảnh)", "Thêm ảnh minh họa có alt mô tả nội dung ảnh"),
        (5, len(faq) >= 3, f"Ít nhất 3 câu FAQ trong frontmatter (hiện {len(faq)})", "Thêm faq: - q/a vào frontmatter"),
        (3, tb_cau <= 25, f"Câu trung bình ≤ 25 từ (hiện {tb_cau:.0f})", "Tách câu dài"),
        (3, not doan_dai, f"Đoạn văn ≤ 120 từ ({len(doan_dai)} đoạn quá dài)", "Chia nhỏ đoạn dài"),
    ]
    diem = sum(d for d, ok, _, _ in tieu_chi if ok)
    return diem, tieu_chi


def in_ket_qua(path, diem, tieu_chi, out):
    print(f"ĐIỂM SEO: {diem}/100  ({path})", file=out)
    for d, ok, mo_ta, goi_y in tieu_chi:
        if not ok:
            print(f"  ✗ -{d:>2}  {mo_ta}  →  {goi_y}", file=out)


def ghi_lich_su(du_lieu, path, diem):
    """Ghi mỗi lần chấm vào .claude/nhat-ky-cham-diem.csv: chứng minh hook có chạy + xem điểm tăng dần."""
    thu_muc = Path(du_lieu.get("cwd", ".")) / ".claude"
    thu_muc.mkdir(exist_ok=True)
    f = thu_muc / "nhat-ky-cham-diem.csv"
    moi = not f.exists()
    with open(f, "a", encoding="utf-8-sig" if moi else "utf-8") as out:
        if moi:
            out.write("thoi_gian,bai_viet,diem\n")
        out.write(f"{datetime.now():%d/%m/%Y %H:%M:%S},{Path(path).name},{diem}\n")


def main():
    nguong = int(sys.argv[sys.argv.index("--nguong") + 1]) if "--nguong" in sys.argv else NGUONG_MAC_DINH
    if "--hook" in sys.argv:
        du_lieu = json.load(sys.stdin)
        path = du_lieu.get("tool_input", {}).get("file_path", "")
        if not re.search(r"[\\/]bai-viet[\\/][^\\/]+\.md$", path) or not Path(path).exists():
            sys.exit(0)  # không phải bài viết -> bỏ qua
        diem, tc = cham(path)
        ghi_lich_su(du_lieu, path, diem)
        if diem < nguong:
            in_ket_qua(path, diem, tc, sys.stderr)
            print(f"Chưa đạt ngưỡng {nguong}. Hãy sửa các mục ✗ ở trên (không độn chữ, không nhồi từ khóa).", file=sys.stderr)
            sys.exit(2)
        # Thoát mã 0 thì stdout thường KHÔNG tới được Claude -> báo kết quả qua additionalContext
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                 "additionalContext": f"ĐIỂM SEO: {diem}/100 - đạt ngưỡng {nguong} ({Path(path).name})."}},
                         ensure_ascii=False))
        sys.exit(0)

    for path in [a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()]:
        diem, tc = cham(path)
        in_ket_qua(path, diem, tc, sys.stdout)
        for d, ok, mo_ta, _ in tc:
            if ok:
                print(f"  ✓ +{d:>2}  {mo_ta}")


if __name__ == "__main__":
    main()
