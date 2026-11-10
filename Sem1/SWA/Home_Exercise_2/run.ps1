param(
    [ValidateSet('dashboard', 'experiment', 'setup', 'verify', 'test', 'doctor', 'stop')]
    [string]$Action = 'dashboard',
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:PYTHONPATH = Join-Path $PSScriptRoot 'src'
$env:PYTHONUTF8 = '1'
$pythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if ($Action -eq 'setup') {
    if (-not (Test-Path -LiteralPath $pythonPath)) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Creating the Python environment failed. Use Python 3.12 or 3.13.' }
    }
    & $pythonPath -m pip install -e '.[dev]'
    if ($LASTEXITCODE -ne 0) { throw 'Installing dependencies failed.' }
    exit 0
}
if (-not (Test-Path -LiteralPath $pythonPath)) { throw 'Run .\run.ps1 setup first.' }
switch ($Action) {
    'dashboard' { & $pythonPath -m streamlit run app.py @ExtraArgs }
    'experiment' {
        docker compose up -d --wait --wait-timeout 180
        if ($LASTEXITCODE -ne 0) { throw 'Start Docker Desktop, then retry.' }
        & $pythonPath -m earlybird.cli doctor
        if ($LASTEXITCODE -ne 0) { throw 'Database verification failed. Inspect docker compose logs.' }
        & $pythonPath -m earlybird.cli run @ExtraArgs
    }
    'verify' { & $pythonPath -m earlybird.cli verify }
    'doctor' { & $pythonPath -m earlybird.cli doctor }
    'test' { & $pythonPath -m pytest @ExtraArgs }
    'stop' { docker compose stop }
}
if ($LASTEXITCODE -ne 0) { throw "$Action failed with exit code $LASTEXITCODE" }
