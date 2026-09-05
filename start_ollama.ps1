# ─────────────────────────────────────────────────────────────
# APEX - Local Ollama Service Starter
# Optimized for Dual-Core CPU & 8GB RAM on Drive D
# ─────────────────────────────────────────────────────────────

$OllamaDir = "D:\UNCLECHAN\ollama"
$OllamaExe = "$OllamaDir\ollama.exe"
$ModelsDir = "D:\UNCLECHAN\ollama_models"

if (-not (Test-Path $OllamaExe)) {
    Write-Error "Ollama executable not found at $OllamaExe"
    exit 1
}

# Redirect models to Drive D (preventing Drive C from running out of space)
$env:OLLAMA_MODELS = $ModelsDir
$env:OLLAMA_HOST = "127.0.0.1:11434"

# Concurrency throttles: 1 request, 1 model in RAM (protects dual-core CPU & RAM)
$env:OLLAMA_NUM_PARALLEL = "1"
$env:OLLAMA_MAX_LOADED_MODELS = "1"
$env:OLLAMA_KEEP_ALIVE = "15m"

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host " Starting Ollama (Drive D / Hardware-Optimized)" -ForegroundColor Green
Write-Host " OLLAMA_MODELS = $env:OLLAMA_MODELS" -ForegroundColor Yellow
Write-Host " OLLAMA_HOST   = $env:OLLAMA_HOST" -ForegroundColor Yellow
Write-Host " Host Specs    = Intel Core i3-2350M, 8GB RAM" -ForegroundColor Yellow
Write-Host "======================================================" -ForegroundColor Cyan

& $OllamaExe serve
