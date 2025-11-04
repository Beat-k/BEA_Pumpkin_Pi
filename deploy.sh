#!/bin/bash

# Deployment Script for BEA Pumpkin Pi Alexa Skill (Linux/macOS)
# ================================================================

set -e  # Exit on any error

# Configuration
ENVIRONMENT=${1:-development}
REGION=${2:-us-east-1}
SKILL_NAME="BEA_Pumpkin_Pi"
LAMBDA_FUNCTION_NAME="ask-bea-pumpkin-pi-default"
SKILL_ID=""  # Will be populated after skill creation

echo "🎵 BEA Pumpkin Pi Deployment Script"
echo "================================================"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check if ASK CLI is installed
if command -v ask >/dev/null 2>&1; then
    ASK_VERSION=$(ask --version)
    echo "✅ ASK CLI found: $ASK_VERSION"
else
    echo "❌ ASK CLI not found. Please install with: npm install -g ask-cli"
    exit 1
fi

# Check if AWS CLI is installed
if command -v aws >/dev/null 2>&1; then
    AWS_VERSION=$(aws --version)
    echo "✅ AWS CLI found: $AWS_VERSION"
else
    echo "❌ AWS CLI not found. Please install AWS CLI"
    exit 1
fi

# Check if Python is installed
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo ""

# Run tests
echo "🧪 Running tests..."

# Change to lambda directory
cd lambda

# Install test dependencies
echo "Installing test dependencies..."
python3 -m pip install pytest pytest-mock numpy scipy --quiet

# Run unit tests
echo "Running unit tests..."
if python3 -m pytest test_bea_components.py -v; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed. Deployment aborted."
    exit 1
fi

cd ..
echo ""

# Package Lambda function
echo "📦 Packaging Lambda function..."

# Create deployment package directory
PACKAGE_DIR="deployment_package"
if [ -d "$PACKAGE_DIR" ]; then
    rm -rf "$PACKAGE_DIR"
fi
mkdir "$PACKAGE_DIR"

# Copy Lambda code
cp -r lambda/* "$PACKAGE_DIR/"

# Install dependencies
cd "$PACKAGE_DIR"
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt -t . --quiet

# Create deployment ZIP
ZIP_FILE="../bea-pumpkin-pi-lambda.zip"
if [ -f "$ZIP_FILE" ]; then
    rm "$ZIP_FILE"
fi

echo "Creating deployment package..."
zip -r "$ZIP_FILE" . >/dev/null

cd ..
rm -rf "$PACKAGE_DIR"

echo "✅ Lambda package created: bea-pumpkin-pi-lambda.zip"
echo ""

# Deploy or update Lambda function
echo "🚀 Deploying Lambda function..."

# Check if function exists
if aws lambda get-function --function-name "$LAMBDA_FUNCTION_NAME" --region "$REGION" >/dev/null 2>&1; then
    echo "Function exists, updating..."
    aws lambda update-function-code \
        --function-name "$LAMBDA_FUNCTION_NAME" \
        --zip-file fileb://bea-pumpkin-pi-lambda.zip \
        --region "$REGION"
    echo "✅ Lambda function updated successfully!"
else
    echo "Function doesn't exist, creating..."
    aws lambda create-function \
        --function-name "$LAMBDA_FUNCTION_NAME" \
        --runtime "python3.9" \
        --role "arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role" \
        --handler "lambda_function.handler" \
        --zip-file fileb://bea-pumpkin-pi-lambda.zip \
        --timeout 30 \
        --memory-size 256 \
        --region "$REGION"
    echo "✅ Lambda function created successfully!"
fi

# Clean up deployment package
rm bea-pumpkin-pi-lambda.zip
echo ""

# Deploy skill manifest (if SKILL_ID is set)
if [ -n "$SKILL_ID" ]; then
    echo "📝 Updating skill manifest..."
    if ask smapi update-skill-manifest --skill-id "$SKILL_ID" --manifest file://skill.json --stage "$ENVIRONMENT"; then
        echo "✅ Skill manifest updated successfully!"
    else
        echo "❌ Failed to update skill manifest"
        echo "You may need to create the skill first with: ask smapi create-skill"
    fi
    echo ""

    # Deploy interaction model
    echo "🗣️ Updating interaction model..."
    if ask smapi update-interaction-model --skill-id "$SKILL_ID" --locale en-US --interaction-model file://models/en-US.json --stage "$ENVIRONMENT"; then
        echo "✅ Interaction model updated successfully!"
    else
        echo "❌ Failed to update interaction model"
    fi
    echo ""
fi

# Test skill endpoint
echo "🔍 Testing skill endpoint..."

# Create test request
cat > test_request.json << EOF
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
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    }
}
EOF

# Test Lambda function directly
if aws lambda invoke \
    --function-name "$LAMBDA_FUNCTION_NAME" \
    --payload file://test_request.json \
    --region "$REGION" \
    test_response.json >/dev/null 2>&1; then
    
    if [ -f "test_response.json" ]; then
        echo "✅ Skill endpoint test successful!"
        RESPONSE_TEXT=$(python3 -c "
import json
with open('test_response.json') as f:
    data = json.load(f)
    print(data.get('response', {}).get('outputSpeech', {}).get('text', 'No response text'))
")
        echo "Response: $RESPONSE_TEXT"
        
        # Clean up test files
        rm test_request.json test_response.json
    fi
else
    echo "⚠️ Endpoint test failed - this may be normal if Lambda function isn't created yet"
fi

echo ""

# Deployment summary
echo "📋 Deployment Summary"
echo "====================="
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo "Lambda Function: $LAMBDA_FUNCTION_NAME"
echo "Skill Name: $SKILL_NAME"

if [ -n "$SKILL_ID" ]; then
    echo "Skill ID: $SKILL_ID"
fi

echo ""
echo "🎵 BEA Pumpkin Pi deployment completed!"
echo ""
echo "Next steps:"
echo "1. Test your skill in the Alexa Developer Console"
echo "2. Enable the skill for testing on your Echo devices"
echo "3. Try voice commands like 'Alexa, ask Pumpkin Pi to enhance my audio'"
echo ""
echo "For support, contact: jeremyjackson7@proton.me"