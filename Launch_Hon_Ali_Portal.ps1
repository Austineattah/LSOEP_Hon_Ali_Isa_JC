$ErrorActionPreference = "Stop"
$projectDir = "C:\Users\USER\Desktop\LSOEP_Hon_Ali.portal"
$pythonExe = Join-Path $projectDir "env\Scripts\python.exe"
$url = "http://localhost:8501"

Set-Location $projectDir

$serverProcess = Start-Process -FilePath $pythonExe `
    -ArgumentList @("-m", "streamlit", "run", "main.py", "--server.port", "8501") `
    -WorkingDirectory $projectDir `
    -PassThru

try {
    $deadline = (Get-Date).AddSeconds(30)
    $ready = $false

    while ((Get-Date) -lt $deadline) {
        if ($serverProcess.HasExited) {
            break
        }
        try {
            $client = New-Object System.Net.Sockets.TcpClient
            $asyncResult = $client.BeginConnect("127.0.0.1", 8501, $null, $null)
            if ($asyncResult.AsyncWaitHandle.WaitOne(500) -and $client.Connected) {
                $client.EndConnect($asyncResult)
                $client.Close()
                $ready = $true
                break
            }
            $client.Close()
        } catch {
            # Port not open yet; keep polling
        }
        Start-Sleep -Milliseconds 500
    }

    if ($ready) {
        Start-Process $url
    }

    Wait-Process -Id $serverProcess.Id
} finally {
    if ($serverProcess -and -not $serverProcess.HasExited) {
        Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
    }
}
