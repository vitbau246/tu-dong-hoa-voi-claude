<#
  Hẹn giờ theo dõi đối thủ: 8:00 và 14:00 mỗi ngày. Có thay đổi thì hiện thông báo Windows + mở báo cáo.
  Chạy:  powershell -ExecutionPolicy Bypass -File .\dang-ky-theo-doi.ps1 -Url "https://website-doi-thu.vn/danh-muc"
  Gỡ:    Unregister-ScheduledTask -TaskName "Claude - Theo doi doi thu" -Confirm:$false
#>
param([Parameter(Mandatory)][string]$Url, [switch]$ChayNgay)

$thuMuc = $PSScriptRoot
$chay = Join-Path $thuMuc "chay-theo-doi.ps1"

# Script chạy mỗi lần: gọi theo-doi.py, nếu có báo cáo mới thì thông báo
@"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location '$thuMuc'
`$truoc = @(Get-ChildItem bao-cao-doi-thu -Filter *.md -ErrorAction SilentlyContinue).Count
`$kq = python theo-doi.py '$Url' 2>&1
"[`$(Get-Date -Format 'dd/MM/yyyy HH:mm')] `$kq" | Out-File nhat-ky-theo-doi.txt -Append -Encoding utf8
`$moi = Get-ChildItem bao-cao-doi-thu -Filter *.md -ErrorAction SilentlyContinue | Sort-Object LastWriteTime | Select-Object -Last 1
if (@(Get-ChildItem bao-cao-doi-thu -Filter *.md -ErrorAction SilentlyContinue).Count -gt `$truoc) {
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
    `$x = New-Object Windows.Data.Xml.Dom.XmlDocument
    `$x.LoadXml("<toast><visual><binding template='ToastGeneric'><text>Đối thủ vừa thay đổi</text><text>Mở báo cáo mới nhất</text></binding></visual></toast>")
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe').Show([Windows.UI.Notifications.ToastNotification]::new(`$x))
    Start-Process `$moi.FullName
}
"@ | Out-File $chay -Encoding utf8   # Out-File utf8 của PowerShell 5.1 = UTF-8 có BOM

$hanhDong = New-ScheduledTaskAction -Execute "powershell.exe" -WorkingDirectory $thuMuc `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$chay`""
$kichHoat = @((New-ScheduledTaskTrigger -Daily -At 8:00am), (New-ScheduledTaskTrigger -Daily -At 2:00pm))
$caiDat = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 15)
Register-ScheduledTask -TaskName "Claude - Theo doi doi thu" -Action $hanhDong -Trigger $kichHoat -Settings $caiDat `
    -Description "Theo dõi website đối thủ (tập 14 - Tự động hóa với Claude)" -Force | Out-Null
"Đã đăng ký: 8:00 và 14:00 hằng ngày. Lần chạy tới: $((Get-ScheduledTaskInfo -TaskName 'Claude - Theo doi doi thu').NextRunTime)"
if ($ChayNgay) { Start-ScheduledTask -TaskName "Claude - Theo doi doi thu"; "Đang chạy thử ngay..." }
