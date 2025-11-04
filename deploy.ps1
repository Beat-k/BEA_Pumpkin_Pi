# Deployment Script for BEA Pumpkin Pi Alexa Skill
# ==================================================
# PowerShell script for automated deployment to AWS

param(
    [string]$Environment = "development",
    [string]$Region = "us-east-1",
    [switch]$SkipTests = $false,
    [switch]$UpdateSkillManifest = $true,
    [switch]$UpdateInteractionModel = $true,
    [switch]$DeployLambda = $true
)

Write-Host "🎵 BEA Pumpkin Pi Deployment Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Region: $Region" -ForegroundColor Yellow
Write-Host ""

# Configuration
$SkillName = "BEA_Pumpkin_Pi"
$LambdaFunctionName = "ask-bea-pumpkin-pi-default"
$SkillId = ""  # Will be populated after skill creation

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Green

# Check if ASK CLI is installed
try {
    $askVersion = ask --version
    Write-Host "✅ ASK CLI found: $askVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ASK CLI not found. Please install with: npm install -g ask-cli" -ForegroundColor Red
    exit 1
}

# Check if AWS CLI is installed
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI found: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install AWS CLI" -ForegroundColor Red
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Run tests (unless skipped)
if (-not $SkipTests) {
    Write-Host "🧪 Running tests..." -ForegroundColor Green
    
    # Change to lambda directory
    Set-Location -Path "lambda"
    
    # Install test dependencies
    Write-Host "Installing test dependencies..." -ForegroundColor Yellow
    python -m pip install pytest pytest-mock numpy scipy --quiet
    
    # Run unit tests
    Write-Host "Running unit tests..." -ForegroundColor Yellow
    $testResult = python -m pytest test_bea_components.py -v
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Tests failed. Deployment aborted." -ForegroundColor Red
        Set-Location -Path ".."
        exit 1
    }
    
    Write-Host "✅ All tests passed!" -ForegroundColor Green
    Set-Location -Path ".."
    Write-Host ""
}

# Package Lambda function
if ($DeployLambda) {
    Write-Host "📦 Packaging Lambda function..." -ForegroundColor Green
    
    # Create deployment package directory
    $PackageDir = "deployment_package"
    if (Test-Path $PackageDir) {
        Remove-Item -Recurse -Force $PackageDir
    }
    New-Item -ItemType Directory -Path $PackageDir | Out-Null
    
    # Copy Lambda code
    Copy-Item -Path "lambda\*" -Destination $PackageDir -Recurse
    
    # Install dependencies
    Set-Location -Path $PackageDir
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt -t . --quiet
    
    # Create deployment ZIP
    $ZipFile = "..\bea-pumpkin-pi-lambda.zip"
    if (Test-Path $ZipFile) {
        Remove-Item $ZipFile
    }
    
    Write-Host "Creating deployment package..." -ForegroundColor Yellow
    Compress-Archive -Path "*" -DestinationPath $ZipFile
    
    Set-Location -Path ".."
    Remove-Item -Recurse -Force $PackageDir
    
    Write-Host "✅ Lambda package created: bea-pumpkin-pi-lambda.zip" -ForegroundColor Green
    Write-Host ""
}

# Deploy or update Lambda function
if ($DeployLambda) {
    Write-Host "🚀 Deploying Lambda function..." -ForegroundColor Green
    
    # Check if function exists
    $functionExists = $false
    try {
        aws lambda get-function --function-name $LambdaFunctionName --region $Region | Out-Null
        $functionExists = $true
        Write-Host "Function exists, updating..." -ForegroundColor Yellow
    } catch {
        Write-Host "Function doesn't exist, creating..." -ForegroundColor Yellow
    }
    
    if ($functionExists) {
        # Update existing function
        aws lambda update-function-code --function-name $LambdaFunctionName --zip-file fileb://bea-pumpkin-pi-lambda.zip --region $Region
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Lambda function updated successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to update Lambda function" -ForegroundColor Red
        }
    } else {
        # Create new function
        $createResult = aws lambda create-function --function-name $LambdaFunctionName --runtime "python3.9" --role "arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role" --handler "lambda_function.handler" --zip-file fileb://bea-pumpkin-pi-lambda.zip --timeout 30 --memory-size 256 --region $Region
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Lambda function created successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to create Lambda function" -ForegroundColor Red
            Write-Host "Please ensure you have the correct IAM role configured" -ForegroundColor Yellow
        }
    }
    
    # Clean up deployment package
    Remove-Item "bea-pumpkin-pi-lambda.zip"
    Write-Host ""
}

# Deploy skill manifest
if ($UpdateSkillManifest) {
    Write-Host "📝 Updating skill manifest..." -ForegroundColor Green
    
    $deployResult = ask smapi update-skill-manifest --skill-id $SkillId --manifest file://skill.json --stage $Environment
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Skill manifest updated successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to update skill manifest" -ForegroundColor Red
        Write-Host "You may need to create the skill first with: ask smapi create-skill" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Deploy interaction model
if ($UpdateInteractionModel) {
    Write-Host "🗣️ Updating interaction model..." -ForegroundColor Green
    
    $modelResult = ask smapi update-interaction-model --skill-id $SkillId --locale en-US --interaction-model file://models/en-US.json --stage $Environment
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Interaction model updated successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to update interaction model" -ForegroundColor Red
    }
    Write-Host ""
}

# Test skill endpoint
Write-Host "🔍 Testing skill endpoint..." -ForegroundColor Green

$testRequest = @"
{
    "version": "1.0",
    "session": {
        "new": true,
        "sessionId": "test-session",
        "user": {
            "userId": "test-user"
        }
    },
    "request": {
        "type": "LaunchRequest",
        "requestId": "test-request",
        "timestamp": "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')"
    }
}
"@

# Save test request to file
$testRequest | Out-File -FilePath "test_request.json" -Encoding UTF8

# Test Lambda function directly
try {
    $testResult = aws lambda invoke --function-name $LambdaFunctionName --payload file://test_request.json --region $Region test_response.json
    
    if (Test-Path "test_response.json") {
        $response = Get-Content "test_response.json" | ConvertFrom-Json
        Write-Host "✅ Skill endpoint test successful!" -ForegroundColor Green
        Write-Host "Response: $($response.response.outputSpeech.text)" -ForegroundColor Cyan
        
        # Clean up test files
        Remove-Item "test_request.json"
        Remove-Item "test_response.json"
    }
} catch {
    Write-Host "⚠️ Endpoint test failed - this may be normal if Lambda function isn't created yet" -ForegroundColor Yellow
}

Write-Host ""

# Deployment summary
Write-Host "📋 Deployment Summary" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor White
Write-Host "Region: $Region" -ForegroundColor White
Write-Host "Lambda Function: $LambdaFunctionName" -ForegroundColor White
Write-Host "Skill Name: $SkillName" -ForegroundColor White

if ($SkillId) {
    Write-Host "Skill ID: $SkillId" -ForegroundColor White
}

Write-Host ""
Write-Host "🎵 BEA Pumpkin Pi deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test your skill in the Alexa Developer Console" -ForegroundColor White
Write-Host "2. Enable the skill for testing on your Echo devices" -ForegroundColor White
Write-Host "3. Try voice commands like 'Alexa, ask Pumpkin Pi to enhance my audio'" -ForegroundColor White
Write-Host ""
Write-Host "For support, contact: jeremyjackson7@proton.me" -ForegroundColor Cyan