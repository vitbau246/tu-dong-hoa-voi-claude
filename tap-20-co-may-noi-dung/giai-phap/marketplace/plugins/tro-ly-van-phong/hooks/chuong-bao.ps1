param([string]$Loai = "xong")
# Hook "chuông báo": hiện thông báo Windows khi Claude làm xong (Stop) hoặc cần bạn duyệt (Notification).
# File phải lưu dạng UTF-8 có BOM để Windows PowerShell 5.1 hiển thị đúng tiếng Việt.

$null = [Console]::In.ReadToEnd()  # Claude Code gửi JSON qua stdin; ở đây không cần dùng

if ($Loai -eq "can-duyet") {
    $tieuDe = "Claude đang chờ bạn duyệt"
    $noiDung = "Quay lại VS Code để cho phép hoặc từ chối thao tác."
} else {
    $tieuDe = "Claude đã làm xong"
    $noiDung = "Quay lại VS Code để xem kết quả."
}

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml("<toast><visual><binding template='ToastGeneric'><text>$tieuDe</text><text>$noiDung</text></binding></visual><audio src='ms-winsoundevent:Notification.Default'/></toast>")
$appId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show([Windows.UI.Notifications.ToastNotification]::new($xml))
