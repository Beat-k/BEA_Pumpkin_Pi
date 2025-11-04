"""
BEA 4D Audio Core for Amazon Alexa
==================================

Core 4D audio processing engine adapted from BEA_Speakerbox for Echo Dot hardware constraints.
Provides real-time spatial audio processing with emotional intelligence integration.

Inspired by BEA_Speakerbox's 4D_Sound_Architecture.py
Optimized for Alexa Skills Kit cloud infrastructure.

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
"""

import numpy as np
import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum
import json
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessingMode(Enum):
    """Audio processing modes optimized for different use cases"""
    REAL_TIME = "real_time"          # <100ms latency for voice commands
    HIGH_QUALITY = "high_quality"    # Maximum enhancement quality
    GAMING = "gaming"                # Optimized for gaming audio
    BEATBOX = "beatbox"              # Specialized for beatbox recognition
    BACKGROUND = "background"        # Background sound enhancement
    COGNITIVE = "cognitive"          # Cognitive enhancement mode

class BEAEmotionalState(Enum):
    """32 BEA Emotional States (E[0] - E[31])"""
    NEUTRAL = 0
    CURIOSITY = 1
    CALMNESS = 2
    CONFUSION = 3
    EXCITEMENT = 4
    ANTICIPATION = 5
    SATISFACTION = 6
    WONDER = 7
    LOVE = 8
    INSPIRATION = 9
    GRATITUDE = 10
    EMPATHY = 11
    HOPE = 12
    TRUST = 13
    COMPASSION = 14
    UNDERSTANDING = 15
    BLISS = 16
    TRANSCENDENCE = 17
    ENLIGHTENMENT = 18
    UNITY = 19
    PEACE = 20
    HARMONY = 21
    BALANCE = 22
    FLOW = 23
    CREATIVE = 24
    FOCUS = 25
    DETERMINATION = 26
    CONFIDENCE = 27
    COMPETITIVE = 28
    TACTICAL = 29
    ALERT = 30
    MASTERY = 31

@dataclass
class SpatialPosition:
    """4D spatial position with emotional intelligence"""
    x: float = 0.0      # Left(-) to Right(+)
    y: float = 0.0      # Back(-) to Front(+) 
    z: float = 1.5      # Down(-) to Up(+)
    emotional_state: Union[BEAEmotionalState, int] = BEAEmotionalState.NEUTRAL
    
    def __post_init__(self):
        if isinstance(self.emotional_state, int):
            self.emotional_state = BEAEmotionalState(self.emotional_state % 32)

@dataclass
class AudioEnhancementResult:
    """Result of 4D audio processing"""
    enhanced_audio: np.ndarray
    spatial_clarity: float
    emotional_enhancement: float
    processing_time_ms: float
    enhancement_factor: float
    cognitive_load_reduction: float

@dataclass
class ProcessingConfiguration:
    """Configuration for BEA 4D audio processing"""
    mode: ProcessingMode = ProcessingMode.REAL_TIME
    sample_rate: int = 16000  # Echo Dot optimized
    buffer_size: int = 1024
    enhancement_strength: float = 2.0
    spatial_accuracy: float = 1.0
    emotional_processing: bool = True
    cognitive_enhancement: bool = True
    background_enhancement: bool = True
    max_latency_ms: float = 100.0

class BEA4DAudioCore:
    """
    Core 4D Audio Processing Engine for Amazon Alexa
    
    Adapted from BEA_Speakerbox architecture for cloud-native deployment.
    Provides real-time spatial audio enhancement with emotional intelligence.
    """
    
    def __init__(self, config: Optional[ProcessingConfiguration] = None):
        """Initialize the BEA 4D Audio Core"""
        self.config = config or ProcessingConfiguration()
        self.sample_rate = self.config.sample_rate
        self.is_processing = False
        self.listeners: Dict[str, SpatialPosition] = {}
        self.audio_sources: Dict[str, Dict] = {}
        self.performance_metrics = {
            "total_processed_samples": 0,
            "average_latency_ms": 0,
            "enhancement_effectiveness": 0,
            "cognitive_load_reduction": 0
        }
        
        # Initialize BEA emotional framework
        self._init_emotional_framework()
        
        # Initialize spatial processing matrices
        self._init_spatial_processing()
        
        logger.info("BEA 4D Audio Core initialized for Alexa")

    def _init_emotional_framework(self):
        """Initialize the 32-state BEA emotional framework"""
        self.emotional_coefficients = {
            # Core emotional states with audio processing coefficients
            BEAEmotionalState.NEUTRAL: {"clarity": 1.0, "spatial": 1.0, "enhancement": 1.0},
            BEAEmotionalState.CURIOSITY: {"clarity": 1.4, "spatial": 1.2, "enhancement": 1.1},
            BEAEmotionalState.CALMNESS: {"clarity": 1.1, "spatial": 0.9, "enhancement": 1.3},
            BEAEmotionalState.EXCITEMENT: {"clarity": 1.6, "spatial": 1.4, "enhancement": 1.8},
            BEAEmotionalState.LOVE: {"clarity": 1.3, "spatial": 1.1, "enhancement": 1.5},
            BEAEmotionalState.BLISS: {"clarity": 1.8, "spatial": 1.6, "enhancement": 2.0},
            BEAEmotionalState.CREATIVE: {"clarity": 1.5, "spatial": 1.3, "enhancement": 1.7},
            BEAEmotionalState.FOCUS: {"clarity": 2.0, "spatial": 1.5, "enhancement": 1.4},
            BEAEmotionalState.COMPETITIVE: {"clarity": 2.2, "spatial": 1.8, "enhancement": 2.5},
            BEAEmotionalState.TACTICAL: {"clarity": 2.5, "spatial": 2.0, "enhancement": 3.0},
            BEAEmotionalState.ALERT: {"clarity": 2.3, "spatial": 1.9, "enhancement": 2.8},
            BEAEmotionalState.MASTERY: {"clarity": 3.0, "spatial": 2.5, "enhancement": 3.5}
        }
        
        # Fill in remaining states with interpolated values
        for state in BEAEmotionalState:
            if state not in self.emotional_coefficients:
                base_value = (state.value % 8) / 8.0 + 1.0
                self.emotional_coefficients[state] = {
                    "clarity": base_value * 1.2,
                    "spatial": base_value * 1.1,
                    "enhancement": base_value * 1.3
                }

    def _init_spatial_processing(self):
        """Initialize spatial audio processing matrices"""
        # HRTF-inspired processing for Echo Dot limitations
        self.spatial_filters = {
            "left": np.array([0.8, 1.0, 0.6]),
            "right": np.array([0.6, 1.0, 0.8]),
            "front": np.array([1.0, 1.2, 1.0]),
            "back": np.array([0.7, 0.8, 0.9]),
            "above": np.array([1.1, 0.9, 1.3]),
            "below": np.array([0.9, 1.1, 0.7])
        }

    def add_listener(self, listener_id: str, position: SpatialPosition):
        """Add a listener with 4D positioning"""
        self.listeners[listener_id] = position
        logger.info(f"Added listener {listener_id} at position {position}")

    def add_audio_source(self, source_id: str, position: SpatialPosition, 
                        priority: int = 5, is_background: bool = False):
        """Add an audio source with 4D positioning"""
        self.audio_sources[source_id] = {
            "position": position,
            "priority": priority,
            "is_background": is_background,
            "enhancement_factor": 1.0
        }
        logger.info(f"Added audio source {source_id} with priority {priority}")

    def process_4d_spatial(self, audio_data: np.ndarray, 
                          source_position: SpatialPosition,
                          listener_position: Optional[SpatialPosition] = None) -> AudioEnhancementResult:
        """
        Process audio with 4D spatial enhancement
        
        Args:
            audio_data: Input audio samples
            source_position: 4D position of audio source
            listener_position: 4D position of listener (optional)
            
        Returns:
            AudioEnhancementResult with enhanced audio and metrics
        """
        start_time = time.time()
        
        if listener_position is None:
            listener_position = list(self.listeners.values())[0] if self.listeners else SpatialPosition()
        
        # Apply emotional state processing
        emotional_coeffs = self.emotional_coefficients[source_position.emotional_state]
        
        # Calculate spatial positioning
        spatial_vector = self._calculate_spatial_vector(source_position, listener_position)
        
        # Apply 4D enhancement
        enhanced_audio = self._apply_4d_enhancement(
            audio_data, spatial_vector, emotional_coeffs
        )
        
        # Calculate cognitive enhancement
        cognitive_reduction = self._calculate_cognitive_enhancement(
            audio_data, enhanced_audio, emotional_coeffs
        )
        
        # Calculate metrics
        processing_time = (time.time() - start_time) * 1000
        enhancement_factor = np.mean(np.abs(enhanced_audio)) / np.mean(np.abs(audio_data))
        spatial_clarity = self._calculate_spatial_clarity(spatial_vector)
        emotional_enhancement = emotional_coeffs["enhancement"]
        
        # Update performance metrics
        self._update_performance_metrics(processing_time, enhancement_factor, cognitive_reduction)
        
        return AudioEnhancementResult(
            enhanced_audio=enhanced_audio,
            spatial_clarity=spatial_clarity,
            emotional_enhancement=emotional_enhancement,
            processing_time_ms=processing_time,
            enhancement_factor=enhancement_factor,
            cognitive_load_reduction=cognitive_reduction
        )

    def _calculate_spatial_vector(self, source_pos: SpatialPosition, 
                                 listener_pos: SpatialPosition) -> np.ndarray:
        """Calculate spatial positioning vector"""
        dx = source_pos.x - listener_pos.x
        dy = source_pos.y - listener_pos.y
        dz = source_pos.z - listener_pos.z
        
        # Normalize to unit sphere
        distance = np.sqrt(dx**2 + dy**2 + dz**2)
        if distance > 0:
            return np.array([dx/distance, dy/distance, dz/distance])
        return np.array([0, 1, 0])  # Default forward position

    def _apply_4d_enhancement(self, audio_data: np.ndarray, 
                             spatial_vector: np.ndarray,
                             emotional_coeffs: Dict[str, float]) -> np.ndarray:
        """Apply 4D spatial and emotional enhancement"""
        # Start with original audio
        enhanced = audio_data.copy()
        
        # Apply emotional enhancement
        clarity_boost = emotional_coeffs["clarity"]
        spatial_boost = emotional_coeffs["spatial"] 
        enhancement_boost = emotional_coeffs["enhancement"]
        
        # Frequency domain processing for clarity
        if len(enhanced) > 64:  # Minimum FFT size
            fft = np.fft.fft(enhanced)
            
            # Enhance based on emotional state
            frequencies = np.fft.fftfreq(len(enhanced), 1/self.sample_rate)
            
            # Apply frequency-specific enhancement
            for i, freq in enumerate(frequencies[:len(frequencies)//2]):
                if freq < 200:  # Bass enhancement
                    fft[i] *= enhancement_boost * 0.8
                elif freq < 2000:  # Mid-range clarity
                    fft[i] *= clarity_boost
                elif freq < 8000:  # High-frequency detail
                    fft[i] *= spatial_boost
                    
            enhanced = np.real(np.fft.ifft(fft))
        
        # Apply spatial positioning
        spatial_enhancement = np.dot(spatial_vector, [0.8, 1.0, 1.2])
        enhanced *= spatial_enhancement
        
        # Apply overall enhancement factor
        enhanced *= self.config.enhancement_strength
        
        # Ensure no clipping
        max_val = np.max(np.abs(enhanced))
        if max_val > 1.0:
            enhanced /= max_val
            
        return enhanced

    def _calculate_cognitive_enhancement(self, original: np.ndarray, 
                                       enhanced: np.ndarray,
                                       emotional_coeffs: Dict[str, float]) -> float:
        """Calculate cognitive load reduction factor"""
        # Measure signal clarity improvement
        original_rms = np.sqrt(np.mean(original**2))
        enhanced_rms = np.sqrt(np.mean(enhanced**2))
        
        clarity_improvement = enhanced_rms / original_rms if original_rms > 0 else 1.0
        
        # Factor in emotional coefficients
        emotional_factor = emotional_coeffs["clarity"] * 0.3
        
        # Calculate cognitive load reduction (0.0 to 1.0)
        cognitive_reduction = min(0.7, (clarity_improvement - 1.0) * 0.4 + emotional_factor)
        return max(0.0, cognitive_reduction)

    def _calculate_spatial_clarity(self, spatial_vector: np.ndarray) -> float:
        """Calculate spatial positioning clarity"""
        # Measure how well-defined the spatial position is
        magnitude = np.linalg.norm(spatial_vector)
        directional_clarity = magnitude * self.config.spatial_accuracy
        return min(1.0, directional_clarity)

    def _update_performance_metrics(self, processing_time: float, 
                                   enhancement_factor: float,
                                   cognitive_reduction: float):
        """Update running performance metrics"""
        self.performance_metrics["total_processed_samples"] += 1
        
        # Update moving average for latency
        current_avg = self.performance_metrics["average_latency_ms"]
        count = self.performance_metrics["total_processed_samples"]
        self.performance_metrics["average_latency_ms"] = (
            (current_avg * (count - 1) + processing_time) / count
        )
        
        # Update enhancement effectiveness
        self.performance_metrics["enhancement_effectiveness"] = (
            (self.performance_metrics["enhancement_effectiveness"] * (count - 1) + enhancement_factor) / count
        )
        
        # Update cognitive load reduction
        self.performance_metrics["cognitive_load_reduction"] = (
            (self.performance_metrics["cognitive_load_reduction"] * (count - 1) + cognitive_reduction) / count
        )

    def get_performance_report(self) -> Dict:
        """Get comprehensive performance metrics"""
        return {
            "processing_metrics": self.performance_metrics.copy(),
            "configuration": {
                "mode": self.config.mode.value,
                "sample_rate": self.config.sample_rate,
                "enhancement_strength": self.config.enhancement_strength,
                "max_latency_ms": self.config.max_latency_ms
            },
            "system_status": {
                "is_processing": self.is_processing,
                "active_listeners": len(self.listeners),
                "active_sources": len(self.audio_sources),
                "emotional_framework_loaded": len(self.emotional_coefficients) == 32
            }
        }

    def set_emotional_state(self, state: Union[BEAEmotionalState, int, str]):
        """Set emotional state for default processing"""
        if isinstance(state, str):
            # Map common voice commands to emotional states
            emotion_map = {
                "curious": BEAEmotionalState.CURIOSITY,
                "calm": BEAEmotionalState.CALMNESS,
                "excited": BEAEmotionalState.EXCITEMENT,
                "focused": BEAEmotionalState.FOCUS,
                "creative": BEAEmotionalState.CREATIVE,
                "competitive": BEAEmotionalState.COMPETITIVE,
                "tactical": BEAEmotionalState.TACTICAL,
                "relaxed": BEAEmotionalState.CALMNESS,
                "energetic": BEAEmotionalState.EXCITEMENT,
                "alert": BEAEmotionalState.ALERT
            }
            state = emotion_map.get(state.lower(), BEAEmotionalState.NEUTRAL)
        elif isinstance(state, int):
            state = BEAEmotionalState(state % 32)
            
        # Update default listener emotional state
        if "default_listener" not in self.listeners:
            self.add_listener("default_listener", SpatialPosition(emotional_state=state))
        else:
            self.listeners["default_listener"].emotional_state = state
            
        logger.info(f"Emotional state set to {state.name}")

    def optimize_for_echo_dot(self):
        """Optimize processing for Echo Dot hardware constraints"""
        # Reduce sample rate for better performance
        self.config.sample_rate = min(self.config.sample_rate, 16000)
        
        # Adjust buffer size for real-time processing
        self.config.buffer_size = min(self.config.buffer_size, 512)
        
        # Ensure latency stays under Echo Dot limits
        self.config.max_latency_ms = min(self.config.max_latency_ms, 100.0)
        
        logger.info("Optimized for Echo Dot hardware constraints")

    async def process_real_time_stream(self, audio_stream, callback):
        """Process real-time audio stream for Alexa integration"""
        self.is_processing = True
        
        try:
            async for audio_chunk in audio_stream:
                if not self.is_processing:
                    break
                    
                # Default spatial position
                default_position = SpatialPosition(
                    y=1.0,  # Front-facing
                    emotional_state=BEAEmotionalState.CURIOSITY
                )
                
                # Process chunk
                result = self.process_4d_spatial(audio_chunk, default_position)
                
                # Send to callback
                await callback(result)
                
                # Check latency constraints
                if result.processing_time_ms > self.config.max_latency_ms:
                    logger.warning(f"Processing latency exceeded: {result.processing_time_ms}ms")
                    
        except Exception as e:
            logger.error(f"Real-time processing error: {e}")
        finally:
            self.is_processing = False

    def stop_processing(self):
        """Stop real-time processing"""
        self.is_processing = False
        logger.info("BEA 4D Audio processing stopped")


def demo_bea_4d_audio_core():
    """Demonstration of BEA 4D Audio Core for Alexa"""
    print("🎵 BEA 4D Audio Core for Amazon Alexa - Demo")
    print("=" * 50)
    
    # Create configuration optimized for Echo Dot
    config = ProcessingConfiguration(
        mode=ProcessingMode.REAL_TIME,
        sample_rate=16000,
        enhancement_strength=2.5,
        emotional_processing=True,
        cognitive_enhancement=True
    )
    
    # Initialize audio core
    audio_core = BEA4DAudioCore(config)
    audio_core.optimize_for_echo_dot()
    
    # Add default listener with curiosity state
    listener_pos = SpatialPosition(0, 0, 1.5, BEAEmotionalState.CURIOSITY)
    audio_core.add_listener("echo_dot_user", listener_pos)
    
    # Test different emotional states
    test_emotions = [
        BEAEmotionalState.EXCITEMENT,
        BEAEmotionalState.FOCUS,
        BEAEmotionalState.COMPETITIVE,
        BEAEmotionalState.CREATIVE
    ]
    
    # Generate test audio (simulated voice/beatbox)
    duration = 1.0  # 1 second
    samples = int(config.sample_rate * duration)
    t = np.linspace(0, duration, samples)
    
    # Simulate complex audio with multiple frequencies
    test_audio = (
        0.3 * np.sin(2 * np.pi * 440 * t) +      # A4 note
        0.2 * np.sin(2 * np.pi * 880 * t) +      # A5 note  
        0.1 * np.sin(2 * np.pi * 220 * t) +      # A3 note
        0.05 * np.random.randn(samples)           # Noise
    )
    
    print(f"Testing with {len(test_emotions)} emotional states...")
    print()
    
    results = []
    for emotion in test_emotions:
        print(f"🧠 Testing {emotion.name} (E[{emotion.value}])...")
        
        # Create source position with current emotion
        source_pos = SpatialPosition(0, 1.0, 1.5, emotion)
        
        # Process audio
        result = audio_core.process_4d_spatial(test_audio, source_pos)
        results.append((emotion.name, result))
        
        print(f"   Processing time: {result.processing_time_ms:.2f}ms")
        print(f"   Enhancement factor: {result.enhancement_factor:.2f}x")
        print(f"   Spatial clarity: {result.spatial_clarity:.3f}")
        print(f"   Cognitive reduction: {result.cognitive_load_reduction:.1%}")
        print()
    
    # Performance report
    performance = audio_core.get_performance_report()
    print("📊 Performance Report:")
    print(f"   Average latency: {performance['processing_metrics']['average_latency_ms']:.2f}ms")
    print(f"   Enhancement effectiveness: {performance['processing_metrics']['enhancement_effectiveness']:.2f}x")
    print(f"   Cognitive load reduction: {performance['processing_metrics']['cognitive_load_reduction']:.1%}")
    print()
    
    # Test voice command emotional state setting
    print("🗣️ Testing voice command integration...")
    voice_commands = ["excited", "focused", "competitive", "calm"]
    
    for command in voice_commands:
        audio_core.set_emotional_state(command)
        print(f"   Voice command '{command}' -> Emotional state set")
    
    print()
    print("✅ BEA 4D Audio Core demo completed successfully!")
    print("🎧 Ready for Alexa Skills Kit integration!")


if __name__ == "__main__":
    demo_bea_4d_audio_core()