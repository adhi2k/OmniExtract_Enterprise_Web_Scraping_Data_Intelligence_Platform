# PowerShell script to push OmniExtract project to GitHub
param(
    [string]$RepoName = "omniextract-data-pipeline"
)

Write-Host "=== OmniExtract Platform GitHub Deployment ===" -ForegroundColor Cyan

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
    Write-Host "[1/4] Git repository initialized." -ForegroundColor Green
}

# 2. Add and commit files
Write-Host "[2/4] Staging and committing files..." -ForegroundColor Yellow
git add .
git commit -m "feat: OmniExtract automated web scraping platform, datasets, and presentation dashboard"

# 3. Check for GitHub CLI (gh)
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "[3/4] GitHub CLI detected. Creating remote repository..." -ForegroundColor Yellow
    gh repo create $RepoName --public --source=. --remote=origin --push
    if ($LASTEXITCODE -eq 0) {
        Write-Host "=== SUCCESS: Published to GitHub ===" -ForegroundColor Green
        gh repo view --web
        exit 0
    }
}

# 4. Push via Remote URL
Write-Host "[3/4] Enter your GitHub Repository URL (or press Enter to use default):" -ForegroundColor Cyan
$RemoteUrl = Read-Host "GitHub Remote URL"

if ($RemoteUrl) {
    git remote remove origin -ErrorAction SilentlyContinue
    git remote add origin $RemoteUrl
    Write-Host "[4/4] Pushing to GitHub main branch..." -ForegroundColor Yellow
    git push -u origin main
    Write-Host "=== Repository pushed successfully! ===" -ForegroundColor Green
} else {
    Write-Host "Run the following commands to push:" -ForegroundColor Yellow
    Write-Host "  git remote add origin https://github.com/<YOUR_USERNAME>/$RepoName.git"
    Write-Host "  git push -u origin main"
}
