"""
Tiny Beatbox Engine for Amazon Alexa
====================================

Lightweight beatbox recognition engine inspired by BEA_Beatbox's TinyAI integration.
Optimized for Alexa Skills Kit cloud infrastructure with sub-100ms inference.

Inspired by BEA_Beatbox's hybrid_bea_tinyai_system.py and edge_inference_engine.py
Adapted for voice assistant integration and cloud deployment.

© 2025 Jeremy F. Jackson dba BEATEK. All Rights Reserved.
"""

import numpy as np
import asyncio
import logging
import json
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum
import scipy.signal
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BeatboxStyle(Enum):
    """Beatbox style categories for recognition"""
    CLASSIC = "classic"
    MODERN = "modern"
    BASS = "bass"
    SNARE = "snare"
    VOCAL = "vocal"
    TECHNO = "techno"
    FREESTYLE = "freestyle"

class RecognitionMode(Enum):
    """Recognition processing modes"""
    REAL_TIME = "real_time"          # <100ms for voice commands
    HIGH_ACCURACY = "high_accuracy"  # Maximum recognition quality
    EDGE_OPTIMIZED = "edge_optimized" # Minimal resource usage
    HYBRID_ENSEMBLE = "hybrid_ensemble" # Multiple methods combined

@dataclass
class BeatboxPattern:
    """Detected beatbox pattern structure"""
    pattern_type: str
    confidence: float
    timestamp: float
    duration: float
    frequency_range: Tuple[float, float]
    intensity: float
    style: BeatboxStyle

@dataclass
class RecognitionResult:
    """Beatbox recognition result with comprehensive metrics"""
    patterns: List[BeatboxPattern]
    overall_confidence: float
    processing_time_ms: float
    bpm_detected: Optional[float]
    primary_style: BeatboxStyle
    quality_score: float
    enhancement_suggestions: List[str]

@dataclass
class FeatureVector:
    """Lightweight feature representation for TinyAI processing"""
    spectral_centroid: float
    spectral_rolloff: float
    spectral_bandwidth: float
    zero_crossing_rate: float
    mfcc_coefficients: np.ndarray  # 13 coefficients
    energy: float
    tempo_features: np.ndarray  # 4 tempo-related features

class MicroFeatureExtractor:
    """
    Micro-sized feature extractor optimized for cloud deployment
    
    Inspired by BEA_Beatbox's micro_feature_extractor.py
    Designed for minimal memory footprint and fast processing
    """
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.hop_length = 512
        self.n_fft = 1024
        self.n_mfcc = 13
        
        # Pre-compute mel filter bank for efficiency
        self._init_mel_filters()
        
    def _init_mel_filters(self):
        """Initialize mel-scale filter bank"""
        n_mels = 26
        fmin = 0
        fmax = self.sample_rate // 2
        
        # Create mel-scale frequency points
        mel_f = np.linspace(self._hz_to_mel(fmin), self._hz_to_mel(fmax), n_mels + 2)
        hz_f = self._mel_to_hz(mel_f)
        
        # Convert to FFT bin indices
        bin_indices = np.floor((self.n_fft + 1) * hz_f / self.sample_rate).astype(int)
        
        # Create filter bank
        self.mel_filters = np.zeros((n_mels, self.n_fft // 2 + 1))
        for i in range(n_mels):
            left, center, right = bin_indices[i:i+3]
            
            # Triangular filter
            for j in range(left, center):
                if center > left:
                    self.mel_filters[i, j] = (j - left) / (center - left)
            for j in range(center, right):
                if right > center:
                    self.mel_filters[i, j] = (right - j) / (right - center)
    
    @staticmethod
    def _hz_to_mel(hz):
        """Convert Hz to mel scale"""
        return 2595 * np.log10(1 + hz / 700)
    
    @staticmethod
    def _mel_to_hz(mel):
        """Convert mel to Hz scale"""
        return 700 * (10**(mel / 2595) - 1)
    
    def extract_features(self, audio_data: np.ndarray) -> FeatureVector:
        """Extract lightweight features for beatbox recognition"""
        if len(audio_data) < self.n_fft:
            # Pad short audio
            audio_data = np.pad(audio_data, (0, self.n_fft - len(audio_data)))
        
        # Compute STFT
        f, t, stft = scipy.signal.stft(
            audio_data, 
            fs=self.sample_rate,
            window='hann',
            nperseg=self.n_fft,
            noverlap=self.n_fft//2
        )
        
        magnitude = np.abs(stft)
        power = magnitude ** 2
        
        # Spectral features
        spectral_centroid = self._compute_spectral_centroid(magnitude, f)
        spectral_rolloff = self._compute_spectral_rolloff(magnitude, f)
        spectral_bandwidth = self._compute_spectral_bandwidth(magnitude, f, spectral_centroid)
        
        # Time-domain features
        zero_crossing_rate = self._compute_zero_crossing_rate(audio_data)
        energy = np.mean(power)
        
        # MFCC computation
        mfcc_coefficients = self._compute_mfcc(magnitude)
        
        # Tempo features
        tempo_features = self._compute_tempo_features(audio_data)
        
        return FeatureVector(
            spectral_centroid=spectral_centroid,
            spectral_rolloff=spectral_rolloff,
            spectral_bandwidth=spectral_bandwidth,
            zero_crossing_rate=zero_crossing_rate,
            mfcc_coefficients=mfcc_coefficients,
            energy=energy,
            tempo_features=tempo_features
        )
    
    def _compute_spectral_centroid(self, magnitude: np.ndarray, frequencies: np.ndarray) -> float:
        """Compute spectral centroid (brightness measure)"""
        if magnitude.shape[1] == 0:
            return 0.0
        
        weighted_freq = np.sum(magnitude * frequencies[:, np.newaxis], axis=0)
        total_magnitude = np.sum(magnitude, axis=0)
        
        # Avoid division by zero
        centroid = np.divide(weighted_freq, total_magnitude, 
                           out=np.zeros_like(weighted_freq), where=total_magnitude!=0)
        
        return np.mean(centroid)
    
    def _compute_spectral_rolloff(self, magnitude: np.ndarray, frequencies: np.ndarray, 
                                 rolloff_threshold: float = 0.85) -> float:
        """Compute spectral rolloff (frequency below which 85% of energy exists)"""
        if magnitude.shape[1] == 0:
            return 0.0
        
        total_energy = np.sum(magnitude, axis=0)
        rolloff_energy = rolloff_threshold * total_energy
        
        cumulative_energy = np.cumsum(magnitude, axis=0)
        rolloff_indices = []
        
        for i in range(magnitude.shape[1]):
            if total_energy[i] > 0:
                idx = np.where(cumulative_energy[:, i] >= rolloff_energy[i])[0]
                if len(idx) > 0:
                    rolloff_indices.append(frequencies[idx[0]])
                else:
                    rolloff_indices.append(frequencies[-1])
            else:
                rolloff_indices.append(0.0)
        
        return np.mean(rolloff_indices)
    
    def _compute_spectral_bandwidth(self, magnitude: np.ndarray, frequencies: np.ndarray,
                                   centroid: float) -> float:
        """Compute spectral bandwidth (spread around centroid)"""
        if magnitude.shape[1] == 0:
            return 0.0
        
        # Compute weighted deviation from centroid
        freq_diff = frequencies[:, np.newaxis] - centroid
        weighted_deviation = np.sum(magnitude * (freq_diff ** 2), axis=0)
        total_magnitude = np.sum(magnitude, axis=0)
        
        # Avoid division by zero
        variance = np.divide(weighted_deviation, total_magnitude,
                           out=np.zeros_like(weighted_deviation), where=total_magnitude!=0)
        
        bandwidth = np.sqrt(np.mean(variance))
        return bandwidth
    
    def _compute_zero_crossing_rate(self, audio_data: np.ndarray) -> float:
        """Compute zero crossing rate (measure of noisiness)"""
        if len(audio_data) < 2:
            return 0.0
        
        # Sign changes indicate zero crossings
        signs = np.sign(audio_data)
        sign_changes = np.diff(signs) != 0
        zcr = np.sum(sign_changes) / len(audio_data)
        
        return zcr
    
    def _compute_mfcc(self, magnitude: np.ndarray) -> np.ndarray:
        """Compute Mel-Frequency Cepstral Coefficients"""
        if magnitude.shape[1] == 0:
            return np.zeros(self.n_mfcc)
        
        # Apply mel filter bank
        mel_spectrogram = np.dot(self.mel_filters, magnitude)
        
        # Convert to log scale (avoid log(0))
        log_mel = np.log(mel_spectrogram + 1e-10)
        
        # Apply DCT to get cepstral coefficients
        mfcc = scipy.fftpack.dct(log_mel, axis=0, norm='ortho')[:self.n_mfcc]
        
        # Return mean across time
        return np.mean(mfcc, axis=1) if mfcc.shape[1] > 0 else np.zeros(self.n_mfcc)
    
    def _compute_tempo_features(self, audio_data: np.ndarray) -> np.ndarray:
        """Compute tempo-related features for rhythm detection"""
        # Onset detection using spectral flux
        hop_length = self.hop_length
        n_frames = len(audio_data) // hop_length
        
        if n_frames < 2:
            return np.zeros(4)
        
        # Compute spectral flux (onset strength)
        onset_strength = []
        for i in range(1, n_frames):
            frame_start = i * hop_length
            frame_end = min(frame_start + self.n_fft, len(audio_data))
            frame = audio_data[frame_start:frame_end]
            
            if len(frame) < self.n_fft:
                frame = np.pad(frame, (0, self.n_fft - len(frame)))
            
            # Simple spectral flux (difference in spectral energy)
            spectrum = np.abs(np.fft.fft(frame))
            if i == 1:
                prev_spectrum = spectrum
                continue
            
            flux = np.sum(np.maximum(0, spectrum - prev_spectrum))
            onset_strength.append(flux)
            prev_spectrum = spectrum
        
        onset_strength = np.array(onset_strength)
        
        # Tempo features
        tempo_mean = np.mean(onset_strength)
        tempo_std = np.std(onset_strength)
        tempo_max = np.max(onset_strength) if len(onset_strength) > 0 else 0
        tempo_rhythm = self._estimate_periodicity(onset_strength)
        
        return np.array([tempo_mean, tempo_std, tempo_max, tempo_rhythm])
    
    def _estimate_periodicity(self, onset_strength: np.ndarray) -> float:
        """Estimate rhythmic periodicity"""
        if len(onset_strength) < 4:
            return 0.0
        
        # Simple autocorrelation for periodicity
        autocorr = np.correlate(onset_strength, onset_strength, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Find prominent peaks (excluding zero lag)
        if len(autocorr) > 1:
            peak_strength = np.max(autocorr[1:]) / autocorr[0] if autocorr[0] > 0 else 0
            return peak_strength
        
        return 0.0

class TinyBeatboxClassifier:
    """
    Ultra-lightweight beatbox classifier for cloud deployment
    
    Inspired by BEA_Beatbox's tiny_neural_networks.py
    Uses simple but effective classification algorithms
    """
    
    def __init__(self):
        self.pattern_templates = self._init_pattern_templates()
        self.style_classifiers = self._init_style_classifiers()
        
    def _init_pattern_templates(self) -> Dict[str, Dict]:
        """Initialize beatbox pattern templates"""
        return {
            "kick": {
                "spectral_centroid_range": (50, 200),
                "energy_threshold": 0.7,
                "zero_crossing_rate": (0.02, 0.15),
                "mfcc_signature": np.array([0.5, -0.2, 0.1, -0.1, 0.05, 0, 0, 0, 0, 0, 0, 0, 0])
            },
            "snare": {
                "spectral_centroid_range": (1000, 4000),
                "energy_threshold": 0.6,
                "zero_crossing_rate": (0.15, 0.4),
                "mfcc_signature": np.array([0.3, 0.2, -0.1, 0.15, -0.05, 0.1, 0, 0, 0, 0, 0, 0, 0])
            },
            "hihat": {
                "spectral_centroid_range": (4000, 8000),
                "energy_threshold": 0.3,
                "zero_crossing_rate": (0.3, 0.7),
                "mfcc_signature": np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0, 0, 0, 0, 0, 0])
            },
            "bass": {
                "spectral_centroid_range": (20, 150),
                "energy_threshold": 0.8,
                "zero_crossing_rate": (0.01, 0.1),
                "mfcc_signature": np.array([0.7, -0.3, 0.2, -0.15, 0.1, -0.05, 0, 0, 0, 0, 0, 0, 0])
            },
            "vocal": {
                "spectral_centroid_range": (200, 2000),
                "energy_threshold": 0.5,
                "zero_crossing_rate": (0.05, 0.25),
                "mfcc_signature": np.array([0.4, 0.1, 0.1, 0.05, 0.05, 0.05, 0.02, 0.02, 0, 0, 0, 0, 0])
            }
        }
    
    def _init_style_classifiers(self) -> Dict[BeatboxStyle, Dict]:
        """Initialize style classification rules"""
        return {
            BeatboxStyle.CLASSIC: {
                "pattern_weights": {"kick": 0.4, "snare": 0.4, "hihat": 0.2},
                "tempo_range": (80, 120),
                "complexity_threshold": 0.3
            },
            BeatboxStyle.MODERN: {
                "pattern_weights": {"kick": 0.3, "snare": 0.3, "hihat": 0.2, "vocal": 0.2},
                "tempo_range": (100, 160),
                "complexity_threshold": 0.6
            },
            BeatboxStyle.BASS: {
                "pattern_weights": {"bass": 0.6, "kick": 0.3, "vocal": 0.1},
                "tempo_range": (60, 140),
                "complexity_threshold": 0.4
            },
            BeatboxStyle.TECHNO: {
                "pattern_weights": {"kick": 0.35, "snare": 0.25, "hihat": 0.4},
                "tempo_range": (120, 180),
                "complexity_threshold": 0.7
            },
            BeatboxStyle.VOCAL: {
                "pattern_weights": {"vocal": 0.7, "snare": 0.2, "hihat": 0.1},
                "tempo_range": (70, 130),
                "complexity_threshold": 0.5
            }
        }
    
    def classify_pattern(self, features: FeatureVector) -> List[BeatboxPattern]:
        """Classify beatbox patterns from feature vector"""
        patterns = []
        
        for pattern_name, template in self.pattern_templates.items():
            confidence = self._calculate_pattern_confidence(features, template)
            
            if confidence > 0.3:  # Confidence threshold
                pattern = BeatboxPattern(
                    pattern_type=pattern_name,
                    confidence=confidence,
                    timestamp=0.0,  # Will be set by caller
                    duration=0.5,   # Default duration
                    frequency_range=template["spectral_centroid_range"],
                    intensity=features.energy,
                    style=self._classify_style(features, pattern_name)
                )
                patterns.append(pattern)
        
        # Sort by confidence
        patterns.sort(key=lambda p: p.confidence, reverse=True)
        return patterns[:3]  # Return top 3 patterns
    
    def _calculate_pattern_confidence(self, features: FeatureVector, 
                                    template: Dict) -> float:
        """Calculate confidence score for pattern match"""
        confidence_components = []
        
        # Spectral centroid match
        if template["spectral_centroid_range"][0] <= features.spectral_centroid <= template["spectral_centroid_range"][1]:
            centroid_score = 1.0
        else:
            # Gradual falloff outside range
            center = np.mean(template["spectral_centroid_range"])
            deviation = abs(features.spectral_centroid - center) / center
            centroid_score = max(0, 1.0 - deviation)
        confidence_components.append(centroid_score * 0.3)
        
        # Energy match
        energy_score = min(1.0, features.energy / template["energy_threshold"])
        confidence_components.append(energy_score * 0.25)
        
        # Zero crossing rate match
        zcr_min, zcr_max = template["zero_crossing_rate"]
        if zcr_min <= features.zero_crossing_rate <= zcr_max:
            zcr_score = 1.0
        else:
            zcr_score = max(0, 1.0 - abs(features.zero_crossing_rate - np.mean([zcr_min, zcr_max])) / np.mean([zcr_min, zcr_max]))
        confidence_components.append(zcr_score * 0.2)
        
        # MFCC similarity
        mfcc_similarity = np.exp(-np.sum((features.mfcc_coefficients - template["mfcc_signature"])**2))
        confidence_components.append(mfcc_similarity * 0.25)
        
        return sum(confidence_components)
    
    def _classify_style(self, features: FeatureVector, dominant_pattern: str) -> BeatboxStyle:
        """Classify overall beatbox style"""
        style_scores = {}
        
        for style, classifier in self.style_classifiers.items():
            score = 0.0
            
            # Pattern weight contribution
            if dominant_pattern in classifier["pattern_weights"]:
                score += classifier["pattern_weights"][dominant_pattern]
            
            # Tempo estimation (simplified)
            estimated_tempo = self._estimate_tempo(features.tempo_features)
            tempo_min, tempo_max = classifier["tempo_range"]
            if tempo_min <= estimated_tempo <= tempo_max:
                score += 0.3
            
            # Complexity assessment
            complexity = np.std(features.mfcc_coefficients) + features.spectral_bandwidth / 1000
            if complexity >= classifier["complexity_threshold"]:
                score += 0.2
            
            style_scores[style] = score
        
        # Return style with highest score
        best_style = max(style_scores, key=style_scores.get)
        return best_style
    
    def _estimate_tempo(self, tempo_features: np.ndarray) -> float:
        """Estimate BPM from tempo features"""
        if len(tempo_features) < 4:
            return 120.0  # Default tempo
        
        # Simple tempo estimation based on rhythm detection
        periodicity = tempo_features[3]
        base_tempo = 120.0
        
        # Adjust based on rhythmic content
        if periodicity > 0.5:
            return base_tempo * 1.2  # Faster tempo
        elif periodicity < 0.2:
            return base_tempo * 0.8  # Slower tempo
        
        return base_tempo

class TinyBeatboxEngine:
    """
    Main beatbox recognition engine for Alexa integration
    
    Combines micro feature extraction with lightweight classification
    Optimized for real-time processing in cloud environment
    """
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.feature_extractor = MicroFeatureExtractor(sample_rate)
        self.classifier = TinyBeatboxClassifier()
        self.is_listening = False
        self.recognition_buffer = deque(maxlen=10)  # Store recent results
        
        # Performance tracking
        self.performance_metrics = {
            "total_recognitions": 0,
            "average_confidence": 0.0,
            "average_processing_time": 0.0,
            "pattern_distribution": {}
        }
        
        logger.info("Tiny Beatbox Engine initialized for Alexa")
    
    def start_recognition(self, style_preference: str = "freestyle") -> bool:
        """Start beatbox recognition with style preference"""
        self.is_listening = True
        self.style_preference = BeatboxStyle(style_preference.lower()) if style_preference != "freestyle" else None
        
        logger.info(f"Beatbox recognition started with {style_preference} preference")
        return True
    
    def stop_recognition(self):
        """Stop beatbox recognition"""
        self.is_listening = False
        logger.info("Beatbox recognition stopped")
    
    def recognize_beatbox(self, audio_data: np.ndarray, 
                         mode: RecognitionMode = RecognitionMode.REAL_TIME) -> RecognitionResult:
        """
        Recognize beatbox patterns in audio data
        
        Args:
            audio_data: Input audio samples
            mode: Recognition processing mode
            
        Returns:
            RecognitionResult with detected patterns and metrics
        """
        start_time = time.time()
        
        if not self.is_listening:
            self.start_recognition()
        
        # Extract features
        features = self.feature_extractor.extract_features(audio_data)
        
        # Classify patterns
        patterns = self.classifier.classify_pattern(features)
        
        # Calculate overall metrics
        overall_confidence = np.mean([p.confidence for p in patterns]) if patterns else 0.0
        processing_time = (time.time() - start_time) * 1000
        
        # Estimate BPM
        bpm_detected = self.classifier._estimate_tempo(features.tempo_features)
        
        # Determine primary style
        if patterns:
            primary_style = patterns[0].style
        else:
            primary_style = self.style_preference or BeatboxStyle.FREESTYLE
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(features, patterns)
        
        # Generate enhancement suggestions
        enhancement_suggestions = self._generate_enhancement_suggestions(features, patterns)
        
        # Create result
        result = RecognitionResult(
            patterns=patterns,
            overall_confidence=overall_confidence,
            processing_time_ms=processing_time,
            bpm_detected=bpm_detected,
            primary_style=primary_style,
            quality_score=quality_score,
            enhancement_suggestions=enhancement_suggestions
        )
        
        # Update metrics and buffer
        self._update_performance_metrics(result)
        self.recognition_buffer.append(result)
        
        return result
    
    def _calculate_quality_score(self, features: FeatureVector, 
                               patterns: List[BeatboxPattern]) -> float:
        """Calculate overall quality score of beatbox performance"""
        score_components = []
        
        # Pattern clarity (higher is better)
        if patterns:
            max_confidence = max(p.confidence for p in patterns)
            score_components.append(max_confidence * 0.4)
        else:
            score_components.append(0.0)
        
        # Spectral richness
        spectral_richness = min(1.0, features.spectral_bandwidth / 2000)
        score_components.append(spectral_richness * 0.3)
        
        # Energy consistency  
        energy_score = min(1.0, features.energy)
        score_components.append(energy_score * 0.2)
        
        # Rhythmic content
        rhythm_score = features.tempo_features[3] if len(features.tempo_features) > 3 else 0
        score_components.append(rhythm_score * 0.1)
        
        return sum(score_components)
    
    def _generate_enhancement_suggestions(self, features: FeatureVector,
                                        patterns: List[BeatboxPattern]) -> List[str]:
        """Generate suggestions for improving beatbox performance"""
        suggestions = []
        
        # Low confidence patterns
        if patterns and max(p.confidence for p in patterns) < 0.6:
            suggestions.append("Try to make your beats more distinct and pronounced")
        
        # Low energy
        if features.energy < 0.3:
            suggestions.append("Increase the volume and intensity of your beatbox")
        
        # Limited frequency range
        if features.spectral_rolloff < 2000:
            suggestions.append("Add more high-frequency elements like hi-hats or snares")
        
        # Monotone (low spectral bandwidth)
        if features.spectral_bandwidth < 500:
            suggestions.append("Try varying your sounds to add more complexity")
        
        # Low rhythmic content
        if len(features.tempo_features) > 3 and features.tempo_features[3] < 0.2:
            suggestions.append("Focus on creating stronger rhythmic patterns")
        
        # Style-specific suggestions
        if patterns:
            dominant_pattern = patterns[0].pattern_type
            if dominant_pattern == "kick" and len([p for p in patterns if p.pattern_type in ["snare", "hihat"]]) == 0:
                suggestions.append("Add snare or hi-hat sounds to complete the rhythm")
            elif dominant_pattern in ["snare", "hihat"] and len([p for p in patterns if p.pattern_type == "kick"]) == 0:
                suggestions.append("Add bass/kick sounds for a fuller beat")
        
        return suggestions
    
    def _update_performance_metrics(self, result: RecognitionResult):
        """Update running performance metrics"""
        self.performance_metrics["total_recognitions"] += 1
        count = self.performance_metrics["total_recognitions"]
        
        # Update average confidence
        current_avg_conf = self.performance_metrics["average_confidence"]
        self.performance_metrics["average_confidence"] = (
            (current_avg_conf * (count - 1) + result.overall_confidence) / count
        )
        
        # Update average processing time
        current_avg_time = self.performance_metrics["average_processing_time"]
        self.performance_metrics["average_processing_time"] = (
            (current_avg_time * (count - 1) + result.processing_time_ms) / count
        )
        
        # Update pattern distribution
        for pattern in result.patterns:
            pattern_type = pattern.pattern_type
            if pattern_type not in self.performance_metrics["pattern_distribution"]:
                self.performance_metrics["pattern_distribution"][pattern_type] = 0
            self.performance_metrics["pattern_distribution"][pattern_type] += 1
    
    def get_performance_report(self) -> Dict:
        """Get comprehensive performance metrics"""
        return {
            "recognition_metrics": self.performance_metrics.copy(),
            "recent_results": [
                {
                    "confidence": r.overall_confidence,
                    "processing_time_ms": r.processing_time_ms,
                    "patterns_detected": len(r.patterns),
                    "primary_style": r.primary_style.value,
                    "quality_score": r.quality_score
                }
                for r in list(self.recognition_buffer)[-5:]  # Last 5 results
            ],
            "system_status": {
                "is_listening": self.is_listening,
                "sample_rate": self.sample_rate,
                "buffer_size": len(self.recognition_buffer)
            }
        }
    
    async def process_real_time_audio(self, audio_stream, callback):
        """Process real-time audio stream for Alexa integration"""
        async for audio_chunk in audio_stream:
            if not self.is_listening:
                break
            
            try:
                result = self.recognize_beatbox(audio_chunk)
                await callback(result)
            except Exception as e:
                logger.error(f"Real-time recognition error: {e}")


def demo_tiny_beatbox_engine():
    """Demonstration of Tiny Beatbox Engine for Alexa"""
    print("🥁 Tiny Beatbox Engine for Amazon Alexa - Demo")
    print("=" * 50)
    
    # Initialize engine
    engine = TinyBeatboxEngine(sample_rate=16000)
    
    # Test with different styles
    test_styles = ["classic", "modern", "bass", "techno", "vocal"]
    
    print("Testing beatbox recognition with various styles...")
    print()
    
    for style in test_styles:
        print(f"🎵 Testing {style.upper()} style...")
        
        # Start recognition for style
        engine.start_recognition(style)
        
        # Generate test audio simulating beatbox sounds
        duration = 2.0
        samples = int(engine.sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Create style-specific test patterns
        if style == "bass":
            # Heavy bass with low frequencies
            test_audio = (
                0.8 * np.sin(2 * np.pi * 60 * t) * np.exp(-t) +    # Bass drop
                0.4 * np.sin(2 * np.pi * 120 * t) * (t < 0.5) +     # Short bass
                0.1 * np.random.randn(samples)                       # Noise
            )
        elif style == "techno":
            # High-tempo electronic sounds
            test_audio = (
                0.6 * np.sin(2 * np.pi * 440 * t) * np.sin(8 * np.pi * t) +  # Modulated tone
                0.4 * np.sin(2 * np.pi * 4000 * t) * (np.sin(16 * np.pi * t) > 0.5) +  # Hi-hat pattern
                0.2 * np.random.randn(samples)
            )
        elif style == "vocal":
            # Vocal-like formants
            test_audio = (
                0.5 * np.sin(2 * np.pi * 200 * t) +    # Fundamental
                0.3 * np.sin(2 * np.pi * 600 * t) +    # First formant
                0.2 * np.sin(2 * np.pi * 1200 * t) +   # Second formant
                0.1 * np.random.randn(samples)
            )
        else:  # classic, modern
            # Traditional beatbox sounds
            test_audio = (
                0.7 * np.sin(2 * np.pi * 80 * t) * np.exp(-3*t) +       # Kick
                0.5 * np.random.randn(samples) * (np.sin(4 * np.pi * t) > 0.7) +  # Snare
                0.3 * np.random.randn(samples) * (np.sin(8 * np.pi * t) > 0.8)    # Hi-hat
            )
        
        # Recognize beatbox
        result = engine.recognize_beatbox(test_audio)
        
        print(f"   Primary style detected: {result.primary_style.value}")
        print(f"   Overall confidence: {result.overall_confidence:.3f}")
        print(f"   Processing time: {result.processing_time_ms:.2f}ms")
        print(f"   Quality score: {result.quality_score:.3f}")
        print(f"   BPM detected: {result.bpm_detected:.1f}")
        print(f"   Patterns detected: {len(result.patterns)}")
        
        if result.patterns:
            for i, pattern in enumerate(result.patterns[:2]):  # Show top 2
                print(f"     {i+1}. {pattern.pattern_type} (confidence: {pattern.confidence:.3f})")
        
        if result.enhancement_suggestions:
            print(f"   Suggestions: {result.enhancement_suggestions[0]}")
        
        print()
    
    # Performance report
    performance = engine.get_performance_report()
    print("📊 Performance Report:")
    metrics = performance["recognition_metrics"]
    print(f"   Total recognitions: {metrics['total_recognitions']}")
    print(f"   Average confidence: {metrics['average_confidence']:.3f}")
    print(f"   Average processing time: {metrics['average_processing_time']:.2f}ms")
    
    if metrics["pattern_distribution"]:
        print("   Pattern distribution:")
        for pattern, count in metrics["pattern_distribution"].items():
            print(f"     {pattern}: {count}")
    
    print()
    print("✅ Tiny Beatbox Engine demo completed successfully!")
    print("🎧 Ready for Alexa Skills Kit integration!")


if __name__ == "__main__":
    demo_tiny_beatbox_engine()