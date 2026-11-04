"""Chạy Claude Code thật (claude -p) trên demo/ của một tập, lưu kết quả JSON vào du-lieu-that/tap-XX/.

  python chay-that.py ..\\tap-02-gop-excel 1-khao-sat plan prompt1.txt
  python chay-that.py ..\\tap-02-gop-excel 2-gop acceptEdits prompt2.txt --tiep   # nối phiên trước (--resume)

Quyền: plan = chỉ đọc; acceptEdits = sửa file + chạy python/pip (PowerShell trên Windows).
"""
import argparse, json, os, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
GOC = Path(__file__).parent
CLAUDE = os.environ.get("CLAUDE_EXE") or str(next(Path.home().glob(
    ".vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude.exe")))
CONG_CU = ["Read", "Glob", "Grep", "Write", "Edit", "PowerShell(python *)", "PowerShell(pip *)", "PowerShell(py *)"]

ap = argparse.ArgumentParser()
ap.add_argument("tap"); ap.add_argument("ten"); ap.add_argument("che_do", choices=["plan", "acceptEdits"])
ap.add_argument("prompt_file"); ap.add_argument("--tiep", action="store_true")
ap.add_argument("--ngan-sach", default="3")
a = ap.parse_args()

tap = Path(a.tap).resolve()
so = re.match(r"tap-(\d+)", tap.name).group(1)
ra = GOC / "du-lieu-that" / f"tap-{so}"; ra.mkdir(parents=True, exist_ok=True)
prompt = Path(a.prompt_file).read_text(encoding="utf-8").strip()

lenh = [CLAUDE, "-p", prompt, "--output-format", "json", "--permission-mode", a.che_do,
        "--max-budget-usd", a.ngan_sach, "--allowedTools", *CONG_CU]
if a.tiep:
    truoc = sorted(ra.glob("*.json"))[-1]
    lenh += ["--resume", json.loads(truoc.read_text(encoding="utf-8"))["session_id"]]

bd = time.time()
p = subprocess.run(lenh, cwd=tap / "demo", capture_output=True, text=True, encoding="utf-8")
giay = round(time.time() - bd, 1)
try:
    kq = json.loads(p.stdout)
except json.JSONDecodeError:
    sys.exit(f"LỖI (mã {p.returncode}):\n{p.stdout[-2000:]}\n{p.stderr[-2000:]}")
kq["_giay"], kq["_prompt"] = giay, prompt
kq["result"] = kq.get("result", "").replace(os.environ.get("USERNAME", "\0"), "<ban>")
(ra / f"{a.ten}.json").write_text(json.dumps(kq, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"== {a.ten}: {giay}s · ${kq.get('total_cost_usd', 0):.2f} · {kq.get('num_turns')} lượt · {kq.get('subtype')}")
print(kq["result"])
