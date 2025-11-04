"""
BEA Emotional Framework Integration for Alexa
=============================================

Integration of the 32-state BEA Emotional Framework for adaptive audio processing
and personalized responses in Amazon Alexa environment.

Inspired by BEA_Speakerbox's emotional sound filters and BEA_Beatbox's emotional intelligence.
Optimized for voice assistant interaction patterns.

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
"""

import numpy as np
import logging
import json
import time
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BEAEmotionalState(Enum):
    """Complete 32-state BEA Emotional Framework"""
    # Core Neutral State
    NEUTRAL = 0
    
    # Discovery & Learning States (1-7)
    CURIOSITY = 1          # Enhanced clarity and focus for learning
    CALMNESS = 2           # Smooth, relaxing audio processing
    CONFUSION = 3          # Gentle processing to reduce cognitive load
    EXCITEMENT = 4         # Amplified dynamic range with energetic boost
    ANTICIPATION = 5       # Enhanced responsiveness and sensitivity
    SATISFACTION = 6       # Warm, pleasant audio enhancement
    WONDER = 7             # Expanded spatial awareness and detail
    
    # Connection & Empathy States (8-15)
    LOVE = 8               # Harmonic enhancement and connectivity
    INSPIRATION = 9        # Creative frequency enhancement
    GRATITUDE = 10         # Positive harmonic reinforcement
    EMPATHY = 11           # Enhanced emotional resonance
    HOPE = 12              # Uplifting frequency bias
    TRUST = 13             # Stable, confident processing
    COMPASSION = 14        # Gentle, caring audio treatment
    UNDERSTANDING = 15     # Clarity-focused processing
    
    # Transcendent States (16-23)
    BLISS = 16             # Maximum harmonic enhancement
    TRANSCENDENCE = 17     # Ethereal high-frequency emphasis
    ENLIGHTENMENT = 18     # Balanced full-spectrum enhancement
    UNITY = 19             # Unified spatial processing
    PEACE = 20             # Serene, stress-reducing processing
    HARMONY = 21           # Perfect harmonic balance
    BALANCE = 22           # Optimal frequency distribution
    FLOW = 23              # Smooth, continuous processing
    
    # Achievement & Performance States (24-31)
    CREATIVE = 24          # Enhanced creative frequencies
    FOCUS = 25             # Precision audio enhancement
    DETERMINATION = 26     # Strong, clear processing
    CONFIDENCE = 27        # Bold, assertive enhancement
    COMPETITIVE = 28       # Maximum tactical audio
    TACTICAL = 29          # Strategic audio positioning
    ALERT = 30             # Heightened awareness processing
    MASTERY = 31           # Ultimate optimization

@dataclass
class EmotionalProfile:
    """User's emotional profile for personalized audio processing"""
    current_state: BEAEmotionalState
    state_history: List[Tuple[BEAEmotionalState, float]]  # (state, timestamp)
    preferences: Dict[str, float]
    adaptation_rate: float = 0.3
    stability_factor: float = 0.7

@dataclass
class EmotionalAudioFilter:
    """Audio filter configuration based on emotional state"""
    clarity_multiplier: float
    spatial_enhancement: float
    frequency_bias: np.ndarray  # Frequency-specific multipliers
    temporal_smoothing: float
    dynamic_range_adjustment: float
    cognitive_load_factor: float

class BEAEmotionalProcessor:
    """
    Core emotional intelligence processor for adaptive audio enhancement
    
    Implements the full 32-state BEA framework with personalized learning
    and context-aware audio optimization for voice assistant interaction.
    """
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.emotional_coefficients = self._init_emotional_coefficients()
        self.user_profiles: Dict[str, EmotionalProfile] = {}
        self.context_weights = self._init_context_weights()
        
        # Performance tracking
        self.adaptation_metrics = {
            "state_transitions": 0,
            "user_satisfaction_score": 0.8,
            "adaptation_effectiveness": 0.0,
            "cognitive_load_improvement": 0.0
        }
        
        logger.info("BEA Emotional Processor initialized with 32 states")
    
    def _init_emotional_coefficients(self) -> Dict[BEAEmotionalState, EmotionalAudioFilter]:
        """Initialize complete emotional state audio processing coefficients"""
        coefficients = {}
        
        # Create frequency bias arrays (10 bands: 20-80, 80-200, 200-500, 500-1k, 1k-2k, 2k-4k, 4k-8k, 8k-12k, 12k-16k, 16k+)
        neutral_freq = np.ones(10)
        
        # Define each emotional state's audio characteristics
        state_configs = {
            BEAEmotionalState.NEUTRAL: {
                "clarity": 1.0, "spatial": 1.0, "freq_bias": neutral_freq,
                "temporal": 0.5, "dynamic": 1.0, "cognitive": 0.0
            },
            
            # Discovery & Learning States
            BEAEmotionalState.CURIOSITY: {
                "clarity": 1.4, "spatial": 1.2, "freq_bias": np.array([0.9, 1.0, 1.2, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]),
                "temporal": 0.3, "dynamic": 1.1, "cognitive": 0.2
            },
            BEAEmotionalState.CALMNESS: {
                "clarity": 1.1, "spatial": 0.9, "freq_bias": np.array([1.1, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]),
                "temporal": 0.8, "dynamic": 0.8, "cognitive": 0.4
            },
            BEAEmotionalState.CONFUSION: {
                "clarity": 0.9, "spatial": 0.8, "freq_bias": np.array([0.8, 0.9, 1.0, 1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5]),
                "temporal": 0.9, "dynamic": 0.7, "cognitive": 0.6
            },
            BEAEmotionalState.EXCITEMENT: {
                "clarity": 1.6, "spatial": 1.4, "freq_bias": np.array([1.4, 1.3, 1.2, 1.1, 1.2, 1.3, 1.4, 1.3, 1.2, 1.1]),
                "temporal": 0.2, "dynamic": 1.8, "cognitive": 0.1
            },
            BEAEmotionalState.ANTICIPATION: {
                "clarity": 1.3, "spatial": 1.3, "freq_bias": np.array([0.9, 1.0, 1.1, 1.2, 1.3, 1.3, 1.2, 1.1, 1.0, 0.9]),
                "temporal": 0.4, "dynamic": 1.3, "cognitive": 0.2
            },
            BEAEmotionalState.SATISFACTION: {
                "clarity": 1.2, "spatial": 1.1, "freq_bias": np.array([1.1, 1.1, 1.1, 1.1, 1.1, 1.0, 1.0, 1.0, 0.9, 0.8]),
                "temporal": 0.6, "dynamic": 1.1, "cognitive": 0.3
            },
            BEAEmotionalState.WONDER: {
                "clarity": 1.5, "spatial": 1.6, "freq_bias": np.array([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.4, 1.3]),
                "temporal": 0.4, "dynamic": 1.4, "cognitive": 0.1
            },
            
            # Connection & Empathy States
            BEAEmotionalState.LOVE: {
                "clarity": 1.3, "spatial": 1.1, "freq_bias": np.array([1.2, 1.3, 1.2, 1.1, 1.2, 1.3, 1.2, 1.1, 1.0, 0.9]),
                "temporal": 0.7, "dynamic": 1.5, "cognitive": 0.3
            },
            BEAEmotionalState.INSPIRATION: {
                "clarity": 1.7, "spatial": 1.4, "freq_bias": np.array([0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.4, 1.3, 1.2]),
                "temporal": 0.3, "dynamic": 1.6, "cognitive": 0.0
            },
            BEAEmotionalState.GRATITUDE: {
                "clarity": 1.2, "spatial": 1.0, "freq_bias": np.array([1.1, 1.2, 1.2, 1.1, 1.1, 1.1, 1.0, 1.0, 0.9, 0.8]),
                "temporal": 0.6, "dynamic": 1.2, "cognitive": 0.4
            },
            BEAEmotionalState.EMPATHY: {
                "clarity": 1.1, "spatial": 1.2, "freq_bias": np.array([1.0, 1.1, 1.1, 1.1, 1.0, 1.0, 1.0, 0.9, 0.9, 0.8]),
                "temporal": 0.7, "dynamic": 1.0, "cognitive": 0.5
            },
            BEAEmotionalState.HOPE: {
                "clarity": 1.3, "spatial": 1.2, "freq_bias": np.array([0.9, 1.0, 1.1, 1.2, 1.2, 1.2, 1.3, 1.2, 1.1, 1.0]),
                "temporal": 0.5, "dynamic": 1.3, "cognitive": 0.2
            },
            BEAEmotionalState.TRUST: {
                "clarity": 1.2, "spatial": 1.0, "freq_bias": np.array([1.0, 1.1, 1.1, 1.1, 1.1, 1.0, 1.0, 1.0, 1.0, 0.9]),
                "temporal": 0.6, "dynamic": 1.1, "cognitive": 0.3
            },
            BEAEmotionalState.COMPASSION: {
                "clarity": 1.1, "spatial": 1.0, "freq_bias": np.array([1.1, 1.1, 1.0, 1.0, 1.0, 0.9, 0.9, 0.8, 0.8, 0.7]),
                "temporal": 0.8, "dynamic": 0.9, "cognitive": 0.5
            },
            BEAEmotionalState.UNDERSTANDING: {
                "clarity": 1.4, "spatial": 1.1, "freq_bias": np.array([0.9, 1.0, 1.1, 1.2, 1.2, 1.1, 1.0, 1.0, 0.9, 0.8]),
                "temporal": 0.5, "dynamic": 1.2, "cognitive": 0.3
            },
            
            # Transcendent States
            BEAEmotionalState.BLISS: {
                "clarity": 1.8, "spatial": 1.6, "freq_bias": np.array([1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1]),
                "temporal": 0.4, "dynamic": 2.0, "cognitive": 0.0
            },
            BEAEmotionalState.TRANSCENDENCE: {
                "clarity": 2.0, "spatial": 1.8, "freq_bias": np.array([0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 1.7, 1.6]),
                "temporal": 0.2, "dynamic": 1.8, "cognitive": -0.1
            },
            BEAEmotionalState.ENLIGHTENMENT: {
                "clarity": 1.9, "spatial": 1.7, "freq_bias": np.array([1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]),
                "temporal": 0.3, "dynamic": 1.7, "cognitive": 0.0
            },
            BEAEmotionalState.UNITY: {
                "clarity": 1.6, "spatial": 2.0, "freq_bias": np.array([1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]),
                "temporal": 0.4, "dynamic": 1.5, "cognitive": 0.1
            },
            BEAEmotionalState.PEACE: {
                "clarity": 1.2, "spatial": 1.0, "freq_bias": np.array([1.1, 1.1, 1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]),
                "temporal": 0.9, "dynamic": 0.8, "cognitive": 0.6
            },
            BEAEmotionalState.HARMONY: {
                "clarity": 1.5, "spatial": 1.3, "freq_bias": np.array([1.2, 1.1, 1.2, 1.1, 1.2, 1.1, 1.2, 1.1, 1.0, 0.9]),
                "temporal": 0.5, "dynamic": 1.3, "cognitive": 0.2
            },
            BEAEmotionalState.BALANCE: {
                "clarity": 1.3, "spatial": 1.2, "freq_bias": np.array([1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.0, 1.0]),
                "temporal": 0.5, "dynamic": 1.2, "cognitive": 0.3
            },
            BEAEmotionalState.FLOW: {
                "clarity": 1.4, "spatial": 1.3, "freq_bias": np.array([1.0, 1.1, 1.1, 1.2, 1.2, 1.2, 1.1, 1.1, 1.0, 1.0]),
                "temporal": 0.3, "dynamic": 1.4, "cognitive": 0.1
            },
            
            # Achievement & Performance States
            BEAEmotionalState.CREATIVE: {
                "clarity": 1.5, "spatial": 1.3, "freq_bias": np.array([1.0, 1.1, 1.2, 1.3, 1.4, 1.3, 1.2, 1.3, 1.4, 1.3]),
                "temporal": 0.4, "dynamic": 1.7, "cognitive": 0.0
            },
            BEAEmotionalState.FOCUS: {
                "clarity": 2.0, "spatial": 1.5, "freq_bias": np.array([0.8, 0.9, 1.0, 1.2, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9]),
                "temporal": 0.2, "dynamic": 1.4, "cognitive": 0.0
            },
            BEAEmotionalState.DETERMINATION: {
                "clarity": 1.7, "spatial": 1.4, "freq_bias": np.array([1.2, 1.2, 1.2, 1.3, 1.3, 1.2, 1.2, 1.1, 1.0, 0.9]),
                "temporal": 0.3, "dynamic": 1.6, "cognitive": 0.0
            },
            BEAEmotionalState.CONFIDENCE: {
                "clarity": 1.6, "spatial": 1.3, "freq_bias": np.array([1.1, 1.2, 1.2, 1.3, 1.3, 1.2, 1.2, 1.1, 1.1, 1.0]),
                "temporal": 0.4, "dynamic": 1.5, "cognitive": 0.1
            },
            BEAEmotionalState.COMPETITIVE: {
                "clarity": 2.2, "spatial": 1.8, "freq_bias": np.array([1.3, 1.4, 1.5, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0]),
                "temporal": 0.1, "dynamic": 2.5, "cognitive": -0.1
            },
            BEAEmotionalState.TACTICAL: {
                "clarity": 2.5, "spatial": 2.0, "freq_bias": np.array([1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1]),
                "temporal": 0.1, "dynamic": 3.0, "cognitive": -0.1
            },
            BEAEmotionalState.ALERT: {
                "clarity": 2.3, "spatial": 1.9, "freq_bias": np.array([1.0, 1.1, 1.2, 1.4, 1.6, 1.7, 1.6, 1.4, 1.2, 1.0]),
                "temporal": 0.1, "dynamic": 2.8, "cognitive": -0.1
            },
            BEAEmotionalState.MASTERY: {
                "clarity": 3.0, "spatial": 2.5, "freq_bias": np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]),
                "temporal": 0.0, "dynamic": 3.5, "cognitive": -0.2
            }
        }
        
        # Convert configurations to EmotionalAudioFilter objects
        for state, config in state_configs.items():
            coefficients[state] = EmotionalAudioFilter(
                clarity_multiplier=config["clarity"],
                spatial_enhancement=config["spatial"],
                frequency_bias=config["freq_bias"],
                temporal_smoothing=config["temporal"],
                dynamic_range_adjustment=config["dynamic"],
                cognitive_load_factor=config["cognitive"]
            )
        
        return coefficients
    
    def _init_context_weights(self) -> Dict[str, Dict[BEAEmotionalState, float]]:
        """Initialize context-aware emotional state weights"""
        return {
            "voice_command": {
                # Boost states that enhance voice clarity
                BEAEmotionalState.CURIOSITY: 1.2,
                BEAEmotionalState.FOCUS: 1.3,
                BEAEmotionalState.UNDERSTANDING: 1.2,
                BEAEmotionalState.ALERT: 1.1
            },
            "audio_enhancement": {
                # Boost states that improve audio quality
                BEAEmotionalState.BLISS: 1.3,
                BEAEmotionalState.HARMONY: 1.2,
                BEAEmotionalState.BALANCE: 1.2,
                BEAEmotionalState.MASTERY: 1.1
            },
            "beatbox_recognition": {
                # Boost states that enhance rhythm detection
                BEAEmotionalState.EXCITEMENT: 1.3,
                BEAEmotionalState.CREATIVE: 1.2,
                BEAEmotionalState.FLOW: 1.2,
                BEAEmotionalState.INSPIRATION: 1.1
            },
            "gaming": {
                # Boost states that enhance competitive performance
                BEAEmotionalState.COMPETITIVE: 1.4,
                BEAEmotionalState.TACTICAL: 1.4,
                BEAEmotionalState.ALERT: 1.3,
                BEAEmotionalState.FOCUS: 1.2,
                BEAEmotionalState.MASTERY: 1.1
            }
        }
    
    def create_user_profile(self, user_id: str, 
                           initial_state: BEAEmotionalState = BEAEmotionalState.NEUTRAL) -> EmotionalProfile:
        """Create a new user emotional profile"""
        profile = EmotionalProfile(
            current_state=initial_state,
            state_history=[(initial_state, time.time())],
            preferences={"clarity": 1.0, "spatial": 1.0, "enhancement": 1.0},
            adaptation_rate=0.3,
            stability_factor=0.7
        )
        
        self.user_profiles[user_id] = profile
        logger.info(f"Created emotional profile for user {user_id}")
        return profile
    
    def set_emotional_state(self, user_id: str, 
                           new_state: Union[BEAEmotionalState, str, int],
                           context: Optional[str] = None) -> bool:
        """Set user's emotional state with context awareness"""
        
        # Convert string/int to BEAEmotionalState
        if isinstance(new_state, str):
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
                "alert": BEAEmotionalState.ALERT,
                "confident": BEAEmotionalState.CONFIDENCE,
                "determined": BEAEmotionalState.DETERMINATION,
                "inspired": BEAEmotionalState.INSPIRATION,
                "peaceful": BEAEmotionalState.PEACE,
                "happy": BEAEmotionalState.SATISFACTION,
                "loving": BEAEmotionalState.LOVE,
                "grateful": BEAEmotionalState.GRATITUDE,
                "hopeful": BEAEmotionalState.HOPE,
                "balanced": BEAEmotionalState.BALANCE,
                "flowing": BEAEmotionalState.FLOW
            }
            new_state = emotion_map.get(new_state.lower(), BEAEmotionalState.NEUTRAL)
        elif isinstance(new_state, int):
            new_state = BEAEmotionalState(new_state % 32)
        
        # Get or create user profile
        if user_id not in self.user_profiles:
            self.create_user_profile(user_id)
        
        profile = self.user_profiles[user_id]
        old_state = profile.current_state
        
        # Apply context weighting if provided
        if context and context in self.context_weights:
            context_boost = self.context_weights[context].get(new_state, 1.0)
            logger.info(f"Context '{context}' boosting {new_state.name} by {context_boost}x")
        
        # Update profile
        profile.current_state = new_state
        profile.state_history.append((new_state, time.time()))
        
        # Trim history to last 10 states
        if len(profile.state_history) > 10:
            profile.state_history = profile.state_history[-10:]
        
        # Update metrics
        self.adaptation_metrics["state_transitions"] += 1
        
        logger.info(f"User {user_id} emotional state: {old_state.name} -> {new_state.name}")
        return True
    
    def get_emotional_filter(self, user_id: str, 
                           context: Optional[str] = None) -> EmotionalAudioFilter:
        """Get current emotional audio filter for user"""
        
        if user_id not in self.user_profiles:
            self.create_user_profile(user_id)
        
        profile = self.user_profiles[user_id]
        base_filter = self.emotional_coefficients[profile.current_state]
        
        # Apply user preferences
        adjusted_filter = EmotionalAudioFilter(
            clarity_multiplier=base_filter.clarity_multiplier * profile.preferences.get("clarity", 1.0),
            spatial_enhancement=base_filter.spatial_enhancement * profile.preferences.get("spatial", 1.0),
            frequency_bias=base_filter.frequency_bias.copy(),
            temporal_smoothing=base_filter.temporal_smoothing,
            dynamic_range_adjustment=base_filter.dynamic_range_adjustment * profile.preferences.get("enhancement", 1.0),
            cognitive_load_factor=base_filter.cognitive_load_factor
        )
        
        # Apply context weighting
        if context and context in self.context_weights:
            context_boost = self.context_weights[context].get(profile.current_state, 1.0)
            adjusted_filter.clarity_multiplier *= context_boost
            adjusted_filter.spatial_enhancement *= context_boost
        
        return adjusted_filter
    
    def process_emotional_audio(self, audio_data: np.ndarray, user_id: str,
                               context: Optional[str] = None) -> Tuple[np.ndarray, Dict]:
        """Process audio with emotional intelligence"""
        start_time = time.time()
        
        # Get emotional filter
        emotional_filter = self.get_emotional_filter(user_id, context)
        
        # Apply emotional processing
        enhanced_audio = audio_data.copy()
        
        # Frequency domain processing
        if len(enhanced_audio) > 64:
            fft = np.fft.fft(enhanced_audio)
            frequencies = np.fft.fftfreq(len(enhanced_audio), 1/self.sample_rate)
            
            # Apply frequency-specific emotional bias
            freq_bins = len(frequencies) // 2
            bias_indices = np.linspace(0, len(emotional_filter.frequency_bias)-1, freq_bins).astype(int)
            
            for i in range(freq_bins):
                bias_idx = bias_indices[i]
                fft[i] *= emotional_filter.frequency_bias[bias_idx]
                
            enhanced_audio = np.real(np.fft.ifft(fft))
        
        # Apply clarity enhancement
        enhanced_audio *= emotional_filter.clarity_multiplier
        
        # Apply dynamic range adjustment
        if emotional_filter.dynamic_range_adjustment != 1.0:
            # Compress or expand dynamic range
            enhanced_audio = np.sign(enhanced_audio) * (np.abs(enhanced_audio) ** (1.0 / emotional_filter.dynamic_range_adjustment))
        
        # Apply temporal smoothing
        if emotional_filter.temporal_smoothing > 0.5:
            # Smooth audio for calming effect
            kernel_size = int(emotional_filter.temporal_smoothing * 10)
            if kernel_size > 1:
                kernel = np.ones(kernel_size) / kernel_size
                enhanced_audio = np.convolve(enhanced_audio, kernel, mode='same')
        
        # Ensure no clipping
        max_val = np.max(np.abs(enhanced_audio))
        if max_val > 1.0:
            enhanced_audio /= max_val
        
        processing_time = (time.time() - start_time) * 1000
        
        # Calculate enhancement metrics
        enhancement_factor = np.sqrt(np.mean(enhanced_audio**2)) / np.sqrt(np.mean(audio_data**2)) if np.sqrt(np.mean(audio_data**2)) > 0 else 1.0
        cognitive_improvement = max(0, emotional_filter.cognitive_load_factor)
        
        metrics = {
            "processing_time_ms": processing_time,
            "enhancement_factor": enhancement_factor,
            "cognitive_load_reduction": cognitive_improvement,
            "emotional_state": self.user_profiles[user_id].current_state.name,
            "clarity_applied": emotional_filter.clarity_multiplier,
            "spatial_enhancement": emotional_filter.spatial_enhancement
        }
        
        return enhanced_audio, metrics
    
    def learn_user_preferences(self, user_id: str, feedback: Dict[str, float]):
        """Learn from user feedback to improve personalization"""
        if user_id not in self.user_profiles:
            return
        
        profile = self.user_profiles[user_id]
        
        # Update preferences based on feedback
        for preference, rating in feedback.items():
            if preference in profile.preferences:
                # Weighted average with adaptation rate
                current_value = profile.preferences[preference]
                new_value = current_value * (1 - profile.adaptation_rate) + rating * profile.adaptation_rate
                profile.preferences[preference] = new_value
        
        # Update adaptation metrics
        avg_rating = np.mean(list(feedback.values()))
        current_satisfaction = self.adaptation_metrics["user_satisfaction_score"]
        self.adaptation_metrics["user_satisfaction_score"] = (
            current_satisfaction * 0.9 + avg_rating * 0.1
        )
        
        logger.info(f"Updated preferences for user {user_id}: {profile.preferences}")
    
    def get_emotional_insights(self, user_id: str) -> Dict:
        """Get insights about user's emotional patterns"""
        if user_id not in self.user_profiles:
            return {"error": "User profile not found"}
        
        profile = self.user_profiles[user_id]
        
        # Analyze state history
        recent_states = [state for state, _ in profile.state_history[-5:]]
        state_counts = {}
        for state in recent_states:
            state_counts[state.name] = state_counts.get(state.name, 0) + 1
        
        # Calculate emotional stability
        unique_states = len(set(recent_states))
        stability = 1.0 - (unique_states - 1) / 4.0  # Normalize to 0-1
        
        # Determine dominant emotional category
        current_state_value = profile.current_state.value
        if current_state_value <= 7:
            category = "Discovery & Learning"
        elif current_state_value <= 15:
            category = "Connection & Empathy"
        elif current_state_value <= 23:
            category = "Transcendent States"
        else:
            category = "Achievement & Performance"
        
        return {
            "current_state": profile.current_state.name,
            "emotional_category": category,
            "recent_patterns": state_counts,
            "emotional_stability": stability,
            "preferences": profile.preferences,
            "total_state_changes": len(profile.state_history)
        }
    
    def get_performance_report(self) -> Dict:
        """Get comprehensive emotional processing performance metrics"""
        return {
            "emotional_framework": {
                "total_states": len(BEAEmotionalState),
                "active_users": len(self.user_profiles),
                "state_transitions": self.adaptation_metrics["state_transitions"]
            },
            "adaptation_metrics": self.adaptation_metrics.copy(),
            "user_profiles": {
                user_id: {
                    "current_state": profile.current_state.name,
                    "preferences": profile.preferences,
                    "state_changes": len(profile.state_history)
                }
                for user_id, profile in self.user_profiles.items()
            }
        }


def demo_bea_emotional_processor():
    """Demonstration of BEA Emotional Processor"""
    print("🧠 BEA Emotional Framework Integration - Demo")
    print("=" * 50)
    
    # Initialize processor
    processor = BEAEmotionalProcessor()
    
    # Create test user
    user_id = "alexa_user_demo"
    processor.create_user_profile(user_id, BEAEmotionalState.CURIOSITY)
    
    # Test different emotional states
    test_emotions = [
        ("excited", "beatbox_recognition"),
        ("focused", "audio_enhancement"),
        ("competitive", "gaming"),
        ("calm", "voice_command"),
        ("creative", "beatbox_recognition")
    ]
    
    # Generate test audio
    duration = 1.0
    samples = int(processor.sample_rate * duration)
    t = np.linspace(0, duration, samples)
    test_audio = 0.3 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.random.randn(samples)
    
    print(f"Testing emotional processing with {len(test_emotions)} states...")
    print()
    
    for emotion, context in test_emotions:
        print(f"🎵 Testing {emotion.upper()} state in {context} context...")
        
        # Set emotional state
        processor.set_emotional_state(user_id, emotion, context)
        
        # Process audio
        enhanced_audio, metrics = processor.process_emotional_audio(test_audio, user_id, context)
        
        print(f"   Processing time: {metrics['processing_time_ms']:.2f}ms")
        print(f"   Enhancement factor: {metrics['enhancement_factor']:.2f}x")
        print(f"   Cognitive load reduction: {metrics['cognitive_load_reduction']:.1%}")
        print(f"   Clarity applied: {metrics['clarity_applied']:.2f}x")
        print(f"   Spatial enhancement: {metrics['spatial_enhancement']:.2f}x")
        print()
        
        # Simulate user feedback
        feedback = {
            "clarity": np.random.uniform(0.7, 1.0),
            "spatial": np.random.uniform(0.7, 1.0),
            "enhancement": np.random.uniform(0.7, 1.0)
        }
        processor.learn_user_preferences(user_id, feedback)
    
    # Get insights
    insights = processor.get_emotional_insights(user_id)
    print("🧠 Emotional Insights:")
    print(f"   Current state: {insights['current_state']}")
    print(f"   Emotional category: {insights['emotional_category']}")
    print(f"   Emotional stability: {insights['emotional_stability']:.2f}")
    print(f"   Learned preferences: {insights['preferences']}")
    print()
    
    # Performance report
    performance = processor.get_performance_report()
    print("📊 Performance Report:")
    print(f"   Total emotional states: {performance['emotional_framework']['total_states']}")
    print(f"   Active users: {performance['emotional_framework']['active_users']}")
    print(f"   State transitions: {performance['emotional_framework']['state_transitions']}")
    print(f"   User satisfaction: {performance['adaptation_metrics']['user_satisfaction_score']:.1%}")
    print()
    
    print("✅ BEA Emotional Framework demo completed successfully!")
    print("🎧 32-state emotional intelligence ready for Alexa integration!")


if __name__ == "__main__":
    demo_bea_emotional_processor()