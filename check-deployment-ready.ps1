# 🔧 BEA Pumpkin Pi - Quick Deployment Setup Verification

Write-Host "🎵 BEA Pumpkin Pi - Deployment Tool Verification" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host ""

# Check Python
Write-Host "🐍 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        $version = [Version]$matches[1]
        if ($version -ge [Version]"3.8") {
            Write-Host "✅ Python $pythonVersion - GOOD" -ForegroundColor Green
        } else {
            Write-Host "❌ Python $pythonVersion - Need 3.8+" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "❌ Python not found" -ForegroundColor Red
}

# Check AWS CLI
Write-Host "☁️ Checking AWS CLI..." -ForegroundColor Yellow
try {
    $awsPath = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"
    if (Test-Path $awsPath) {
        $awsVersion = & $awsPath --version 2>&1
        Write-Host "✅ $awsVersion - GOOD" -ForegroundColor Green
    } else {
        Write-Host "❌ AWS CLI not found at expected path" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ AWS CLI not working" -ForegroundColor Red
}

# Check Node.js
Write-Host "📦 Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v(\d+)\.") {
        $version = [int]$matches[1]
        if ($version -ge 14) {
            Write-Host "✅ Node.js $nodeVersion - GOOD" -ForegroundColor Green
        } else {
            Write-Host "❌ Node.js $nodeVersion - Need v14+" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "❌ Node.js not found" -ForegroundColor Red
}

# Check ASK CLI
Write-Host "🗣️ Checking ASK CLI..." -ForegroundColor Yellow
try {
    $askVersion = ask --version 2>&1
    Write-Host "✅ ASK CLI v$askVersion - GOOD" -ForegroundColor Green
} catch {
    Write-Host "❌ ASK CLI not found" -ForegroundColor Red
}

# Check Lambda package
Write-Host "📦 Checking Lambda package..." -ForegroundColor Yellow
if (Test-Path "bea-pumpkin-pi-lambda.zip") {
    $size = (Get-Item "bea-pumpkin-pi-lambda.zip").Length / 1MB
    Write-Host "✅ Lambda package ready ($([math]::Round($size, 1)) MB)" -ForegroundColor Green
} else {
    Write-Host "❌ Lambda package not found" -ForegroundColor Red
}

# Check skill files
Write-Host "📄 Checking skill files..." -ForegroundColor Yellow
$requiredFiles = @("skill.json", "models/en-US.json", "lambda/lambda_function.py")
$allPresent = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file" -ForegroundColor Red
        $allPresent = $false
    }
}

Write-Host ""
Write-Host "🎯 DEPLOYMENT READINESS CHECK" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Gray

if ($allPresent) {
    Write-Host "🚀 BEA Pumpkin Pi is READY for deployment!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Create AWS account (if needed): https://aws.amazon.com/free/" -ForegroundColor White
    Write-Host "2. Create Amazon Developer account: https://developer.amazon.com/" -ForegroundColor White
    Write-Host "3. Configure AWS CLI: aws configure" -ForegroundColor White
    Write-Host "4. Configure ASK CLI: ask configure" -ForegroundColor White
    Write-Host "5. Follow ACCOUNT_SETUP_GUIDE.md for detailed instructions" -ForegroundColor White
} else {
    Write-Host "⚠️  Some files are missing. Please check the setup." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📖 For detailed setup instructions, see:" -ForegroundColor Cyan
Write-Host "   - ACCOUNT_SETUP_GUIDE.md" -ForegroundColor White
Write-Host "   - DEPLOYMENT_GUIDE.md" -ForegroundColor White
Write-Host ""
Write-Host "Need help? Email: jeremyjackson7@proton.me" -ForegroundColor Cyan