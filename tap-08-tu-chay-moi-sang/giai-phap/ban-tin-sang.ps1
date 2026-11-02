<#
  Bản tin sáng tự động bằng Claude Code (chế độ không giao diện: claude -p)
  - Đọc tin từ RSS VnExpress + danh sách việc trong cong-viec.csv
  - Ghi ra ban-tin\YYYY-MM-DD.html, mở file và hiện thông báo Windows
  Chạy tay:  powershell -ExecutionPolicy Bypass -File .\ban-tin-sang.ps1
  Lưu ý: file phải lưu dạng UTF-8 có BOM để Windows PowerShell 5.1 đọc đúng tiếng Việt.
#>
param(
    [string]$Claude = "",           # đường dẫn claude.exe nếu không nằm trong PATH
    [switch]$KhongMoFile            # thêm -KhongMoFile khi chạy theo lịch mà không muốn tự mở trình duyệt
)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8  # đọc đúng tiếng Việt từ claude.exe
Set-Location $PSScriptRoot

# 1. Tìm claude: tham số -> PATH -> vị trí mặc định của bộ cài native
if (-not $Claude) {
    $lenh = Get-Command claude -ErrorAction SilentlyContinue
    $Claude = if ($lenh) { $lenh.Source } else { "$env:USERPROFILE\.local\bin\claude.exe" }
}
if (-not (Test-Path $Claude)) { throw "Không tìm thấy claude. Cài CLI: irm https://claude.ai/install.ps1 | iex" }

$ngay = Get-Date -Format "yyyy-MM-dd"
$homNay = Get-Date -Format "dd/MM/yyyy"
New-Item -ItemType Directory -Force -Path "ban-tin" | Out-Null

$yeuCau = @"
Hôm nay là $homNay. Tạo bản tin sáng dạng HTML, lưu vào ban-tin/$ngay.html:
1. Đọc RSS https://vnexpress.net/rss/kinh-doanh.rss và https://vnexpress.net/rss/khoa-hoc-cong-nghe.rss.
   Chọn 5 tin đáng chú ý nhất cho người làm văn phòng. Mỗi tin: tiêu đề, 2 câu tóm tắt, đường link gốc.
2. Đọc cong-viec.csv: liệt kê việc QUÁ HẠN (tô đỏ) và việc đến hạn trong 3 ngày tới (tô cam), sắp theo hạn.
3. Một dòng 'Việc nên làm đầu tiên hôm nay', kèm lý do ngắn.
Yêu cầu HTML: một file duy nhất, CSS nhúng sẵn, đọc tốt trên điện thoại, tiếng Việt có dấu.
Không bịa tin: chỉ dùng tin có trong RSS. Cuối cùng trả lời đúng 1 dòng: số tin và số việc cần chú ý.
"@

# 2. Gọi Claude ở chế độ không giao diện, chỉ cấp đúng quyền cần thiết
$batDau = Get-Date
$ketQua = & $Claude -p $yeuCau `
    --allowedTools "Read,Write,WebFetch(domain:vnexpress.net)" `
    --max-budget-usd 1 `
    --output-format text 2>&1
$giay = [int]((Get-Date) - $batDau).TotalSeconds
"[$(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')] ($giay giây) $ketQua" | Out-File "ban-tin\nhat-ky.txt" -Append -Encoding utf8

# 3. Mở bản tin + thông báo
$file = Join-Path $PSScriptRoot "ban-tin\$ngay.html"
if (Test-Path $file) {
    $tieuDe = "Bản tin sáng $homNay đã sẵn sàng"
    if (-not $KhongMoFile) { Start-Process $file }
} else {
    $tieuDe = "Bản tin sáng gặp lỗi, xem ban-tin\nhat-ky.txt"
}
$noiDung = ("$ketQua" -replace "[<>&]", " ")
if ($noiDung.Length -gt 120) { $noiDung = $noiDung.Substring(0, 120) }
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml("<toast><visual><binding template='ToastGeneric'><text>$tieuDe</text><text>$noiDung</text></binding></visual></toast>")
$appId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show([Windows.UI.Notifications.ToastNotification]::new($xml))
