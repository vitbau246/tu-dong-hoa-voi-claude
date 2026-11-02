"""Chuyển báo cáo Markdown đơn giản (tiêu đề, đoạn, gạch đầu dòng, bảng, **đậm**) sang Word.

Dùng: python md_sang_docx.py duong-dan/bao-cao.md   -> tạo bao-cao.docx cùng thư mục
"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


def them_chu(p, text):
    # Tách **đậm** thành các run riêng
    for i, phan in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if phan:
            p.add_run(phan).bold = i % 2 == 1


def chuyen(md_path: Path) -> Path:
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(13)

    dong = md_path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(dong):
        d = dong[i].rstrip()
        if d.startswith("|"):
            bang = []
            while i < len(dong) and dong[i].strip().startswith("|"):
                o = [c.strip() for c in dong[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in o):
                    bang.append(o)
                i += 1
            t = doc.add_table(rows=len(bang), cols=max(len(r) for r in bang))
            t.style = "Table Grid"
            for r, hang in enumerate(bang):
                for c, gt in enumerate(hang):
                    o = t.cell(r, c).paragraphs[0]
                    them_chu(o, gt)
                    if r == 0:
                        for run in o.runs:
                            run.bold = True
            continue
        if d.startswith("# "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(d[2:])
            r.bold, r.font.size, r.font.color.rgb = True, Pt(16), RGBColor(0x1F, 0x4E, 0x79)
        elif d.startswith("## "):
            p = doc.add_paragraph()
            r = p.add_run(d[3:])
            r.bold, r.font.size = True, Pt(14)
        elif re.match(r"^\s*[-*] ", d):
            them_chu(doc.add_paragraph(style="List Bullet"), re.sub(r"^\s*[-*] ", "", d))
        elif d:
            them_chu(doc.add_paragraph(), d)
        i += 1

    out = md_path.with_suffix(".docx")
    doc.save(out)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        sys.exit("Cách dùng: python md_sang_docx.py <file.md>")
    print(f"Đã tạo: {chuyen(Path(sys.argv[1]))}")
