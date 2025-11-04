# BEA Pumpkin Pi Skill - Deployment Guide

## Overview
Complete deployment and testing guide for the BEA Pumpkin Pi Amazon Alexa skill. This skill combines 4D spatial audio processing, TinyAI beatbox recognition, emotional intelligence, and gaming optimization from the BEA ecosystem.

## Prerequisites

### Development Environment
- Python 3.8+ (3.9 recommended for AWS Lambda)
- AWS CLI configured with appropriate permissions
- ASK CLI (Alexa Skills Kit Command Line Interface)
- Node.js 14+ (for ASK CLI)

### AWS Requirements
- AWS Lambda execution role with permissions:
  - `AWSLambdaBasicExecutionRole`
  - CloudWatch Logs access
- Amazon Developer Account with Alexa Skills enabled

### Local Dependencies
```bash
pip install -r requirements.txt
pip install pytest psutil  # For testing
```

## Quick Start

### Option 1: Automated Deployment (Recommended)

**Windows (PowerShell):**
```powershell
.\deploy.ps1
```

**Linux/macOS (Bash):**
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Deployment

1. **Run Tests**
   ```bash
   cd lambda
   python -m pytest test_bea_components.py -v
   ```

2. **Package Lambda Function**
   ```bash
   cd lambda
   zip -r ../bea-pumpkin-pi-lambda.zip . -x "test_*.py" "__pycache__/*"
   ```

3. **Deploy to AWS Lambda**
   ```bash
   aws lambda create-function \
     --function-name bea-pumpkin-pi \
     --runtime python3.9 \
     --handler lambda_function.lambda_handler \
     --zip-file fileb://../bea-pumpkin-pi-lambda.zip \
     --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role
   ```

4. **Deploy Alexa Skill**
   ```bash
   ask deploy
   ```

## Configuration

### Environment Variables
Set these in AWS Lambda configuration:

- `BEA_LOG_LEVEL`: `INFO` (or `DEBUG` for troubleshooting)
- `BEA_AUDIO_QUALITY`: `high` (or `standard` for lower latency)
- `BEA_GAMING_MODE`: `enabled` (or `disabled` to skip gaming features)
- `BEA_EMOTIONAL_LEARNING`: `enabled` (or `disabled` for privacy)

### Skill Settings
Update `skill.json` before deployment:

1. Replace `YOUR_LAMBDA_ARN` with your actual Lambda function ARN
2. Update `publishingInformation.distributionCountries` as needed
3. Modify `privacyAndCompliance` settings for your compliance requirements

### Regional Settings
For regions other than US-East-1:

1. Update Lambda region in deployment scripts
2. Modify `skill.json` endpoint region
3. Update interaction model in `models/` directory for additional locales

## Testing

### Unit Tests
```bash
cd lambda
python -m pytest test_bea_components.py -v --tb=short
```

### Integration Tests
```bash
cd lambda
python -m pytest test_bea_components.py::TestIntegration -v
```

### Performance Tests
```bash
cd lambda
python -m pytest test_bea_components.py::test_performance_requirements -v
python -m pytest test_bea_components.py::test_memory_usage -v
```

### Alexa Skill Testing
1. **Simulator Testing:**
   - Open [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
   - Navigate to your skill → Test tab
   - Enable testing and try voice commands

2. **Device Testing:**
   - Ensure your Echo device is linked to your developer account
   - Say "Alexa, open BEA Pumpkin Pi"

### Test Commands
Try these voice interactions:

- **Launch:** "Alexa, open BEA Pumpkin Pi"
- **Audio Enhancement:** "enhance my audio for gaming"
- **Beatbox Recognition:** "listen to my beatbox"
- **Emotional State:** "set emotional state to excited"
- **Gaming Mode:** "start gaming mode for FPS"
- **Spatial Audio:** "create spatial audio at position one two three"

## Troubleshooting

### Common Issues

**Import Errors in Local Testing:**
- Expected behavior - ASK SDK packages are provided in Lambda environment
- Use `pytest -k "not test_intent_handlers"` to skip handler tests locally

**Lambda Timeout:**
- Increase timeout in Lambda configuration (recommend 30 seconds)
- Check `BEA_AUDIO_QUALITY` setting - use `standard` for faster processing

**Skill Not Responding:**
- Verify Lambda function ARN in `skill.json`
- Check CloudWatch logs for errors
- Ensure Lambda execution role has correct permissions

**Audio Quality Issues:**
- Adjust `enhancement_strength` in processing configuration
- Verify Echo Dot optimization is enabled
- Check `BEA_AUDIO_QUALITY` environment variable

### Debugging Steps

1. **Check Lambda Logs:**
   ```bash
   aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/bea-pumpkin-pi"
   aws logs tail "/aws/lambda/bea-pumpkin-pi" --follow
   ```

2. **Test Lambda Function Directly:**
   ```bash
   aws lambda invoke \
     --function-name bea-pumpkin-pi \
     --payload '{"request":{"type":"LaunchRequest"}}' \
     response.json
   ```

3. **Validate Skill Manifest:**
   ```bash
   ask api validate-skill -s YOUR_SKILL_ID
   ```

### Performance Optimization

**For High-Performance Requirements:**
- Set `BEA_AUDIO_QUALITY=standard`
- Reduce `enhancement_strength` to 1.0-2.0 range
- Enable `optimize_for_echo_dot()` in configuration
- Use `ProcessingMode.EFFICIENT` for lower latency

**For Maximum Quality:**
- Set `BEA_AUDIO_QUALITY=high`
- Increase Lambda memory to 512MB or higher
- Use `ProcessingMode.REAL_TIME` with higher `enhancement_strength`

## Monitoring

### CloudWatch Metrics
Monitor these key metrics:
- Function Duration (target: <5 seconds)
- Function Errors (target: <1%)
- Concurrent Executions
- Memory Utilization

### Custom Metrics
The skill reports these custom metrics:
- Audio processing time
- Beatbox recognition accuracy
- Gaming session duration
- Emotional state transitions

### Log Analysis
Key log patterns to monitor:
- `"BEA-4D-PROCESSING"` - Audio processing events
- `"BEATBOX-RECOGNITION"` - Recognition results
- `"EMOTIONAL-UPDATE"` - User emotional state changes
- `"GAMING-SESSION"` - Gaming optimization events

## Security

### User Data Protection
- Emotional profiles stored temporarily in Lambda memory only
- No persistent storage of voice data
- User preferences cleared after session timeout

### Privacy Compliance
- Update `privacyAndCompliance` section in `skill.json`
- Implement data deletion upon user request
- Follow Alexa Voice Service guidelines

### API Security
- Lambda function uses IAM roles for AWS access
- No API keys stored in code
- All external dependencies via secure HTTPS

## Maintenance

### Updates
1. Update component code
2. Run full test suite
3. Deploy using automated scripts
4. Monitor CloudWatch for issues
5. Update skill version in manifest

### Monitoring Schedule
- **Daily:** Check error rates and performance
- **Weekly:** Review CloudWatch logs for patterns
- **Monthly:** Update dependencies and security patches

### Version Control
- Tag releases in git
- Maintain deployment logs
- Track performance regression

## Support

### Documentation
- [Amazon Alexa Skills Kit Documentation](https://developer.amazon.com/en-US/docs/alexa/ask-overviews/what-is-the-alexa-skills-kit.html)
- [AWS Lambda Python Documentation](https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html)
- [BEA Ecosystem Documentation](./README.md)

### Contact
For issues specific to BEA Pumpkin Pi skill:
1. Check CloudWatch logs first
2. Run local test suite
3. Review this deployment guide
4. Contact BEATEK support with logs and error details

---

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.