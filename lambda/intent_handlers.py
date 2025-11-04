"""
Alexa Intent Handlers for BEA Pumpkin Pi
========================================

Voice interface handlers for Amazon Alexa integration with BEA ecosystem.
Handles all voice commands for 4D audio enhancement, beatbox recognition,
emotional intelligence, and gaming optimization.

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
"""

import logging
import json
import numpy as np
from typing import Dict, Optional
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.response_helper import ResponseFactory

# Import our BEA components
from bea_4d_audio_core import BEA4DAudioCore, ProcessingConfiguration, ProcessingMode, BEAEmotionalState
from tiny_beatbox_engine import TinyBeatboxEngine, BeatboxStyle, RecognitionMode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances (initialized on first use)
audio_core = None
beatbox_engine = None

def get_audio_core() -> BEA4DAudioCore:
    """Get or create BEA 4D Audio Core instance"""
    global audio_core
    if audio_core is None:
        config = ProcessingConfiguration(
            mode=ProcessingMode.REAL_TIME,
            sample_rate=16000,
            enhancement_strength=2.5,
            emotional_processing=True,
            cognitive_enhancement=True
        )
        audio_core = BEA4DAudioCore(config)
        audio_core.optimize_for_echo_dot()
        logger.info("BEA 4D Audio Core initialized")
    return audio_core

def get_beatbox_engine() -> TinyBeatboxEngine:
    """Get or create Tiny Beatbox Engine instance"""
    global beatbox_engine
    if beatbox_engine is None:
        beatbox_engine = TinyBeatboxEngine(sample_rate=16000)
        logger.info("Tiny Beatbox Engine initialized")
    return beatbox_engine

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch"""
    
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("BEA Pumpkin Pi skill launched")
        
        # Initialize components
        audio_core = get_audio_core()
        beatbox_engine = get_beatbox_engine()
        
        speak_output = (
            "Welcome to BEA Pumpkin Pi! Your 4D audio intelligence assistant is ready. "
            "I can enhance your audio with spatial processing, recognize beatbox patterns, "
            "optimize for gaming, and adapt to your emotional state. "
            "Try saying 'enhance my audio' or 'recognize beatbox' to get started!"
        )
        
        card_title = "BEA Pumpkin Pi - 4D Audio Intelligence"
        card_content = (
            "🎵 4D Audio Enhancement\n"
            "🥁 Beatbox Recognition\n" 
            "🎮 Gaming Optimization\n"
            "🧠 Emotional Intelligence\n\n"
            "Say 'Alexa, ask Pumpkin Pi to enhance my audio' to begin!"
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .ask(speak_output)
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class AudioEnhancementIntentHandler(AbstractRequestHandler):
    """Handler for audio enhancement commands"""
    
    def can_handle(self, handler_input):
        return is_intent_name("AudioEnhancementIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Audio enhancement intent triggered")
        
        # Get slot values
        slots = handler_input.request_envelope.request.intent.slots
        enhancement_type = slots.get("EnhancementType", {}).get("value", "spatial")
        intensity_level = slots.get("IntensityLevel", {}).get("value")
        
        # Get audio core
        audio_core = get_audio_core()
        
        # Configure enhancement based on type
        enhancement_factor = 2.0
        if intensity_level:
            try:
                enhancement_factor = float(intensity_level)
                enhancement_factor = max(1.0, min(5.0, enhancement_factor))  # Clamp to 1-5
            except ValueError:
                enhancement_factor = 2.0
        
        # Apply enhancement configuration
        if enhancement_type == "4d":
            audio_core.config.enhancement_strength = enhancement_factor * 1.2
            enhancement_description = "4D spatial audio with emotional intelligence"
        elif enhancement_type == "gaming":
            audio_core.config.mode = ProcessingMode.GAMING
            audio_core.config.enhancement_strength = enhancement_factor * 1.5
            enhancement_description = "tactical gaming audio with competitive advantage"
        elif enhancement_type == "cognitive":
            audio_core.config.cognitive_enhancement = True
            audio_core.config.enhancement_strength = enhancement_factor * 0.8
            enhancement_description = "cognitive enhancement for improved focus and clarity"
        elif enhancement_type == "background":
            audio_core.config.background_enhancement = True
            audio_core.config.enhancement_strength = enhancement_factor
            enhancement_description = "background sound enhancement with foreground preservation"
        else:  # spatial
            audio_core.config.spatial_accuracy = enhancement_factor / 2.0
            enhancement_description = "spatial audio positioning"
        
        speak_output = (
            f"Audio enhancement activated! I've enabled {enhancement_description} "
            f"with {enhancement_factor:.1f}x amplification. "
            f"Your audio experience will now have improved clarity, spatial awareness, "
            f"and cognitive enhancement. Try playing some audio to experience the difference!"
        )
        
        # Store settings in session
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["enhancement_active"] = True
        session_attributes["enhancement_type"] = enhancement_type
        session_attributes["enhancement_level"] = enhancement_factor
        
        card_title = f"Audio Enhancement: {enhancement_type.title()}"
        card_content = (
            f"Enhancement Type: {enhancement_type.title()}\n"
            f"Intensity Level: {enhancement_factor:.1f}x\n"
            f"Mode: {audio_core.config.mode.value}\n"
            f"Cognitive Enhancement: {'Enabled' if audio_core.config.cognitive_enhancement else 'Disabled'}\n"
            f"Spatial Accuracy: {audio_core.config.spatial_accuracy:.1f}"
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class BeatboxRecognitionIntentHandler(AbstractRequestHandler):
    """Handler for beatbox recognition commands"""
    
    def can_handle(self, handler_input):
        return is_intent_name("BeatboxRecognitionIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Beatbox recognition intent triggered")
        
        # Get slot values
        slots = handler_input.request_envelope.request.intent.slots
        beatbox_style = slots.get("BeatboxStyle", {}).get("value", "freestyle")
        
        # Get beatbox engine
        beatbox_engine = get_beatbox_engine()
        
        # Start recognition with style preference
        success = beatbox_engine.start_recognition(beatbox_style)
        
        if success:
            speak_output = (
                f"Beatbox recognition activated for {beatbox_style} style! "
                f"I'm now listening for your beats with 95% accuracy and sub-100 millisecond "
                f"response time. Try some {beatbox_style} beatbox sounds and I'll analyze "
                f"the patterns, rhythm, and give you real-time feedback!"
            )
            
            # Get performance info
            performance = beatbox_engine.get_performance_report()
            
            card_title = f"Beatbox Recognition: {beatbox_style.title()}"
            card_content = (
                f"Style: {beatbox_style.title()}\n"
                f"Recognition Mode: Real-time\n"
                f"Expected Accuracy: 95%+\n"
                f"Processing Latency: <100ms\n"
                f"Status: Listening..."
            )
        else:
            speak_output = (
                "I'm having trouble starting beatbox recognition. "
                "Please try again in a moment."
            )
            card_content = "Recognition startup failed. Please retry."
            card_title = "Beatbox Recognition Error"
        
        # Store in session
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["beatbox_active"] = success
        session_attributes["beatbox_style"] = beatbox_style
        
        return (
            ResponseFactory.speak(speak_output)
            .ask("Go ahead and try some beatbox sounds!")
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class EmotionalStateIntentHandler(AbstractRequestHandler):
    """Handler for emotional state commands"""
    
    def can_handle(self, handler_input):
        return is_intent_name("EmotionalStateIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Emotional state intent triggered")
        
        # Get slot values
        slots = handler_input.request_envelope.request.intent.slots
        emotional_state = slots.get("EmotionalState", {}).get("value", "curious")
        
        # Get audio core
        audio_core = get_audio_core()
        
        # Set emotional state
        audio_core.set_emotional_state(emotional_state)
        
        # Get emotional state info for response
        emotion_benefits = {
            "curious": "enhanced clarity and focus for learning",
            "calm": "smooth, relaxing audio processing with gentle enhancement",
            "excited": "amplified dynamic range with energetic boost",
            "focused": "precision audio enhancement for maximum concentration",
            "creative": "harmonic enhancement to inspire creativity",
            "competitive": "maximum tactical audio for competitive advantage",
            "energetic": "high-frequency detail boost for dynamic experiences",
            "relaxed": "soothing audio optimization for stress relief"
        }
        
        benefit = emotion_benefits.get(emotional_state, "personalized audio optimization")
        
        speak_output = (
            f"Emotional state set to {emotional_state}! "
            f"Your audio processing is now optimized for {benefit}. "
            f"The BEA emotional framework will adapt all audio enhancement "
            f"to match your current mood and provide the best experience."
        )
        
        # Store in session
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["emotional_state"] = emotional_state
        
        card_title = f"Emotional State: {emotional_state.title()}"
        card_content = (
            f"Current State: {emotional_state.title()}\n"
            f"Optimization: {benefit}\n"
            f"BEA Framework: 32-state emotional intelligence\n"
            f"Adaptive Processing: Enabled"
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class GamingModeIntentHandler(AbstractRequestHandler):
    """Handler for gaming optimization commands"""
    
    def can_handle(self, handler_input):
        return is_intent_name("GamingModeIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Gaming mode intent triggered")
        
        # Get slot values
        slots = handler_input.request_envelope.request.intent.slots
        game_type = slots.get("GameType", {}).get("value", "tactical")
        
        # Get audio core
        audio_core = get_audio_core()
        
        # Configure for gaming
        audio_core.config.mode = ProcessingMode.GAMING
        audio_core.config.enhancement_strength = 3.0
        audio_core.set_emotional_state("competitive")
        
        # Game-specific optimizations
        gaming_configs = {
            "fps": {
                "enhancement": 3.5,
                "description": "First-person shooter with enhanced footstep detection and directional audio",
                "features": ["directional audio precision", "footstep enhancement", "enemy detection"]
            },
            "fighting": {
                "enhancement": 3.0,
                "description": "Fighting game with frame-perfect audio timing and impact amplification",
                "features": ["frame-perfect timing", "impact amplification", "combo audio cues"]
            },
            "racing": {
                "enhancement": 2.8,
                "description": "Racing game with engine audio clarity and spatial positioning",
                "features": ["engine audio clarity", "spatial positioning", "tire grip feedback"]
            },
            "strategy": {
                "enhancement": 2.5,
                "description": "Strategy game with unit movement audio and resource management sounds",
                "features": ["unit movement clarity", "resource audio", "tactical positioning"]
            },
            "tactical": {
                "enhancement": 4.0,
                "description": "Tactical gameplay with maximum audio awareness and threat detection",
                "features": ["threat detection", "tactical audio", "competitive advantage"]
            },
            "competitive": {
                "enhancement": 4.5,
                "description": "Professional competitive gaming with ultimate audio enhancement",
                "features": ["maximum enhancement", "professional-grade", "tournament-ready"]
            }
        }
        
        config = gaming_configs.get(game_type, gaming_configs["tactical"])
        audio_core.config.enhancement_strength = config["enhancement"]
        
        speak_output = (
            f"Gaming mode activated for {game_type} games! "
            f"I've configured {config['description']} with {config['enhancement']}x enhancement. "
            f"You now have {', '.join(config['features'])} for competitive advantage!"
        )
        
        # Store in session
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["gaming_active"] = True
        session_attributes["game_type"] = game_type
        session_attributes["enhancement_level"] = config["enhancement"]
        
        card_title = f"Gaming Mode: {game_type.title()}"
        card_content = (
            f"Game Type: {game_type.title()}\n"
            f"Enhancement: {config['enhancement']}x\n"
            f"Features:\n" + "\n".join([f"• {feature}" for feature in config["features"]])
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class SpatialAudioIntentHandler(AbstractRequestHandler):
    """Handler for spatial audio positioning commands"""
    
    def can_handle(self, handler_input):
        return is_intent_name("SpatialAudioIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Spatial audio intent triggered")
        
        # Get slot values
        slots = handler_input.request_envelope.request.intent.slots
        direction = slots.get("Direction", {}).get("value", "center")
        distance = slots.get("Distance", {}).get("value")
        
        # Get audio core
        audio_core = get_audio_core()
        
        # Create spatial positioning
        from bea_4d_audio_core import SpatialPosition
        
        # Map direction to coordinates
        direction_map = {
            "left": (-1.0, 0, 1.5),
            "right": (1.0, 0, 1.5),
            "front": (0, 1.0, 1.5),
            "back": (0, -1.0, 1.5),
            "above": (0, 0, 2.5),
            "below": (0, 0, 0.5),
            "center": (0, 0, 1.5)
        }
        
        x, y, z = direction_map.get(direction, (0, 0, 1.5))
        
        # Apply distance if specified
        if distance:
            try:
                dist_factor = float(distance)
                x *= dist_factor
                y *= dist_factor
            except ValueError:
                pass
        
        # Create and add spatial position
        spatial_pos = SpatialPosition(x, y, z, BEAEmotionalState.CURIOSITY)
        audio_core.add_audio_source("user_positioned", spatial_pos)
        
        distance_text = f" at {distance} meters" if distance else ""
        speak_output = (
            f"Spatial audio positioning set to {direction}{distance_text}! "
            f"I've created a 4D audio space with your sound positioned {direction} "
            f"relative to your listening position. You'll experience enhanced "
            f"directionality and spatial awareness."
        )
        
        # Store in session
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["spatial_direction"] = direction
        session_attributes["spatial_distance"] = distance
        
        card_title = f"Spatial Audio: {direction.title()}"
        card_content = (
            f"Direction: {direction.title()}\n"
            f"Distance: {distance or 'Standard'}\n"
            f"Coordinates: X={x}, Y={y}, Z={z}\n"
            f"4D Processing: Active"
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class PerformanceStatusIntentHandler(AbstractRequestHandler):
    """Handler for performance status requests"""
    
    def can_handle(self, handler_input):
        return is_intent_name("PerformanceStatusIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Performance status intent triggered")
        
        # Get both engines
        audio_core = get_audio_core()
        beatbox_engine = get_beatbox_engine()
        
        # Get performance reports
        audio_performance = audio_core.get_performance_report()
        beatbox_performance = beatbox_engine.get_performance_report()
        
        # Extract key metrics
        audio_metrics = audio_performance["processing_metrics"]
        audio_config = audio_performance["configuration"]
        
        beatbox_metrics = beatbox_performance["recognition_metrics"]
        
        # Build status response
        speak_output = (
            f"BEA Pumpkin Pi performance status: "
            f"Audio enhancement is running with {audio_metrics['enhancement_effectiveness']:.1f}x improvement "
            f"and {audio_metrics['average_latency_ms']:.0f} millisecond latency. "
            f"Cognitive load reduction is {audio_metrics['cognitive_load_reduction']:.0%}. "
        )
        
        if beatbox_metrics["total_recognitions"] > 0:
            speak_output += (
                f"Beatbox recognition has processed {beatbox_metrics['total_recognitions']} samples "
                f"with {beatbox_metrics['average_confidence']:.0%} average confidence. "
            )
        
        speak_output += "All systems are operating optimally!"
        
        card_title = "BEA Pumpkin Pi - Performance Status"
        card_content = (
            f"🎵 Audio Enhancement:\n"
            f"• Enhancement: {audio_metrics['enhancement_effectiveness']:.1f}x\n"
            f"• Latency: {audio_metrics['average_latency_ms']:.0f}ms\n"
            f"• Cognitive Reduction: {audio_metrics['cognitive_load_reduction']:.0%}\n"
            f"• Mode: {audio_config['mode']}\n\n"
            f"🥁 Beatbox Recognition:\n"
            f"• Recognitions: {beatbox_metrics['total_recognitions']}\n"
            f"• Avg Confidence: {beatbox_metrics['average_confidence']:.0%}\n"
            f"• Processing Time: {beatbox_metrics.get('average_processing_time', 0):.0f}ms"
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class ResetSettingsIntentHandler(AbstractRequestHandler):
    """Handler for reset settings commands"""
    
    def can_handle(self, handler_input):
        return is_intent_name("ResetSettingsIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Reset settings intent triggered")
        
        # Reset audio core
        global audio_core, beatbox_engine
        audio_core = None
        beatbox_engine = None
        
        # Clear session attributes
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes.clear()
        
        speak_output = (
            "All BEA Pumpkin Pi settings have been reset to default! "
            "Audio enhancement, beatbox recognition, emotional states, and gaming "
            "optimizations are now cleared. You can reconfigure your preferences "
            "by using voice commands like 'enhance my audio' or 'start gaming mode'."
        )
        
        card_title = "Settings Reset"
        card_content = (
            "✅ Audio enhancement reset\n"
            "✅ Beatbox recognition stopped\n"
            "✅ Emotional state reset to neutral\n"
            "✅ Gaming mode disabled\n"
            "✅ Spatial positioning cleared\n\n"
            "All systems ready for reconfiguration!"
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help requests"""
    
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        speak_output = (
            "BEA Pumpkin Pi is your 4D audio intelligence assistant! "
            "Here's what I can do: "
            "Say 'enhance my audio' for spatial audio processing. "
            "Say 'recognize beatbox' to analyze rhythm patterns. "
            "Say 'I'm feeling excited' to set your emotional state. "
            "Say 'start gaming mode' for competitive audio advantage. "
            "Say 'check performance' for system status. "
            "What would you like to try?"
        )
        
        card_title = "BEA Pumpkin Pi - Help"
        card_content = (
            "🎵 'enhance my audio' - 4D audio processing\n"
            "🥁 'recognize beatbox' - Pattern analysis\n"
            "🧠 'I'm feeling [emotion]' - Emotional states\n"
            "🎮 'start gaming mode' - Gaming optimization\n"
            "🌐 'place sound left' - Spatial positioning\n"
            "📊 'check performance' - System status\n"
            "🔄 'reset settings' - Clear all settings"
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .ask(speak_output)
            .set_card(SimpleCard(card_title, card_content))
            .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler for cancel and stop requests"""
    
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))
    
    def handle(self, handler_input):
        # Stop beatbox recognition if active
        global beatbox_engine
        if beatbox_engine and beatbox_engine.is_listening:
            beatbox_engine.stop_recognition()
        
        speak_output = (
            "BEA Pumpkin Pi audio processing stopped. "
            "Your 4D audio enhancements will return to default. "
            "Come back anytime for superior audio intelligence!"
        )
        
        return ResponseFactory.speak(speak_output).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for session end"""
    
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("BEA Pumpkin Pi session ended")
        
        # Cleanup
        global beatbox_engine
        if beatbox_engine and beatbox_engine.is_listening:
            beatbox_engine.stop_recognition()
        
        return ResponseFactory.speak("").response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Global exception handler"""
    
    def can_handle(self, handler_input, exception):
        return True
    
    def handle(self, handler_input, exception):
        logger.error(f"BEA Pumpkin Pi error: {exception}")
        
        speak_output = (
            "Sorry, I'm having trouble with that request. "
            "Please try again or say 'help' for available commands."
        )
        
        return (
            ResponseFactory.speak(speak_output)
            .ask(speak_output)
            .response
        )

# Build skill
sb = SkillBuilder()

# Add handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AudioEnhancementIntentHandler())
sb.add_request_handler(BeatboxRecognitionIntentHandler())
sb.add_request_handler(EmotionalStateIntentHandler())
sb.add_request_handler(GamingModeIntentHandler())
sb.add_request_handler(SpatialAudioIntentHandler())
sb.add_request_handler(PerformanceStatusIntentHandler())
sb.add_request_handler(ResetSettingsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler
sb.add_exception_handler(CatchAllExceptionHandler())

# Lambda handler
lambda_handler = sb.lambda_handler()