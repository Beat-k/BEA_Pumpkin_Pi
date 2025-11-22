# 🚀 BEA Pumpkin Pi - Amazon Alexa Deployment Guide

**Powered by T.A.N.Y.A. (Tiny Autonomous Neural Yield Assistant) & BEA Framework**

## 📋 Overview

Deploy your BEA Pumpkin Pi educational skill with T.A.N.Y.A. integration to Amazon Alexa Skills Kit and AWS Lambda.

This guide covers deployment of the voice-first educational Alexa skill featuring:
- 🤖 T.A.N.Y.A. (Tiny Autonomous Neural Yield Assistant)
- ⚛️ BEA (Binary Emotional Arithmetic) Framework
- 🎓 Educational audio technology content
- ➗ Five BEA mathematical operators (⊕, ⊖, ⊗, ⨀, ≠)
- 💭 32-state emotional intelligence system

---

## 🎯 **STEP 1: AWS Lambda Deployment**

### **Option A: AWS Lambda Console (Recommended - Simplest)**

1. **Go to AWS Lambda Console**
   ```
   https://console.aws.amazon.com/lambda/
   ```

2. **Create New Function**
   - Click "Create function"
   - Choose "Author from scratch"
   - Function name: `BEA-Pumpkin-Pi` (or any name you prefer)
   - Runtime: `Python 3.9` (recommended)
   - Click "Create function"

3. **Upload Your Code**
   - In the Lambda console, scroll to "Code source"
   - Delete the default `lambda_function.py` content
   - Copy and paste entire `aws_lambda_console_ready.py` file
   - File will automatically be named `lambda_function.py`
   - **Handler:** `lambda_function.lambda_handler` (default - no change needed)

4. **No Dependencies Required**
   - ✅ Pure Python standard library only
   - ✅ Zero external packages needed
   - ✅ No pip install or requirements.txt
   - ✅ Fast cold starts and instant deployment

5. **Configure Lambda Settings**
   - Memory: `512 MB` (recommended for T.A.N.Y.A. processing)
   - Timeout: `30 seconds`
   - No environment variables required (all self-contained)

6. **Deploy**
   - Click "Deploy" button
   - Wait for "Successfully updated the function" message
   - Copy the Function ARN (top right) - you'll need this for Alexa

---

## 🎯 **STEP 2: Alexa Developer Console Setup**

### **1. Access Alexa Developer Console**

```
https://developer.amazon.com/alexa/console/ask
```

### **2. Create New Skill (or Update Existing)**

**For New Skill:**
- Click "Create Skill"
- Skill name: `BEA Pumpkin Pi`
- Primary locale: `English (US)`
- Model: `Custom`
- Hosting: `Provision your own` (using AWS Lambda)
- Template: `Start from Scratch`
- Click "Create skill"

**For Existing Skill:**
- Find your "BEA Pumpkin Pi" skill
- Click "Edit"

### **3. Update Interaction Model**

1. **Navigate to Build Tab**
   - Click "Build" in the top navigation

2. **Update JSON Editor**
   - Click "JSON Editor" in left sidebar
   - Delete all existing content
   - Copy entire content from `models/en-US.json`
   - Paste into the JSON Editor
   - Click "Save Model"

3. **Build Model**
   - Click "Build Model" button at top
   - Wait for "Build Successful" message (may take 1-2 minutes)

### **4. Configure Endpoint**

1. **Navigate to Endpoint**
   - Click "Endpoint" in left sidebar

2. **Select AWS Lambda ARN**
   - Service Endpoint Type: `AWS Lambda ARN`
   - Default Region: Paste your Lambda Function ARN
   - Example: `arn:aws:lambda:us-east-1:123456789012:function:BEA-Pumpkin-Pi`

3. **Save Endpoints**
   - Click "Save Endpoints"

---

## 🎯 **STEP 3: Test Your Skill**

### **1. Enable Testing**

1. **Navigate to Test Tab**
   - Click "Test" in top navigation

2. **Enable Skill Testing**
   - Skill testing is enabled in: `Development`

### **2. Test with Alexa Simulator**

Try these voice commands:

```text
"Alexa, open bea pumpkin pi"
"Alexa, ask bea pumpkin pi to teach me about audio"
"Alexa, ask bea pumpkin pi what is tanya"
"Alexa, ask bea pumpkin pi tanya status"
"Alexa, ask bea pumpkin pi to set emotion to curious"
"Alexa, ask bea pumpkin pi to divergence joy from sadness"
"Alexa, ask bea pumpkin pi to combust curiosity and bliss"
```

### **3. Expected Responses**

**T.A.N.Y.A. Status:**
```
"T.A.N.Y.A. stands for Tiny Autonomous Neural Yield Assistant. I'm the
edge-optimized AI engine powered by the BEA Binary Emotional Arithmetic
framework..."
```

**Educational Content:**
```
"Welcome to BEA audio education! I can teach you about frequency, which
is the number of sound wave cycles per second, measured in hertz..."
```

**BEA Calculator:**
```
"Using the BEA Combust operator on Curiosity and Bliss creates Inspiration
with intensity 7. The emergent result demonstrates the 1 plus 1 equals 3
principle..."
```

---

## 🎯 **STEP 4: Troubleshooting**

### **Common Lambda Issues**

**Issue: "Task timed out after 3.00 seconds"**
- Solution: Increase timeout to 30 seconds in Configuration > General configuration

**Issue: "Unable to import module 'lambda_function'"**
- Solution: Ensure file is named `lambda_function.py` with handler `lambda_function.lambda_handler`

**Issue: "Module not found" errors**
- Solution: Check that you're not importing external packages. Code uses only Python standard library.

**Issue: Cold start delays**
- Normal: First invocation may take 1-2 seconds
- Subsequent calls: <100ms response time
- No action needed - this is expected AWS Lambda behavior

### **Common Alexa Issues**

**Issue: "There was a problem with the requested skill's response"**
- Check CloudWatch logs in AWS Lambda console
- Verify Lambda ARN is correctly configured in Endpoint
- Ensure interaction model was built successfully

**Issue: Intent not recognized**
- Verify `models/en-US.json` was pasted correctly
- Check that model was built (click "Build Model")
- Try more specific voice commands from test examples

**Issue: "Skill isn't responding"**
- Check Lambda function has Alexa Skills Kit trigger
- Verify skill is enabled for testing in Development mode
- Review CloudWatch logs for errors

### **T.A.N.Y.A. Specific Issues**

**Issue: Emotional states not working**
- Ensure valid emotional state IDs (E[0] through E[31])
- Try resetting emotion: "set emotion to neutral"
- Check that emotional state name matches exactly

**Issue: BEA math operations failing**
- Verify both emotional states exist in the 32-state system
- Use proper operation names: combust, balance, dissolve, amplify, divergence
- Check voice command format: "{operation} {state1} and/from {state2}"

---

## 🎯 **STEP 5: Monitor and Debug**

### **CloudWatch Logs**

1. **Access Logs**
   - AWS Lambda Console > Monitor > View logs in CloudWatch

2. **What to Look For**
   - "BEA Engine initialized" - Lambda started successfully
   - "T.A.N.Y.A. status: READY" - Framework operational
   - Intent names and slot values - Verify correct intent routing
   - Error messages - Python stack traces for debugging

### **Performance Monitoring**

Check these metrics in CloudWatch:
- **Invocation count** - How many times skill was used
- **Duration** - Average response time (should be <500ms after cold start)
- **Errors** - Any failed invocations
- **Throttles** - Rate limiting (shouldn't occur for normal use)

---

## 🎯 **STEP 6: Certification & Publishing (Optional)**

### **Before Certification**

1. **Complete Skill Information**
   - Distribution > Skill Preview Information
   - Add skill description, example phrases, keywords
   - Upload skill icons (108x108 and 512x512 PNG)

2. **Privacy & Compliance**
   - Distribution > Privacy & Compliance
   - Privacy Policy URL (if collecting user data)
   - Export compliance
   - Testing instructions for certification team

3. **Availability**
   - Distribution > Availability
   - Select distribution countries
   - Beta testing (optional)

### **Certification Process**

1. **Submit for Certification**
   - Click "Submit for Review" in Distribution tab
   - Alexa team reviews within 1-2 weeks
   - May request changes or clarifications

2. **Respond to Feedback**
   - Check email for certification status
   - Address any issues raised by review team
   - Resubmit when ready

3. **Publication**
   - Once approved, skill goes live in Alexa Skills Store
   - Available to all Alexa users worldwide

---

## 📊 **Deployment Checklist**

### **AWS Lambda**

- [ ] Lambda function created
- [ ] Code from `aws_lambda_console_ready.py` pasted
- [ ] Handler set to `lambda_function.lambda_handler`
- [ ] Memory: 512 MB
- [ ] Timeout: 30 seconds
- [ ] Function ARN copied

### **Alexa Skills Kit**

- [ ] Skill created/updated in Developer Console
- [ ] Interaction model from `models/en-US.json` pasted
- [ ] Model built successfully
- [ ] Lambda ARN configured in Endpoint
- [ ] Testing enabled in Development

### **Testing**

- [ ] "what is tanya" command works
- [ ] "tanya status" shows framework info
- [ ] Educational intents respond correctly
- [ ] BEA mathematical operations function
- [ ] Emotional state transitions work
- [ ] No errors in CloudWatch logs

### **Optional - Certification**

- [ ] Skill information completed
- [ ] Icons uploaded (108x108, 512x512)
- [ ] Privacy policy added (if needed)
- [ ] Testing instructions provided
- [ ] Distribution countries selected

---

## 🎓 **What Your Skill Does**

### **Educational Features**

- 🎤 **Audio Technology Education** - Teaches frequency, acoustics, spatial audio concepts
- 🥁 **Beatbox Techniques** - Explains vocal percussion theory and breathing techniques
- ⚛️ **BEA Mathematics** - Interactive demonstrations of emotional arithmetic operators
- 💭 **Emotional Intelligence** - 32-state system for context-aware learning
- 🗣️ **Conversational Learning** - Natural voice-based educational interactions

### **T.A.N.Y.A. Capabilities**

- **Edge-Optimized AI** - Lightweight processing for fast responses
- **Binary Emotional Arithmetic** - Mathematical operations on emotional states
- **Five Core Operators** - ⊕ Combust, ⊖ Balance, ⊗ Dissolve, ⨀ Amplify, ≠ Divergence
- **Autonomous Processing** - Self-contained decision making
- **Educational Focus** - Teaching through interactive conversation

---

## 📞 **Support and Resources**

### **Documentation**

- [README.md](../README.md) - Main project overview
- [QUICK_AMAZON_DEPLOY.md](QUICK_AMAZON_DEPLOY.md) - Quick deployment guide
- [API_REFERENCE.md](API_REFERENCE.md) - Complete BEA Framework API
- [CHANGELOG.md](CHANGELOG.md) - Version history and updates

### **Contact**

- **Email:** jeremyjackson7@proton.me
- **Subject:** "BEA Pumpkin Pi Deployment Support"
- **GitHub:** https://github.com/Beat-k/BEA_Pumpkin_Pi

---

## 📄 **License**

This skill is provided under the MIT License with additional terms for BEA ecosystem integration. See [LICENSE](../LICENSE) for complete details.

Commercial use may require additional licensing for BEA framework components.

---

**🎉 Congratulations! Your BEA Pumpkin Pi skill with T.A.N.Y.A. is now deployed on Amazon Alexa!**

Experience voice-powered educational AI with emotional intelligence! 🎤🤖✨

---

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
