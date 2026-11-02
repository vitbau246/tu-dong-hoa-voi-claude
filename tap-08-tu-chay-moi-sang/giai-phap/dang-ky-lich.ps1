<#
  Đăng ký Windows Task Scheduler: chạy ban-tin-sang.ps1 lúc 7:30 sáng, Thứ 2 đến Thứ 6.
  - Nếu 7:30 máy đang tắt: chạy bù ngay khi bạn bật máy (StartWhenAvailable)
  - Không cần quyền Administrator
  Chạy:     powershell -ExecutionPolicy Bypass -File .\dang-ky-lich.ps1
  Thử ngay: Start-ScheduledTask -TaskName "Claude - Ban tin sang"
  Gỡ bỏ:    Unregister-ScheduledTask -TaskName "Claude - Ban tin sang" -Confirm:$false
#>
param([string]$Gio = "7:30am")

$tenTask = "Claude - Ban tin sang"
$script = Join-Path $PSScriptRoot "ban-tin-sang.ps1"

$hanhDong = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$script`"" `
    -WorkingDirectory $PSScriptRoot
$kichHoat = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday -At $Gio
$caiDat = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 15) `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $tenTask -Action $hanhDong -Trigger $kichHoat -Settings $caiDat `
    -Description "Bản tin sáng do Claude Code tạo (tập 8 - Tự động hóa với Claude)" -Force | Out-Null

$t = Get-ScheduledTask -TaskName $tenTask
"Đã đăng ký '$tenTask' - trạng thái: $($t.State) - lần chạy tới: $((Get-ScheduledTaskInfo -TaskName $tenTask).NextRunTime)"
