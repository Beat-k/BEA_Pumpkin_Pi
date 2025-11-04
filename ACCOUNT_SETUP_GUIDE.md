# 🚀 BEA Pumpkin Pi - Complete Deployment Setup Guide

## 📋 **Account Setup Requirements**

You'll need these accounts to deploy your BEA Pumpkin Pi skill:

### 1. **AWS Account** (Free Tier Available)
- **Purpose**: Host the Lambda function (backend processing)
- **Cost**: Free tier includes 1M Lambda requests/month
- **Sign up**: https://aws.amazon.com/free/

### 2. **Amazon Developer Account** (Free)
- **Purpose**: Publish Alexa skills
- **Cost**: Completely free
- **Sign up**: https://developer.amazon.com/alexa

## 🔧 **Step-by-Step Account Setup**

### **Step 1: Create AWS Account**

1. **Go to AWS Free Tier**: https://aws.amazon.com/free/
2. **Click "Create a Free Account"**
3. **Fill in account details**:
   - Email address
   - Password  
   - AWS account name (e.g., "BEA-Development")
4. **Provide contact information**
5. **Enter payment method** (won't be charged with free tier)
6. **Verify phone number**
7. **Choose support plan**: Basic (Free)

### **Step 2: Create IAM User for Development**

**Important**: Don't use root account for development!

1. **Sign in to AWS Console**: https://console.aws.amazon.com/
2. **Go to IAM Service**: Search "IAM" in the search bar
3. **Create User**:
   - Click "Users" → "Create user"
   - Username: `bea-developer`
   - Access type: ✅ Programmatic access
4. **Attach Policies**:
   - ✅ `AWSLambda_FullAccess`
   - ✅ `IAMFullAccess` (for creating Lambda execution role)
   - ✅ `CloudWatchLogsFullAccess`
5. **Save Access Keys**: Download CSV with:
   - Access Key ID
   - Secret Access Key
   - **Keep these secure!**

### **Step 3: Create Amazon Developer Account**

1. **Go to Amazon Developer Portal**: https://developer.amazon.com/
2. **Click "Sign In"** → "Create your Amazon Developer account"
3. **Use same email as AWS** (recommended for easier management)
4. **Fill in developer information**:
   - Name/Company: "BEATEK" or your preferred name
   - Country: Your location
   - Address information
5. **Accept terms and conditions**
6. **Verify email address**

### **Step 4: Configure AWS CLI**

Open a **NEW** PowerShell window (to pick up AWS CLI):

```powershell
# Configure AWS CLI with your IAM user credentials
aws configure

# You'll be prompted for:
# AWS Access Key ID: [Enter from downloaded CSV]
# AWS Secret Access Key: [Enter from downloaded CSV]  
# Default region name: us-east-1 (recommended for Alexa)
# Default output format: json
```

### **Step 5: Configure ASK CLI**

```powershell
# Configure Alexa Skills Kit CLI
ask configure

# This will:
# 1. Open a browser window
# 2. Ask you to sign in to your Amazon Developer account
# 3. Authorize ASK CLI to access your account
# 4. Create a profile for development
```

## 🛠️ **Create Lambda Execution Role**

Your Lambda function needs permissions to run. Let's create the role:

```powershell
# Create trust policy for Lambda
$TrustPolicy = @"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
"@

# Save to file
$TrustPolicy | Out-File -FilePath "lambda-trust-policy.json" -Encoding UTF8

# Create the IAM role
aws iam create-role \
  --role-name BEAPumpkinPiLambdaRole \
  --assume-role-policy-document file://lambda-trust-policy.json

# Attach basic execution policy
aws iam attach-role-policy \
  --role-name BEAPumpkinPiLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Get your account ID (needed for role ARN)
aws sts get-caller-identity --query Account --output text
```

## 🚀 **Deploy BEA Pumpkin Pi Skill**

Once accounts are set up, run these commands:

### **Deploy Lambda Function**

```powershell
# Get your AWS account ID first
$AccountId = aws sts get-caller-identity --query Account --output text

# Create Lambda function
aws lambda create-function \
  --function-name bea-pumpkin-pi \
  --runtime python3.9 \
  --role arn:aws:iam::${AccountId}:role/BEAPumpkinPiLambdaRole \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://bea-pumpkin-pi-lambda.zip \
  --timeout 30 \
  --memory-size 512 \
  --description "BEA Pumpkin Pi - 4D Audio Enhancement for Amazon Alexa"

# Set environment variables for optimal performance
aws lambda update-function-configuration \
  --function-name bea-pumpkin-pi \
  --environment Variables='{
    "BEA_LOG_LEVEL":"INFO",
    "BEA_AUDIO_QUALITY":"high",
    "BEA_GAMING_MODE":"enabled",
    "BEA_EMOTIONAL_LEARNING":"enabled"
  }'
```

### **Get Lambda Function ARN**

```powershell
# Get the Lambda ARN (needed for skill.json)
$LambdaArn = aws lambda get-function --function-name bea-pumpkin-pi --query Configuration.FunctionArn --output text
Write-Host "Lambda ARN: $LambdaArn"
```

### **Update Skill Manifest**

You'll need to update `skill.json` with your Lambda ARN:

```json
{
  "manifest": {
    "apis": {
      "custom": {
        "endpoint": {
          "uri": "YOUR_LAMBDA_ARN_HERE"
        }
      }
    }
  }
}
```

### **Deploy Alexa Skill**

```powershell
# Initialize ASK project (if needed)
ask init

# Deploy the skill
ask deploy

# Enable skill for testing
ask dialog --locale en-US
```

## 🧪 **Test Your Skill**

### **Test Lambda Function Directly**

```powershell
# Test Lambda with a sample event
$TestEvent = @"
{
  "request": {
    "type": "LaunchRequest",
    "requestId": "test-request-id",
    "locale": "en-US"
  },
  "session": {
    "sessionId": "test-session-id",
    "user": {
      "userId": "test-user-id"
    }
  }
}
"@

$TestEvent | Out-File -FilePath "test-event.json" -Encoding UTF8

aws lambda invoke \
  --function-name bea-pumpkin-pi \
  --payload file://test-event.json \
  response.json

# Check response
Get-Content response.json
```

### **Test Alexa Skill**

1. **Alexa Developer Console**:
   - Go to https://developer.amazon.com/alexa/console/ask
   - Find your "BEA Pumpkin Pi" skill
   - Click "Test" tab
   - Enable testing for "Development"

2. **Test Commands**:
   ```
   "ask pumpkin pi to enhance my audio"
   "tell pumpkin pi to start gaming mode"
   "ask pumpkin pi to recognize beatbox"
   "tell pumpkin pi I'm feeling excited"
   ```

3. **Test on Echo Device**:
   - Ensure your Echo is linked to the same Amazon account
   - Say: "Alexa, open BEA Pumpkin Pi"

## 🔍 **Monitoring & Troubleshooting**

### **Check Lambda Logs**

```powershell
# View recent logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/bea-pumpkin-pi"

# Stream live logs
aws logs tail "/aws/lambda/bea-pumpkin-pi" --follow
```

### **Monitor Performance**

```powershell
# Check Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=bea-pumpkin-pi \
  --start-time 2025-11-04T00:00:00Z \
  --end-time 2025-11-04T23:59:59Z \
  --period 3600 \
  --statistics Average,Maximum
```

## 💰 **Cost Estimates**

### **AWS Lambda (Free Tier)**
- **Requests**: 1M free requests/month
- **Compute**: 400,000 GB-seconds free/month
- **BEA Pumpkin Pi usage**: Well within free tier for personal use

### **Expected Usage**
- **Voice commands**: ~2-5 seconds each
- **Memory**: 512MB allocated
- **Monthly estimate**: Free for typical personal use

### **Alexa Skills**
- **Development**: Completely free
- **Publishing**: Free
- **Usage**: No charges from Amazon

## 🎯 **Next Steps After Deployment**

1. **Test thoroughly** with various voice commands
2. **Monitor performance** in CloudWatch
3. **Submit for certification** when ready for public release
4. **Add skill to Alexa Skills Store**

## 📞 **Support & Troubleshooting**

### **Common Issues**
- **"Skill not found"**: Check skill is enabled for testing
- **Lambda timeout**: Increase timeout or optimize code
- **Permission denied**: Verify IAM roles and policies
- **Package too large**: Use Lambda layers for dependencies

### **Get Help**
- **AWS Support**: https://aws.amazon.com/support/
- **Alexa Developer Forums**: https://forums.developer.amazon.com/spaces/165/
- **BEA Pumpkin Pi Issues**: https://github.com/Beat-k/BEA_Pumpkin_Pi/issues

---

**🎵 Ready to deploy your BEA Pumpkin Pi skill and revolutionize voice-activated audio! 🎵**

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.