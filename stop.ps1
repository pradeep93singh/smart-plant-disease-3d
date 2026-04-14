$ErrorActionPreference = "SilentlyContinue"

$ports = @(8010, 8502)

foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -State Listen
    foreach ($conn in $connections) {
        if ($conn.OwningProcess -and $conn.OwningProcess -ne 0) {
            Stop-Process -Id $conn.OwningProcess -Force
            Write-Host "Stopped process $($conn.OwningProcess) on port $port"
        }
    }
}

Write-Host "Stop attempt complete."
