# PowerShell script to initialize git and push to GitHub
param(
    [string]$RepoName = "relu-data-extraction-fte"
)

Write-Host "=== Relu Consultancy Challenge GitHub Deployment ===" -ForegroundColor Cyan

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# 1. Initialize Git
if (-not (Test-Path ".git")) {
    Write-Host "[1/4] Initializing Git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
} else {
    Write-Host "[1/4] Git repository already initialized." -ForegroundColor Green
}

# 2. Add and commit files
Write-Host "[2/4] Staging and committing files..." -ForegroundColor Yellow
git add .
git commit -m "Relu Consultancy FTE Challenge: Disney Cruise & Ingredients Network Scrapers with WebApp Dashboard"

# 3. Check for GitHub CLI (gh)
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "[3/4] GitHub CLI detected. Attempting automatic repository creation..." -ForegroundColor Yellow
    gh repo create $RepoName --public --source=. --remote=origin --push
    if ($LASTEXITCODE -eq 0) {
        Write-Host "=== SUCCESS: Hosted on GitHub ===" -ForegroundColor Green
        gh repo view --web
        exit 0
    }
}

# 4. Manual GitHub remote setup prompt
Write-Host "[3/4] Please enter your GitHub Repository URL (e.g., https://github.com/YOUR_USERNAME/$RepoName.git):" -ForegroundColor Cyan
$RemoteUrl = Read-Host "GitHub Remote URL"

if ($RemoteUrl) {
    git remote remove origin -ErrorAction SilentlyContinue
    git remote add origin $RemoteUrl
    Write-Host "[4/4] Pushing to GitHub main branch..." -ForegroundColor Yellow
    git push -u origin main
    Write-Host "=== Repository pushed successfully! ===" -ForegroundColor Green
} else {
    Write-Host "[NOTICE] To push manually later, run:" -ForegroundColor Yellow
    Write-Host "  git remote add origin https://github.com/<YOUR_USERNAME>/$RepoName.git"
    Write-Host "  git push -u origin main"
}
