"""
Unit Tests for BEA Pumpkin Pi Components
========================================

Comprehensive test suite for all BEA components in the Pumpkin Pi Alexa skill.
Tests core functionality, integration, and performance requirements.

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
"""

import pytest
import numpy as np
import json
import time
from unittest.mock import Mock, patch, MagicMock

# Import components to test
try:
    from bea_4d_audio_core import (
        BEA4DAudioCore, ProcessingConfiguration, ProcessingMode, 
        BEAEmotionalState, SpatialPosition
    )
    from tiny_beatbox_engine import (
        TinyBeatboxEngine, BeatboxStyle, RecognitionMode,
        MicroFeatureExtractor, TinyBeatboxClassifier
    )
    from bea_emotional_framework import (
        BEAEmotionalProcessor, EmotionalProfile, EmotionalAudioFilter
    )
    from echo_gaming_enhancer import (
        EchoGamingEnhancer, GameType, GamingMode, GamingProfile
    )
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")
    print("Some tests may be skipped")

class TestBEA4DAudioCore:
    """Test suite for BEA 4D Audio Core"""
    
    def setup_method(self):
        """Setup for each test"""
        config = ProcessingConfiguration(
            mode=ProcessingMode.REAL_TIME,
            sample_rate=16000,
            enhancement_strength=2.0
        )
        self.audio_core = BEA4DAudioCore(config)
        
        # Test audio data
        duration = 0.5
        samples = int(self.audio_core.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        self.test_audio = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.random.randn(samples)
    
    def test_initialization(self):
        """Test proper initialization"""
        assert self.audio_core.sample_rate == 16000
        assert self.audio_core.config.mode == ProcessingMode.REAL_TIME
        assert len(self.audio_core.emotional_coefficients) == 32
        assert not self.audio_core.is_processing
    
    def test_add_listener(self):
        """Test adding listeners"""
        listener_pos = SpatialPosition(0, 1, 1.5, BEAEmotionalState.CURIOSITY)
        self.audio_core.add_listener("test_listener", listener_pos)
        
        assert "test_listener" in self.audio_core.listeners
        assert self.audio_core.listeners["test_listener"].emotional_state == BEAEmotionalState.CURIOSITY
    
    def test_add_audio_source(self):
        """Test adding audio sources"""
        source_pos = SpatialPosition(1, 0, 1.5, BEAEmotionalState.EXCITEMENT)
        self.audio_core.add_audio_source("test_source", source_pos, priority=8)
        
        assert "test_source" in self.audio_core.audio_sources
        assert self.audio_core.audio_sources["test_source"]["priority"] == 8
    
    def test_4d_spatial_processing(self):
        """Test 4D spatial audio processing"""
        source_pos = SpatialPosition(0, 1, 1.5, BEAEmotionalState.EXCITEMENT)
        listener_pos = SpatialPosition(0, 0, 1.5, BEAEmotionalState.CURIOSITY)
        
        result = self.audio_core.process_4d_spatial(self.test_audio, source_pos, listener_pos)
        
        assert result.enhanced_audio is not None
        assert len(result.enhanced_audio) == len(self.test_audio)
        assert result.processing_time_ms > 0
        assert result.enhancement_factor > 0
        assert 0 <= result.spatial_clarity <= 1
        assert 0 <= result.cognitive_load_reduction <= 1
    
    def test_emotional_state_setting(self):
        """Test emotional state management"""
        # Test string input
        self.audio_core.set_emotional_state("excited")
        
        # Test int input
        self.audio_core.set_emotional_state(4)
        
        # Test enum input
        self.audio_core.set_emotional_state(BEAEmotionalState.FOCUS)
        
        # Should have default listener created
        assert "default_listener" in self.audio_core.listeners
    
    def test_echo_dot_optimization(self):
        """Test Echo Dot specific optimizations"""
        original_sample_rate = self.audio_core.config.sample_rate
        original_buffer_size = self.audio_core.config.buffer_size
        
        self.audio_core.optimize_for_echo_dot()
        
        assert self.audio_core.config.sample_rate <= original_sample_rate
        assert self.audio_core.config.buffer_size <= original_buffer_size
        assert self.audio_core.config.max_latency_ms <= 100.0
    
    def test_performance_report(self):
        """Test performance reporting"""
        # Process some audio first
        source_pos = SpatialPosition(0, 1, 1.5, BEAEmotionalState.NEUTRAL)
        self.audio_core.process_4d_spatial(self.test_audio, source_pos)
        
        report = self.audio_core.get_performance_report()
        
        assert "processing_metrics" in report
        assert "configuration" in report
        assert "system_status" in report
        assert report["processing_metrics"]["total_processed_samples"] > 0


class TestTinyBeatboxEngine:
    """Test suite for Tiny Beatbox Engine"""
    
    def setup_method(self):
        """Setup for each test"""
        self.engine = TinyBeatboxEngine(sample_rate=16000)
        
        # Create test beatbox audio (kick pattern)
        duration = 1.0
        samples = int(self.engine.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        # Simulate kick drum with low frequency and decay
        self.kick_audio = 0.8 * np.sin(2 * np.pi * 60 * t) * np.exp(-t * 3)
        
        # Simulate snare with noise burst
        self.snare_audio = 0.6 * np.random.randn(samples) * (np.sin(4 * np.pi * t) > 0.8)
    
    def test_initialization(self):
        """Test proper initialization"""
        assert self.engine.sample_rate == 16000
        assert not self.engine.is_listening
        assert len(self.engine.recognition_buffer) == 0
        assert isinstance(self.engine.feature_extractor, MicroFeatureExtractor)
        assert isinstance(self.engine.classifier, TinyBeatboxClassifier)
    
    def test_start_stop_recognition(self):
        """Test starting and stopping recognition"""
        # Test starting
        success = self.engine.start_recognition("bass")
        assert success
        assert self.engine.is_listening
        
        # Test stopping
        self.engine.stop_recognition()
        assert not self.engine.is_listening
    
    def test_beatbox_recognition(self):
        """Test beatbox pattern recognition"""
        self.engine.start_recognition("classic")
        
        # Test kick recognition
        result = self.engine.recognize_beatbox(self.kick_audio)
        
        assert result.overall_confidence >= 0
        assert result.processing_time_ms > 0
        assert result.bpm_detected > 0
        assert isinstance(result.primary_style, BeatboxStyle)
        assert len(result.enhancement_suggestions) >= 0
    
    def test_feature_extraction(self):
        """Test micro feature extraction"""
        extractor = MicroFeatureExtractor(16000)
        features = extractor.extract_features(self.kick_audio)
        
        assert features.spectral_centroid > 0
        assert features.spectral_rolloff > 0
        assert features.spectral_bandwidth >= 0
        assert 0 <= features.zero_crossing_rate <= 1
        assert len(features.mfcc_coefficients) == 13
        assert features.energy > 0
        assert len(features.tempo_features) == 4
    
    def test_pattern_classification(self):
        """Test pattern classification"""
        classifier = TinyBeatboxClassifier()
        extractor = MicroFeatureExtractor(16000)
        
        # Extract features and classify
        features = extractor.extract_features(self.kick_audio)
        patterns = classifier.classify_pattern(features)
        
        assert isinstance(patterns, list)
        assert all(hasattr(p, 'pattern_type') for p in patterns)
        assert all(hasattr(p, 'confidence') for p in patterns)
        assert all(0 <= p.confidence <= 1 for p in patterns)
    
    def test_performance_report(self):
        """Test performance reporting"""
        # Process some audio first
        self.engine.start_recognition("modern")
        self.engine.recognize_beatbox(self.kick_audio)
        
        report = self.engine.get_performance_report()
        
        assert "recognition_metrics" in report
        assert "recent_results" in report
        assert "system_status" in report
        assert report["recognition_metrics"]["total_recognitions"] > 0


class TestBEAEmotionalFramework:
    """Test suite for BEA Emotional Framework"""
    
    def setup_method(self):
        """Setup for each test"""
        self.processor = BEAEmotionalProcessor(sample_rate=16000)
        self.user_id = "test_user"
        
        # Test audio
        duration = 0.5
        samples = int(self.processor.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        self.test_audio = 0.3 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.random.randn(samples)
    
    def test_initialization(self):
        """Test proper initialization"""
        assert len(self.processor.emotional_coefficients) == 32
        assert len(self.processor.user_profiles) == 0
        assert "voice_command" in self.processor.context_weights
    
    def test_user_profile_creation(self):
        """Test user profile management"""
        profile = self.processor.create_user_profile(self.user_id, BEAEmotionalState.CURIOSITY)
        
        assert profile.current_state == BEAEmotionalState.CURIOSITY
        assert len(profile.state_history) == 1
        assert self.user_id in self.processor.user_profiles
    
    def test_emotional_state_setting(self):
        """Test setting emotional states"""
        # Test string input
        success = self.processor.set_emotional_state(self.user_id, "excited")
        assert success
        
        # Test int input
        success = self.processor.set_emotional_state(self.user_id, 25)
        assert success
        
        # Test enum input
        success = self.processor.set_emotional_state(self.user_id, BEAEmotionalState.COMPETITIVE)
        assert success
        
        profile = self.processor.user_profiles[self.user_id]
        assert profile.current_state == BEAEmotionalState.COMPETITIVE
    
    def test_emotional_audio_processing(self):
        """Test emotional audio processing"""
        self.processor.create_user_profile(self.user_id, BEAEmotionalState.EXCITEMENT)
        
        enhanced_audio, metrics = self.processor.process_emotional_audio(
            self.test_audio, self.user_id, "audio_enhancement"
        )
        
        assert len(enhanced_audio) == len(self.test_audio)
        assert metrics["processing_time_ms"] > 0
        assert metrics["enhancement_factor"] > 0
        assert "emotional_state" in metrics
        assert "clarity_applied" in metrics
    
    def test_emotional_filter_retrieval(self):
        """Test emotional filter retrieval"""
        self.processor.create_user_profile(self.user_id, BEAEmotionalState.FOCUS)
        
        filter_obj = self.processor.get_emotional_filter(self.user_id, "gaming")
        
        assert isinstance(filter_obj, EmotionalAudioFilter)
        assert filter_obj.clarity_multiplier > 0
        assert filter_obj.spatial_enhancement > 0
        assert len(filter_obj.frequency_bias) == 10
    
    def test_user_preference_learning(self):
        """Test user preference learning"""
        self.processor.create_user_profile(self.user_id)
        
        feedback = {"clarity": 0.9, "spatial": 0.8, "enhancement": 0.85}
        self.processor.learn_user_preferences(self.user_id, feedback)
        
        profile = self.processor.user_profiles[self.user_id]
        # Preferences should be updated (weighted average)
        assert profile.preferences["clarity"] != 1.0
    
    def test_emotional_insights(self):
        """Test emotional pattern insights"""
        self.processor.create_user_profile(self.user_id, BEAEmotionalState.CREATIVE)
        self.processor.set_emotional_state(self.user_id, "focused")
        self.processor.set_emotional_state(self.user_id, "competitive")
        
        insights = self.processor.get_emotional_insights(self.user_id)
        
        assert "current_state" in insights
        assert "emotional_category" in insights
        assert "recent_patterns" in insights
        assert "emotional_stability" in insights
        assert 0 <= insights["emotional_stability"] <= 1


class TestEchoGamingEnhancer:
    """Test suite for Echo Gaming Enhancer"""
    
    def setup_method(self):
        """Setup for each test"""
        self.enhancer = EchoGamingEnhancer(sample_rate=16000)
        self.user_id = "test_gamer"
        
        # Test gaming audio (simulate FPS audio)
        duration = 1.0
        samples = int(self.enhancer.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        self.gaming_audio = (
            0.3 * np.sin(2 * np.pi * 2000 * t) * (np.sin(8 * np.pi * t) > 0.7) +  # Footsteps
            0.4 * np.sin(2 * np.pi * 4000 * t) * (np.sin(4 * np.pi * t) > 0.8) +  # Gunshots
            0.1 * np.random.randn(samples)  # Background noise
        )
    
    def test_initialization(self):
        """Test proper initialization"""
        assert self.enhancer.sample_rate == 16000
        assert not self.enhancer.is_gaming_active
        assert len(self.enhancer.game_optimizations) == len(GameType)
        assert len(self.enhancer.active_profiles) == 0
    
    def test_gaming_session_management(self):
        """Test gaming session start/stop"""
        # Start session
        session_id = self.enhancer.start_gaming_session(self.user_id, GameType.FPS, GamingMode.COMPETITIVE)
        
        assert session_id is not None
        assert self.enhancer.is_gaming_active
        assert session_id in self.enhancer.active_profiles
        
        # Stop session
        summary = self.enhancer.stop_gaming_session(session_id)
        
        assert "session_id" in summary
        assert "game_type" in summary
        assert not self.enhancer.is_gaming_active
        assert session_id not in self.enhancer.active_profiles
    
    def test_game_optimization(self):
        """Test game-specific audio optimization"""
        session_id = self.enhancer.start_gaming_session(self.user_id, GameType.FPS, GamingMode.COMPETITIVE)
        
        enhanced_audio, metrics = self.enhancer.optimize_for_game(session_id, self.gaming_audio)
        
        assert len(enhanced_audio) == len(self.gaming_audio)
        assert metrics["processing_time_ms"] > 0
        assert metrics["enhancement_factor"] > 0
        assert metrics["game_type"] == "fps"
        assert metrics["gaming_mode"] == "competitive"
        
        self.enhancer.stop_gaming_session(session_id)
    
    def test_enhancement_level_calculation(self):
        """Test enhancement level calculation"""
        level = self.enhancer._calculate_enhancement_level(GameType.COMPETITIVE, GamingMode.TOURNAMENT)
        assert level > 4.0  # Should be high for competitive + tournament
        
        level = self.enhancer._calculate_enhancement_level(GameType.RPG, GamingMode.CASUAL)
        assert level < 3.0  # Should be lower for RPG + casual
    
    def test_tactical_features(self):
        """Test tactical feature lists"""
        features = self.enhancer._get_tactical_features(GameType.FPS)
        assert len(features) > 0
        assert any("footstep" in f.lower() for f in features)
        
        features = self.enhancer._get_tactical_features(GameType.FIGHTING)
        assert any("frame" in f.lower() for f in features)
    
    def test_gaming_suggestions(self):
        """Test gaming optimization suggestions"""
        session_id = self.enhancer.start_gaming_session(self.user_id, GameType.TACTICAL, GamingMode.COMPETITIVE)
        
        suggestions = self.enhancer.get_gaming_suggestions(session_id)
        
        assert len(suggestions) > 0
        assert all(isinstance(s, str) for s in suggestions)
        
        self.enhancer.stop_gaming_session(session_id)
    
    def test_performance_report(self):
        """Test performance reporting"""
        # Create and end a session
        session_id = self.enhancer.start_gaming_session(self.user_id, GameType.FPS)
        time.sleep(0.1)  # Brief session
        self.enhancer.stop_gaming_session(session_id)
        
        report = self.enhancer.get_performance_report()
        
        assert "gaming_metrics" in report
        assert "active_sessions" in report
        assert "supported_game_types" in report
        assert report["gaming_metrics"]["total_gaming_sessions"] > 0


class TestIntegration:
    """Integration tests for component interaction"""
    
    def test_audio_core_emotional_integration(self):
        """Test integration between audio core and emotional framework"""
        # Initialize components
        config = ProcessingConfiguration(sample_rate=16000)
        audio_core = BEA4DAudioCore(config)
        emotional_processor = BEAEmotionalProcessor(16000)
        
        # Create user profile
        user_id = "integration_test"
        emotional_processor.create_user_profile(user_id, BEAEmotionalState.COMPETITIVE)
        
        # Set emotional state in audio core
        audio_core.set_emotional_state("competitive")
        
        # Test audio processing
        test_audio = np.random.randn(1000) * 0.3
        source_pos = SpatialPosition(0, 1, 1.5, BEAEmotionalState.COMPETITIVE)
        
        result = audio_core.process_4d_spatial(test_audio, source_pos)
        assert result.enhanced_audio is not None
    
    def test_beatbox_gaming_integration(self):
        """Test integration between beatbox engine and gaming enhancer"""
        # Initialize components
        beatbox_engine = TinyBeatboxEngine(16000)
        gaming_enhancer = EchoGamingEnhancer(16000)
        
        # Start rhythm game session
        session_id = gaming_enhancer.start_gaming_session("test_user", GameType.RHYTHM)
        beatbox_engine.start_recognition("techno")
        
        # Test audio that should work for both
        duration = 1.0
        samples = int(16000 * duration)
        t = np.linspace(0, duration, samples)
        rhythm_audio = 0.5 * np.sin(2 * np.pi * 440 * t) * (np.sin(8 * np.pi * t) > 0.5)
        
        # Process with both systems
        beatbox_result = beatbox_engine.recognize_beatbox(rhythm_audio)
        gaming_audio, gaming_metrics = gaming_enhancer.optimize_for_game(session_id, rhythm_audio)
        
        assert beatbox_result.overall_confidence >= 0
        assert len(gaming_audio) == len(rhythm_audio)
        
        # Cleanup
        beatbox_engine.stop_recognition()
        gaming_enhancer.stop_gaming_session(session_id)


@pytest.fixture
def sample_audio():
    """Fixture providing sample audio data"""
    duration = 0.5
    sample_rate = 16000
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples)
    return 0.3 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.random.randn(samples)


def test_performance_requirements(sample_audio):
    """Test that performance requirements are met"""
    # Audio processing should be under 100ms for real-time
    config = ProcessingConfiguration(mode=ProcessingMode.REAL_TIME)
    audio_core = BEA4DAudioCore(config)
    
    start_time = time.time()
    source_pos = SpatialPosition(0, 1, 1.5, BEAEmotionalState.NEUTRAL)
    result = audio_core.process_4d_spatial(sample_audio, source_pos)
    processing_time = (time.time() - start_time) * 1000
    
    assert processing_time < 100, f"Processing time {processing_time}ms exceeds 100ms requirement"
    assert result.processing_time_ms < 100, f"Reported processing time {result.processing_time_ms}ms exceeds requirement"


def test_memory_usage():
    """Test memory usage stays within reasonable bounds"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Initialize all components
    audio_core = BEA4DAudioCore()
    beatbox_engine = TinyBeatboxEngine()
    emotional_processor = BEAEmotionalProcessor()
    gaming_enhancer = EchoGamingEnhancer()
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    # Should not use more than 100MB additional memory
    assert memory_increase < 100, f"Memory usage increased by {memory_increase}MB, exceeds 100MB limit"


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])