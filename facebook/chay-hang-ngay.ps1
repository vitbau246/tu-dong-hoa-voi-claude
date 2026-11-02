<#
  Chạy tự động lịch Facebook: mỗi 30 phút từ 7:00 đến 23:00
    1) --len-lich : đẩy các bài ĐÃ DUYỆT + có media + trong 28 ngày tới lên Facebook (dạng hẹn giờ)
    2) --binh-luan: đăng bình luận "prompt + file mẫu" dưới video vừa lên sóng
  Đăng ký: powershell -ExecutionPolicy Bypass -File .\chay-hang-ngay.ps1 -DangKy
  Chạy tay: powershell -ExecutionPolicy Bypass -File .\chay-hang-ngay.ps1
  Gỡ:       Unregister-ScheduledTask -TaskName "FoxFlow - Lich dang Facebook" -Confirm:$false
#>
param([switch]$DangKy)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location $PSScriptRoot

if ($DangKy) {
    $hd = New-ScheduledTaskAction -Execute "powershell.exe" -WorkingDirectory $PSScriptRoot `
        -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$PSCommandPath`""
    $kh = New-ScheduledTaskTrigger -Daily -At 7:00am
    $kh.Repetition = (New-ScheduledTaskTrigger -Once -At 7:00am -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration (New-TimeSpan -Hours 16)).Repetition
    $cd = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 25) -MultipleInstances IgnoreNew
    Register-ScheduledTask -TaskName "FoxFlow - Lich dang Facebook" -Action $hd -Trigger $kh -Settings $cd `
        -Description "Đẩy lịch đăng lên Fanpage 5 phút tự động hóa + bình luận ghim" -Force | Out-Null
    "Đã đăng ký: mỗi 30 phút, 7:00–23:00. Lần chạy tới: $((Get-ScheduledTaskInfo -TaskName 'FoxFlow - Lich dang Facebook').NextRunTime)"
    return
}

$log = Join-Path $PSScriptRoot "nhat-ky-dang.txt"
"===== $(Get-Date -Format 'dd/MM/yyyy HH:mm') =====" | Out-File $log -Append -Encoding utf8
python dang-facebook.py --len-lich 2>&1 | Out-File $log -Append -Encoding utf8
python dang-facebook.py --binh-luan 2>&1 | Out-File $log -Append -Encoding utf8
