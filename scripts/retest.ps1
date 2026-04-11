# Run pytest from the repository root.
# Usage and examples: see scripts/retest.md
param()
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $RepoRoot
try {
    python -m pytest @args
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
