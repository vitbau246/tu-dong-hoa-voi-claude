"""Hook PreToolUse "phanh an toàn": cấm sửa, xóa, di chuyển bất cứ thứ gì trong thư mục được bảo vệ.

Claude Code gửi JSON mô tả thao tác sắp làm qua stdin.
Thoát mã 2 = CHẶN thao tác. Nội dung in ra stderr được gửi lại cho Claude để nó biết lý do và đổi cách làm.
"""
import json
import re
import sys

sys.stderr.reconfigure(encoding="utf-8")

VUNG_CAM = ["du-lieu-goc"]  # thêm thư mục khác vào đây nếu cần
LENH_THAY_DOI = re.compile(
    r"\b(rm|del|erase|rmdir|rd|mv|move|ren|rename|Remove-Item|Move-Item|Rename-Item|"
    r"Set-Content|Add-Content|Clear-Content|Out-File|New-Item|Copy-Item)\b|>",
    re.IGNORECASE,
)


def chan(ly_do):
    print(f"⛔ BỊ CHẶN bởi hook phanh-an-toan: {ly_do} "
          "Thư mục du-lieu-goc chỉ được ĐỌC. Hãy sao chép file sang lam-viec/ rồi xử lý ở đó.", file=sys.stderr)
    sys.exit(2)


def main():
    du_lieu = json.load(sys.stdin)
    cong_cu = du_lieu.get("tool_name", "")
    dau_vao = du_lieu.get("tool_input", {})

    if cong_cu in ("Edit", "Write", "NotebookEdit"):
        duong_dan = dau_vao.get("file_path", "").replace("\\", "/").lower()
        if any(f"/{v}/" in f"/{duong_dan}" for v in VUNG_CAM):
            chan(f"{cong_cu} định ghi vào {dau_vao.get('file_path')}.")

    elif cong_cu in ("Bash", "PowerShell"):
        lenh = dau_vao.get("command", "")
        if any(v in lenh.lower() for v in VUNG_CAM) and LENH_THAY_DOI.search(lenh):
            chan(f"lệnh có thể thay đổi dữ liệu gốc: `{lenh[:120]}`.")

    sys.exit(0)  # không có ý kiến -> quy trình xin phép bình thường tiếp tục


if __name__ == "__main__":
    main()
