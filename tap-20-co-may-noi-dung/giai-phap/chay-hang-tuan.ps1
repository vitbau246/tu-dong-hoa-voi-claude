<#
  Cỗ máy nội dung hằng tuần: gọi skill /tro-ly-marketing:co-may-noi-dung bằng claude -p, rồi báo "chờ duyệt".
  Chạy tay:   powershell -ExecutionPolicy Bypass -File .\chay-hang-tuan.ps1
  Hẹn giờ:    powershell -ExecutionPolicy Bypass -File .\chay-hang-tuan.ps1 -DangKy      (Thứ 2, 7:00 hằng tuần)
  Gỡ hẹn giờ: Unregister-ScheduledTask -TaskName "Claude - Co may noi dung" -Confirm:$false
  Lưu ý: chạy từ PowerShell (KHÔNG chạy từ Git Bash, vì Git Bash đổi "/tro-ly-marketing:..." thành đường dẫn).
#>
param([switch]$DangKy, [string]$Claude = "", [double]$NganSach = 3)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location $PSScriptRoot

if ($DangKy) {
    $hd = New-ScheduledTaskAction -Execute "powershell.exe" -WorkingDirectory $PSScriptRoot `
        -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$PSCommandPath`""
    $kh = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 7:00am
    $cd = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 45)
    Register-ScheduledTask -TaskName "Claude - Co may noi dung" -Action $hd -Trigger $kh -Settings $cd `
        -Description "Cỗ máy nội dung hằng tuần (tập 20 - Tự động hóa với Claude)" -Force | Out-Null
    "Đã hẹn: Thứ 2 lúc 7:00. Lần chạy tới: $((Get-ScheduledTaskInfo -TaskName 'Claude - Co may noi dung').NextRunTime)"
    return
}

if (-not $Claude) {
    $c = Get-Command claude -ErrorAction SilentlyContinue
    $Claude = if ($c) { $c.Source } else { "$env:USERPROFILE\.local\bin\claude.exe" }
}
New-Item -ItemType Directory -Force cho-duyet | Out-Null
$batDau = Get-Date
# Quyền tối thiểu: đọc/ghi file dự án, tìm và đọc web, chạy các script python của plugin. Không có quyền xuất bản.
$kq = & $Claude -p "/tro-ly-marketing:co-may-noi-dung" `
    --permission-mode acceptEdits `
    --allowedTools "Read,Write,Edit,Glob,WebSearch,WebFetch,Skill,Task,Bash(python *),PowerShell(python *)" `
    --max-budget-usd $NganSach --output-format text 2>&1
$phut = [math]::Round(((Get-Date) - $batDau).TotalMinutes, 1)
"[$(Get-Date -Format 'dd/MM/yyyy HH:mm')] ($phut phút) $kq" | Out-File cho-duyet\nhat-ky-chay.txt -Append -Encoding utf8

$phieu = Get-ChildItem cho-duyet -Filter *.md | Sort-Object LastWriteTime | Select-Object -Last 1
$tieuDe = if ($phieu -and $phieu.LastWriteTime -gt $batDau) { "Bài tuần này đang CHỜ BẠN DUYỆT" } else { "Cỗ máy nội dung gặp lỗi: xem cho-duyet\nhat-ky-chay.txt" }
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$x = New-Object Windows.Data.Xml.Dom.XmlDocument
$x.LoadXml("<toast><visual><binding template='ToastGeneric'><text>$tieuDe</text><text>Mất $phut phút</text></binding></visual></toast>")
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe').Show([Windows.UI.Notifications.ToastNotification]::new($x))
if ($phieu -and $phieu.LastWriteTime -gt $batDau) { Start-Process $phieu.FullName }
