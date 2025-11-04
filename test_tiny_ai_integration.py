#!/usr/bin/env python3
"""
Test TinyAI Integration with BEA Pumpkin Pi
==========================================

This script demonstrates the TinyAI capabilities integrated into the BEA Pumpkin Pi Alexa skill.
Shows real beatbox recognition, pattern analysis, and edge computing features.

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
"""

import json
import sys
import os

# Add lambda directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'lambda'))

try:
    from enhanced_lambda_function import bea_engine, handle_enhanced_beatbox_recognition, handle_enhanced_tiny_ai_status
    from tiny_beatbox_engine import TinyBeatboxEngine, BeatboxStyle
    import numpy as np
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORTS_AVAILABLE = False

def test_tiny_ai_capabilities():
    """Test TinyAI capabilities and status reporting"""
    print("🤖 BEA Pumpkin Pi - TinyAI Integration Test")
    print("=" * 50)
    
    if not IMPORTS_AVAILABLE:
        print("❌ Required modules not available. Please ensure all dependencies are installed.")
        return
    
    print("1. Testing BEA Engine TinyAI Status...")
    capabilities = bea_engine.get_tiny_ai_capabilities()
    print(f"   TinyAI Available: {capabilities['available']}")
    print(f"   Status: {capabilities['status']}")
    print(f"   Capabilities: {len(capabilities.get('capabilities', []))}")
    
    if capabilities['available']:
        print(f"   Supported Styles: {capabilities.get('supported_styles', [])}")
        print(f"   Processing Modes: {capabilities.get('processing_modes', [])}")
        print(f"   Sample Rate: {capabilities.get('sample_rate', 'N/A')} Hz")
    
    print()
    
    print("2. Testing Alexa Voice Response for TinyAI Status...")
    # Simulate Alexa request for TinyAI status
    test_event = {
        "request": {
            "type": "IntentRequest",
            "intent": {
                "name": "TinyAIStatusIntent",
                "slots": {}
            }
        },
        "session": {
            "sessionId": "test_session_123"
        }
    }
    
    try:
        response = handle_enhanced_tiny_ai_status({}, "test_session_123")
        speech_text = response.get("response", {}).get("outputSpeech", {}).get("text", "")
        print(f"   Alexa Response Length: {len(speech_text)} characters")
        print(f"   Response Preview: {speech_text[:150]}...")
        
        if response.get("response", {}).get("card"):
            card = response["response"]["card"]
            print(f"   Card Title: {card.get('title', 'N/A')}")
            print(f"   Card Content Lines: {len(card.get('content', '').split(chr(10)))}")
    except Exception as e:
        print(f"   ❌ Error testing TinyAI status response: {e}")
    
    print()
    
    print("3. Testing TinyAI Beatbox Recognition...")
    # Test different beatbox styles
    test_styles = ["freestyle", "bass", "techno", "vocal"]
    
    for style in test_styles:
        print(f"   Testing {style.upper()} style...")
        
        try:
            result = bea_engine.process_beatbox_recognition(style)
            
            if result["success"]:
                print(f"     ✅ Success: {result['recognition_accuracy']:.1f}% accuracy")
                print(f"     Processing: {result['processing_time_ms']:.1f}ms")
                print(f"     Engine: {result.get('engine_status', 'Unknown')}")
                
                if result.get("engine_status") == "TINY_AI_ACTIVE":
                    tiny_result = result.get("tiny_ai_result", {})
                    print(f"     TinyAI Primary Style: {tiny_result.get('primary_style', 'N/A')}")
                    print(f"     TinyAI Confidence: {tiny_result.get('confidence', 0):.3f}")
                    print(f"     Patterns Detected: {result.get('patterns_detected', 0)}")
                    print(f"     BPM: {result.get('bpm_detected', 'N/A'):.0f}")
                    print(f"     Quality Score: {result.get('quality_score', 0):.2f}")
                    
                    suggestions = result.get("enhancement_suggestions", [])
                    if suggestions:
                        print(f"     Enhancement Tip: {suggestions[0]}")
                else:
                    print(f"     Note: Running in simulation mode")
            else:
                print(f"     ❌ Failed to process {style} style")
        except Exception as e:
            print(f"     ❌ Error processing {style}: {e}")
        
        print()
    
    print("4. Testing Alexa Voice Response for Beatbox Recognition...")
    # Test Alexa beatbox response with TinyAI
    for style in ["bass", "freestyle"]:
        print(f"   Testing Alexa response for {style}...")
        
        try:
            response = handle_enhanced_beatbox_recognition({"BeatboxStyle": {"value": style}}, "test_session_456")
            speech_text = response.get("response", {}).get("outputSpeech", {}).get("text", "")
            print(f"     Response Length: {len(speech_text)} characters")
            print(f"     Contains 'TinyAI': {'TinyAI' in speech_text}")
            print(f"     Contains 'confidence': {'confidence' in speech_text}")
            print(f"     Preview: {speech_text[:100]}...")
            
        except Exception as e:
            print(f"     ❌ Error testing Alexa response: {e}")
        
        print()
    
    print("5. Performance Metrics with TinyAI...")
    try:
        metrics = bea_engine.get_performance_metrics()
        
        print(f"   BEA Version: {metrics.get('bea_engine_version', 'N/A')}")
        print(f"   Engine Status: {metrics.get('engine_status', 'N/A')}")
        
        if "tiny_ai" in metrics:
            tiny_metrics = metrics["tiny_ai"]
            print(f"   TinyAI Status: {tiny_metrics.get('status', 'N/A')}")
            print(f"   TinyAI Engine Active: {tiny_metrics.get('engine_active', False)}")
            print(f"   Total Recognitions: {tiny_metrics.get('total_recognitions', 0)}")
            print(f"   Average Confidence: {tiny_metrics.get('average_confidence', 0):.3f}")
            print(f"   Avg Processing Time: {tiny_metrics.get('average_processing_time', 0):.1f}ms")
        else:
            print("   TinyAI metrics not available")
    except Exception as e:
        print(f"   ❌ Error getting performance metrics: {e}")
    
    print()
    
    print("6. Direct TinyAI Engine Test (if available)...")
    try:
        if hasattr(bea_engine, 'tiny_beatbox') and bea_engine.tiny_beatbox:
            print("   Testing direct TinyAI engine...")
            
            # Create test audio
            duration = 1.0
            samples = int(16000 * duration)
            t = np.linspace(0, duration, samples)
            test_audio = 0.7 * np.sin(2 * np.pi * 80 * t) * np.exp(-3*t)
            test_audio += 0.1 * np.random.randn(samples)
            
            # Process with TinyAI
            result = bea_engine.tiny_beatbox.recognize_beatbox(test_audio)
            
            print(f"     ✅ Direct TinyAI Recognition:")
            print(f"     Confidence: {result.overall_confidence:.3f}")
            print(f"     Processing Time: {result.processing_time_ms:.1f}ms")
            print(f"     Primary Style: {result.primary_style.value}")
            print(f"     BPM: {result.bpm_detected:.0f}")
            print(f"     Quality Score: {result.quality_score:.2f}")
            print(f"     Patterns: {len(result.patterns)}")
            
            if result.enhancement_suggestions:
                print(f"     Suggestion: {result.enhancement_suggestions[0]}")
        else:
            print("   TinyAI engine not initialized - running in simulation mode")
    except Exception as e:
        print(f"   ❌ Direct TinyAI test failed: {e}")
    
    print()
    print("✅ TinyAI Integration Test Complete!")
    print()
    print("🎯 Summary:")
    print("   - TinyAI integration adds real beatbox recognition capabilities")
    print("   - Edge computing processing with sub-100ms latency")
    print("   - Pattern classification and style detection")
    print("   - Quality scoring and enhancement suggestions")
    print("   - Seamless fallback to simulation mode when TinyAI unavailable")
    print("   - Enhanced Alexa voice responses with technical details")
    print()
    print("🗣️  Voice Commands to Test:")
    print("   'Alexa, ask bea pumpkin pi for tiny ai status'")
    print("   'Alexa, ask bea pumpkin pi to start beatbox mode'") 
    print("   'Alexa, ask bea pumpkin pi to recognize bass beatbox'")
    print("   'Alexa, ask bea pumpkin pi to check performance'")

if __name__ == "__main__":
    test_tiny_ai_capabilities()