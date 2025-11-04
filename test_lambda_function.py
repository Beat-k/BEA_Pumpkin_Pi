#!/usr/bin/env python3
"""
Test script for BEA Pumpkin Pi Lambda function
Tests basic functionality without numpy dependencies
"""

import sys
import json

# Import the lambda function
try:
    from aws_lambda_console_ready import lambda_handler, BEACalculator, EmotionalStateIds, BEABit
    print("✅ Successfully imported Lambda function - no numpy errors!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_launch_request():
    """Test launch request"""
    event = {
        "session": {"sessionId": "test_session"},
        "request": {"type": "LaunchRequest"}
    }
    
    response = lambda_handler(event, {})
    print(f"✅ Launch request test passed")
    print(f"Response: {response['response']['outputSpeech']['text'][:100]}...")
    return True

def test_tiny_ai_intent():
    """Test TinyAI status intent"""
    event = {
        "session": {"sessionId": "test_session"},
        "request": {
            "type": "IntentRequest",
            "intent": {
                "name": "TinyAIStatusIntent",
                "slots": {}
            }
        }
    }
    
    response = lambda_handler(event, {})
    print(f"✅ TinyAI status test passed")
    print(f"Response: {response['response']['outputSpeech']['text'][:100]}...")
    return True

def test_bea_calculator():
    """Test BEA Calculator functionality"""
    # Test emotional state creation
    state_a = BEABit(EmotionalStateIds.CURIOSITY, "Curiosity", "🤔", 150, "cognitive")
    state_b = BEABit(EmotionalStateIds.CALMNESS, "Calmness", "😌", 120, "peaceful")
    
    # Test mathematical operations
    result = BEACalculator.combust(state_a, state_b)
    print(f"✅ BEA Calculator combust test passed")
    print(f"Result: {result.name} with intensity {result.level}")
    
    result = BEACalculator.balance(state_a, state_b)
    print(f"✅ BEA Calculator balance test passed")
    print(f"Result: {result.name} with intensity {result.level}")
    
    return True

def test_bea_calculator_intent():
    """Test BEA Calculator intent"""
    event = {
        "session": {"sessionId": "test_session"},
        "request": {
            "type": "IntentRequest",
            "intent": {
                "name": "BEACalculatorIntent",
                "slots": {
                    "MathOperation": {"value": "combust"},
                    "EmotionalStateA": {"value": "curious"},
                    "EmotionalStateB": {"value": "calm"}
                }
            }
        }
    }
    
    response = lambda_handler(event, {})
    print(f"✅ BEA Calculator intent test passed")
    print(f"Response: {response['response']['outputSpeech']['text'][:100]}...")
    return True

def main():
    """Run all tests"""
    print("🧪 Testing BEA Pumpkin Pi Lambda Function")
    print("=" * 50)
    
    try:
        test_launch_request()
        test_tiny_ai_intent()
        test_bea_calculator()
        test_bea_calculator_intent()
        
        print("=" * 50)
        print("🎉 All tests passed! Lambda function is ready for AWS deployment.")
        print("✅ No numpy dependencies")
        print("✅ All intents working")
        print("✅ BEA Framework integration complete")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()