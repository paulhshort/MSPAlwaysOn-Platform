# MSPAlwaysOn + Keep.dev Integration Setup Script

Write-Host "Setting up MSPAlwaysOn + Keep.dev Integration..." -ForegroundColor Green

# Create necessary directories if they don't exist
$directories = @(
    "backend/app/api/routes",
    "backend/app/core",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/services",
    "backend/keep_integration/adapters",
    "backend/keep_integration/providers",
    "frontend/app/components",
    "frontend/app/features",
    "frontend/app/lib",
    "scripts"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        Write-Host "Creating directory: $dir" -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Create empty placeholder files to maintain directory structure in git
$placeholders = @(
    "backend/app/api/routes/__init__.py",
    "backend/app/core/__init__.py",
    "backend/app/models/__init__.py",
    "backend/app/schemas/__init__.py",
    "backend/app/services/__init__.py",
    "backend/keep_integration/adapters/__init__.py",
    "backend/keep_integration/providers/__init__.py"
)

foreach ($file in $placeholders) {
    if (-not (Test-Path $file)) {
        Write-Host "Creating placeholder file: $file" -ForegroundColor Yellow
        New-Item -ItemType File -Path $file -Force | Out-Null
        Set-Content -Path $file -Value "# Placeholder file to maintain directory structure" -Force
    }
}

# Create scripts directory for database initialization
if (-not (Test-Path "scripts/create-multiple-postgresql-databases.sh")) {
    Write-Host "Creating database initialization script" -ForegroundColor Yellow
    Copy-Item -Path "scripts/create-multiple-postgresql-databases.sh" -Destination "scripts/create-multiple-postgresql-databases.sh" -Force
    # Make the script executable
    # Note: This doesn't work on Windows, but it's included for documentation
    # chmod +x scripts/create-multiple-postgresql-databases.sh
}

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Start the development environment: docker-compose up -d" -ForegroundColor Cyan
Write-Host "2. Implement MSP-specific providers" -ForegroundColor Cyan
Write-Host "3. Extend the data model for MSP entities" -ForegroundColor Cyan
Write-Host "4. Develop the frontend with MSP-specific views" -ForegroundColor Cyan
