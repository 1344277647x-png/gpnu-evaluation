# GPnu Course Evaluation - Startup Script
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   GPnu Course Evaluation System" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$root = $PSScriptRoot
if (-not $root) { $root = "D:\gpnu教师评价web" }

Write-Host "[1/3] Checking MySQL..." -ForegroundColor Yellow
$mysql = Get-Service -Name "MySQL96" -ErrorAction SilentlyContinue
if ($mysql -and $mysql.Status -ne "Running") {
    Start-Service "MySQL96"
    Write-Host "       MySQL started" -ForegroundColor Green
} else {
    Write-Host "       MySQL already running" -ForegroundColor Green
}

Start-Sleep -Seconds 2

Write-Host "[2/3] Starting backend..." -ForegroundColor Yellow
$py = Join-Path $root "venv\Scripts\pythonw.exe"
$srv = Join-Path $root "backend\server.py"
Get-Process "pythonw" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Process -WindowStyle Minimized -FilePath $py -ArgumentList $srv
Start-Sleep -Seconds 2
Write-Host "       Backend started" -ForegroundColor Green

Write-Host "[3/3] Detecting network..." -ForegroundColor Yellow
$allIPs = ipconfig | Select-String "IPv4" | ForEach-Object { ($_ -split ": ")[-1].Trim() }

# Prefer 192.168.1.x or 192.168.0.x (most common LAN)
$ip = ($allIPs | Where-Object { $_ -match "^192\.168\.[01]\." } | Select-Object -First 1)
if (-not $ip) { $ip = ($allIPs | Where-Object { $_ -match "^192\.168\." } | Select-Object -First 1) }
if (-not $ip) { $ip = ($allIPs | Where-Object { $_ -notmatch "^127\." } | Select-Object -First 1) }
if (-not $ip) { $ip = "your-IP" }

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  System is READY!" -ForegroundColor Green
Write-Host ""
Write-Host "  Local:  http://localhost:5000" -ForegroundColor White
Write-Host "  Share:  http://${ip}:5000" -ForegroundColor Yellow
Write-Host ""
if ($allIPs.Count -gt 1) {
    Write-Host "  Other detected IPs:" -ForegroundColor DarkGray
    $allIPs | Where-Object { $_ -ne $ip } | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
    Write-Host ""
}
Write-Host "  Admin:  admin / Admin123456" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to close"