#!/usr/bin/env python3
"""
BEA Pumpkin Pi TinyAI - Quick Amazon Deployment Package Creator
=============================================================

This script creates a deployment-ready package for AWS Lambda with all TinyAI components.

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
"""

import os
import shutil
import zipfile
import sys
from pathlib import Path

def create_deployment_package():
    """Create AWS Lambda deployment package with TinyAI integration"""
    
    print("🚀 BEA Pumpkin Pi TinyAI - Deployment Package Creator")
    print("=" * 55)
    
    # Get current directory
    current_dir = Path(__file__).parent
    lambda_dir = current_dir / "lambda"
    deploy_dir = current_dir / "lambda-deploy-tinyai"
    
    # Create deployment directory
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    print(f"📁 Creating deployment package in: {deploy_dir}")
    
    # Required files for TinyAI deployment
    required_files = [
        "enhanced_lambda_function.py",
        "tiny_beatbox_engine.py",
        "bea_4d_audio_core.py",
        "bea_emotional_framework.py", 
        "echo_gaming_enhancer.py"
    ]
    
    # Copy required files
    copied_files = []
    missing_files = []
    
    for file_name in required_files:
        source_file = lambda_dir / file_name
        if source_file.exists():
            dest_file = deploy_dir / file_name
            shutil.copy2(source_file, dest_file)
            copied_files.append(file_name)
            print(f"  ✅ Copied: {file_name}")
        else:
            missing_files.append(file_name)
            print(f"  ❌ Missing: {file_name}")
    
    # Create requirements.txt for numpy
    requirements_content = """numpy>=1.21.0
scipy>=1.7.0"""
    
    with open(deploy_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)
    print(f"  ✅ Created: requirements.txt")
    
    # Create simple lambda_function.py that imports from enhanced
    lambda_wrapper = '''"""
AWS Lambda entry point for BEA Pumpkin Pi TinyAI
Imports and delegates to enhanced_lambda_function
"""

try:
    from enhanced_lambda_function import lambda_handler
except ImportError as e:
    print(f"Import error: {e}")
    
    def lambda_handler(event, context):
        """Fallback handler if enhanced function fails to import"""
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "BEA Pumpkin Pi is initializing. Please try again in a moment."
                },
                "shouldEndSession": True
            }
        }

# Export the handler
__all__ = ['lambda_handler']
'''
    
    with open(deploy_dir / "lambda_function.py", "w") as f:
        f.write(lambda_wrapper)
    print(f"  ✅ Created: lambda_function.py (wrapper)")
    
    # Create deployment info file
    deployment_info = f"""# BEA Pumpkin Pi TinyAI Deployment Package
Generated: {Path(__file__).stat().st_mtime}
Version: 1.3.0
Engine: ACTIVE_WITH_TINY_AI

## Files Included:
{chr(10).join(f"- {f}" for f in copied_files)}

## AWS Lambda Configuration:
- Runtime: Python 3.9
- Handler: lambda_function.lambda_handler
- Memory: 512 MB
- Timeout: 30 seconds

## Missing Files:
{chr(10).join(f"- {f}" for f in missing_files) if missing_files else "None"}

## Deployment Steps:
1. Install dependencies: pip install -r requirements.txt -t .
2. Create ZIP file with all contents
3. Upload to AWS Lambda
4. Configure handler: lambda_function.lambda_handler
"""
    
    with open(deploy_dir / "DEPLOYMENT_INFO.md", "w") as f:
        f.write(deployment_info)
    print(f"  ✅ Created: DEPLOYMENT_INFO.md")
    
    # Create ZIP file
    zip_path = current_dir / "bea-pumpkin-pi-tinyai-deploy.zip"
    
    print(f"\n📦 Creating deployment ZIP: {zip_path.name}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in deploy_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(deploy_dir)
                zipf.write(file_path, arc_name)
                print(f"  📄 Added to ZIP: {arc_name}")
    
    # Get ZIP file size
    zip_size = zip_path.stat().st_size / 1024  # KB
    
    print(f"\n✅ Deployment package created successfully!")
    print(f"📊 Package Statistics:")
    print(f"   Files copied: {len(copied_files)}")
    print(f"   ZIP file size: {zip_size:.1f} KB")
    print(f"   Missing files: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️  Missing Files Warning:")
        for file in missing_files:
            print(f"   - {file}")
        print("   The deployment may not include all features.")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Upload {zip_path.name} to AWS Lambda")
    print(f"   2. Set handler to: lambda_function.lambda_handler")
    print(f"   3. Configure memory: 512 MB")
    print(f"   4. Set timeout: 30 seconds")
    print(f"   5. Test with Alexa Skills Kit")
    
    print(f"\n🎯 AWS Lambda ARN Format:")
    print(f"   arn:aws:lambda:us-east-1:ACCOUNT:function:BEA-Pumpkin-Pi-TinyAI")
    
    return zip_path, copied_files, missing_files

def show_testing_commands():
    """Show commands for testing the deployed skill"""
    print(f"\n🧪 Testing Commands for Alexa Simulator:")
    print("=" * 45)
    
    test_commands = [
        '"Alexa, ask bea pumpkin pi for tiny ai status"',
        '"Alexa, ask bea pumpkin pi to start beatbox mode"',
        '"Alexa, ask bea pumpkin pi to recognize bass beatbox"',
        '"Alexa, ask bea pumpkin pi to enhance my audio"',
        '"Alexa, ask bea pumpkin pi to check performance"',
        '"Alexa, ask bea pumpkin pi to set emotion to focused"',
        '"Alexa, ask bea pumpkin pi to activate gaming mode"'
    ]
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"   {i}. {cmd}")
    
    print(f"\n✨ Expected TinyAI Response:")
    print(f'   "TinyAI engine status: READY. BEA TinyAI integration is')
    print(f'    fully operational with 8 active capabilities..."')

if __name__ == "__main__":
    try:
        zip_path, copied, missing = create_deployment_package()
        show_testing_commands()
        
        print(f"\n🎉 BEA Pumpkin Pi TinyAI deployment package ready!")
        print(f"   Deploy {zip_path.name} to AWS Lambda and test with Alexa! 🎤🤖")
        
    except Exception as e:
        print(f"\n❌ Error creating deployment package: {e}")
        sys.exit(1)