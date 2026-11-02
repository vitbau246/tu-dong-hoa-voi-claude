"""Dựng plugin "tro-ly-marketing" từ các lời giải ĐÃ KIỂM THỬ của tập 11–18, và gộp vào marketplace cùng plugin tập 10.

Chạy:  python dong-goi.py   -> giai-phap/marketplace/ (2 plugin: tro-ly-van-phong, tro-ly-marketing)
Một nguồn duy nhất: sửa skill/script ở tập gốc rồi chạy lại file này.
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
GP = Path(__file__).resolve().parent
S = GP.parent.parent  # thư mục series
MP = GP / "marketplace"
PL = MP / "plugins" / "tro-ly-marketing"

NGUON_SKILL = {
    "nghien-cuu": S / "tap-11-nghien-cuu-trich-nguon/giai-phap/.claude/skills/nghien-cuu",
    "nghien-cuu-sau": S / "tap-12-doi-nghien-cuu-song-song/giai-phap/.claude/skills/nghien-cuu-sau",
    "brief-seo": S / "tap-15-tu-khoa-seo/giai-phap/.claude/skills/brief-seo",
    "viet-bai-seo": S / "tap-16-viet-bai-chuan-seo/giai-phap/.claude/skills/viet-bai-seo",
    "da-kenh": S / "tap-17-dang-wordpress-da-kenh/giai-phap/.claude/skills/da-kenh",
    "co-may-noi-dung": GP / "tro-ly-marketing/skills/co-may-noi-dung",
    "audit-seo": GP / "tro-ly-marketing/skills/audit-seo",
}
SCRIPT = {  # skill -> script đi kèm (đặt trong <skill>/scripts/)
    "nghien-cuu": S / "tap-11-nghien-cuu-trich-nguon/giai-phap/kiem-chung-trich-dan.py",
    "nghien-cuu-sau": S / "tap-11-nghien-cuu-trich-nguon/giai-phap/kiem-chung-trich-dan.py",
    "viet-bai-seo": S / "tap-16-viet-bai-chuan-seo/giai-phap/cham-diem-seo.py",
    "co-may-noi-dung": S / "tap-17-dang-wordpress-da-kenh/giai-phap/dang-wordpress.py",
    "audit-seo": S / "tap-18-audit-seo-ky-thuat/giai-phap/kiem-tra-ky-thuat.py",
}
AGENTS = [S / "tap-12-doi-nghien-cuu-song-song/giai-phap/.claude/agents/nha-nghien-cuu.md",
          S / "tap-12-doi-nghien-cuu-song-song/giai-phap/.claude/agents/kiem-chung-vien.md"]


def main():
    if MP.exists():
        shutil.rmtree(MP)
    (MP / ".claude-plugin").mkdir(parents=True)
    # Plugin tập 10 giữ nguyên
    shutil.copytree(S / "tap-10-plugin-cho-ca-team/giai-phap/van-phong-marketplace/plugins/tro-ly-van-phong",
                    MP / "plugins" / "tro-ly-van-phong")

    (PL / ".claude-plugin").mkdir(parents=True)
    for ten, nguon in NGUON_SKILL.items():
        dich = PL / "skills" / ten
        shutil.copytree(nguon, dich, ignore=shutil.ignore_patterns("scripts"))
        if ten in SCRIPT:
            (dich / "scripts").mkdir()
            shutil.copy(SCRIPT[ten], dich / "scripts" / SCRIPT[ten].name)
    # Skill viet-bai-seo trong plugin: chấm tay bằng script đi kèm thay vì file ở thư mục dự án
    vb = PL / "skills/viet-bai-seo/SKILL.md"
    vb.write_text(vb.read_text(encoding="utf-8").replace(
        "4. Lưu `bai-viet/<slug>.md`. Hook sẽ tự chấm điểm.",
        "4. Lưu `bai-viet/<slug>.md`. Hook của plugin sẽ tự chấm điểm (chấm tay: `python \"${CLAUDE_SKILL_DIR}/scripts/cham-diem-seo.py\" <file>`)."),
        encoding="utf-8")
    # Trong plugin, skill/agent có tiền tố "tro-ly-marketing:" -> ghi rõ để Claude gọi đúng tên
    for f, cu, moi in [
        ("nghien-cuu-sau", "subagent `nha-nghien-cuu`", "subagent `nha-nghien-cuu` (trong plugin: `tro-ly-marketing:nha-nghien-cuu`)"),
        ("nghien-cuu-sau", "subagent `kiem-chung-vien`", "subagent `kiem-chung-vien` (trong plugin: `tro-ly-marketing:kiem-chung-vien`)"),
        ("co-may-noi-dung", "skill `brief-seo`", "skill `tro-ly-marketing:brief-seo`"),
        ("co-may-noi-dung", "skill `viet-bai-seo`", "skill `tro-ly-marketing:viet-bai-seo`"),
        ("co-may-noi-dung", "skill `da-kenh`", "skill `tro-ly-marketing:da-kenh`"),
    ]:
        p = PL / "skills" / f / "SKILL.md"
        t = p.read_text(encoding="utf-8")
        assert cu in t, f"Không thấy '{cu}' trong {p}"
        p.write_text(t.replace(cu, moi), encoding="utf-8")
    (PL / "agents").mkdir()
    for a in AGENTS:
        shutil.copy(a, PL / "agents" / a.name)
    (PL / "hooks").mkdir()
    (PL / "hooks" / "hooks.json").write_text(json.dumps({
        "description": "Tự chấm điểm SEO mỗi khi Claude ghi file trong bai-viet/*.md; dưới 90 điểm thì trả lỗi để Claude tự sửa.",
        "hooks": {"PostToolUse": [{"matcher": "Write|Edit", "hooks": [{
            "type": "command", "command": "python",
            "args": ["${CLAUDE_PLUGIN_ROOT}/skills/viet-bai-seo/scripts/cham-diem-seo.py", "--hook"],
            "statusMessage": "Đang chấm điểm SEO..."}]}]}}, ensure_ascii=False, indent=2), encoding="utf-8")
    (PL / ".claude-plugin" / "plugin.json").write_text(json.dumps({
        "name": "tro-ly-marketing", "version": "1.0.0",
        "description": "Trợ lý marketing: nghiên cứu có kiểm chứng trích dẫn, đội nghiên cứu song song, brief SEO, viết bài tự chấm điểm, "
                       "đăng bản nháp WordPress, nội dung 4 kênh, audit SEO kỹ thuật và cỗ máy nội dung hằng tuần.",
        "author": {"name": "Phòng Marketing, Công ty CP Demo Việt"}}, ensure_ascii=False, indent=2), encoding="utf-8")

    (MP / ".claude-plugin" / "marketplace.json").write_text(json.dumps({
        "name": "van-phong-demo", "description": "Bộ công cụ tự động hóa của Công ty CP Demo Việt",
        "owner": {"name": "Phòng Kế hoạch - Tổng hợp"},
        "plugins": [
            {"name": "tro-ly-van-phong", "source": "./plugins/tro-ly-van-phong",
             "description": "Báo cáo tuần, trộn thư, kiểm tra hóa đơn, dọn thư mục an toàn, đội phân tích báo giá, phanh an toàn"},
            {"name": "tro-ly-marketing", "source": "./plugins/tro-ly-marketing",
             "description": "Nghiên cứu có kiểm chứng, SEO (brief, viết, chấm điểm, audit), đăng WordPress bản nháp, đa kênh, cỗ máy nội dung"},
        ]}, ensure_ascii=False, indent=2), encoding="utf-8")

    so_skill = len(list((PL / "skills").iterdir()))
    print(f"Đã dựng {MP}: tro-ly-marketing ({so_skill} skills, {len(AGENTS)} agents, 1 hook) + tro-ly-van-phong")


if __name__ == "__main__":
    main()
