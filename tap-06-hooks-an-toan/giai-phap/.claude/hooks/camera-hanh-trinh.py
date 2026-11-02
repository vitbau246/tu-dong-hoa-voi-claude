"""Hook PostToolUse "camera hành trình": ghi mọi lệnh Claude chạy và mọi file Claude sửa vào một file CSV.

Mở .claude/nhat-ky-claude.csv bằng Excel để xem lại AI đã làm gì, lúc nào.
"""
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

du_lieu = json.load(sys.stdin)
cong_cu = du_lieu.get("tool_name", "")
dau_vao = du_lieu.get("tool_input", {})
chi_tiet = dau_vao.get("command") or dau_vao.get("file_path") or json.dumps(dau_vao, ensure_ascii=False)[:200]

thu_muc = Path(os.environ.get("CLAUDE_PROJECT_DIR", du_lieu.get("cwd", "."))) / ".claude"
file_log = thu_muc / "nhat-ky-claude.csv"
moi = not file_log.exists()
with open(file_log, "a", newline="", encoding="utf-8-sig" if moi else "utf-8") as f:
    w = csv.writer(f)
    if moi:
        w.writerow(["Thời gian", "Công cụ", "Chi tiết", "Phiên"])
    w.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"), cong_cu, chi_tiet, du_lieu.get("session_id", "")[:8]])
