<#
  Điền đường dẫn vào hộp thoại "Tải lên một tập tin" (do trình duyệt Camoufox/Firefox mở ra) rồi bấm Mở.
  Dùng: powershell -ExecutionPolicy Bypass -File .\chon-file.ps1 -DuongDan "E:\...\video.mp4" [-ChoGiay 30] [-TienTrinh camoufox]
  Tìm hộp thoại bằng Win32 EnumWindows (UI Automation duyệt từ gốc không thấy hộp thoại của Camoufox), rồi điều khiển bằng UI Automation.
  Lưu UTF-8 có BOM (PowerShell 5.1).
#>
param([Parameter(Mandatory)][string]$DuongDan, [int]$ChoGiay = 30, [string]$TienTrinh = "camoufox")
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public class HopThoai { public delegate bool CB(IntPtr h, IntPtr l);
 [DllImport("user32.dll")] static extern bool EnumWindows(CB cb, IntPtr l);
 [DllImport("user32.dll")] static extern int GetClassName(IntPtr h, StringBuilder s, int n);
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint p);
 [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, string l);
 [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
 public static IntPtr Tim(int[] pids) { IntPtr kq = IntPtr.Zero;
  EnumWindows((h, l) => { if (!IsWindowVisible(h)) return true; uint p; GetWindowThreadProcessId(h, out p);
   var c = new StringBuilder(64); GetClassName(h, c, 64);
   if (c.ToString() == "#32770" && Array.IndexOf(pids, (int)p) >= 0) { kq = h; return false; } return true; }, IntPtr.Zero);
  return kq; } }
"@
if (-not (Test-Path $DuongDan)) { Write-Output "LOI: khong thay file $DuongDan"; exit 1 }
$han = (Get-Date).AddSeconds($ChoGiay)
$h = [IntPtr]::Zero
while ((Get-Date) -lt $han -and $h -eq [IntPtr]::Zero) {
    $pids = [int[]]@(Get-Process $TienTrinh -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
    if ($pids.Count) { $h = [HopThoai]::Tim($pids) }
    if ($h -eq [IntPtr]::Zero) { Start-Sleep -Milliseconds 400 }
}
if ($h -eq [IntPtr]::Zero) { Write-Output "LOI: khong thay hop thoai chon file sau $ChoGiay giay"; exit 2 }
[HopThoai]::SetForegroundWindow($h) | Out-Null
$hop = [System.Windows.Automation.AutomationElement]::FromHandle($h)
Write-Output ("Thay hop thoai: " + $hop.Current.Name)
# Camoufox phơi các ô dưới dạng Pane nên tìm theo AutomationId + ClassName, rồi điều khiển bằng thông điệp Win32
$AE = [System.Windows.Automation.AutomationElement]
function TimO($id, $lop) {
    $dk = New-Object System.Windows.Automation.AndCondition(
        (New-Object System.Windows.Automation.PropertyCondition($AE::AutomationIdProperty, $id)),
        (New-Object System.Windows.Automation.PropertyCondition($AE::ClassNameProperty, $lop)))
    $hop.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $dk)
}
$o = TimO "1148" "Edit"
if (-not $o) { Write-Output "LOI: khong thay o ten file"; exit 3 }
[HopThoai]::SendMessage([IntPtr]$o.Current.NativeWindowHandle, 0x000C, [IntPtr]::Zero, $DuongDan) | Out-Null   # WM_SETTEXT
Start-Sleep -Milliseconds 400
$nut = TimO "1" "Button"
if (-not $nut) { Write-Output "LOI: khong thay nut Mo/Open"; exit 4 }
[HopThoai]::SendMessage([IntPtr]$nut.Current.NativeWindowHandle, 0x00F5, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null  # BM_CLICK
Start-Sleep -Milliseconds 800
$con = [HopThoai]::Tim($pids)
if ($con -eq $h) { Write-Output "LOI: hop thoai van con mo (duong dan sai?)"; exit 5 }
Write-Output "OK: da chon $DuongDan"
