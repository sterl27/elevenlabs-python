"""
Utility functions for ElevenLabs Studio App
"""

import base64
import os
import tempfile
from typing import Any, Dict, List, Optional

import streamlit as st

from elevenlabs.client import ElevenLabs
from elevenlabs.types import Model, Voice


class AudioUtils:
    """Utility functions for audio processing"""
    
    @staticmethod
    def audio_to_base64(audio_bytes: bytes) -> str:
        """Convert audio bytes to base64 string"""
        return base64.b64encode(audio_bytes).decode()
    
    @staticmethod
    def base64_to_audio(base64_string: str) -> bytes:
        """Convert base64 string to audio bytes"""
        return base64.b64decode(base64_string)
    
    @staticmethod
    def save_temp_audio(audio_bytes: bytes, suffix: str = ".mp3") -> str:
        """Save audio bytes to temporary file and return path"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(audio_bytes)
            return tmp_file.name
    
    @staticmethod
    def cleanup_temp_file(file_path: str):
        """Remove temporary file"""
        try:
            os.unlink(file_path)
        except FileNotFoundError:
            pass


class VoiceManager:
    """Manage voice operations and caching"""
    
    def __init__(self, client: ElevenLabs):
        self.client = client
        self._voices_cache = None
        self._models_cache = None
    
    def get_voices(self, force_refresh: bool = False) -> List[Voice]:
        """Get available voices with caching and defensive checks"""
        if self.client is None:
            st.error("ElevenLabs client is not initialized.")
            return []
        if self._voices_cache is None or force_refresh:
            try:
                response = getattr(self.client, 'voices', None)
                if response and hasattr(response, 'search'):
                    result = response.search()
                    self._voices_cache = getattr(result, 'voices', [])
                else:
                    st.error("Client 'voices' attribute or 'search' method not found.")
                    return []
            except Exception as e:
                st.error(f"Error fetching voices: {str(e)}")
                return []
        return self._voices_cache or []
    
    def get_models(self, force_refresh: bool = False) -> List[Model]:
        """Get available models with caching and defensive checks"""
        if self.client is None:
            st.error("ElevenLabs client is not initialized.")
            return []
        if self._models_cache is None or force_refresh:
            try:
                response = getattr(self.client, 'models', None)
                if response and hasattr(response, 'list'):
                    result = response.list()
                    self._models_cache = getattr(result, 'models', [])
                else:
                    st.error("Client 'models' attribute or 'list' method not found.")
                    return []
            except Exception as e:
                st.error(f"Error fetching models: {str(e)}")
                return []
        return self._models_cache or []
    
    def get_voice_by_id(self, voice_id: str) -> Optional[Voice]:
        """Get voice by ID"""
        voices = self.get_voices()
        for voice in voices:
            if voice.voice_id == voice_id:
                return voice
        return None
    
    def get_voices_by_category(self, category: str = None) -> List[Voice]:
        """Get voices filtered by category"""
        voices = self.get_voices()
        if not category:
            return voices
        
        # Filter voices by category/labels
        filtered_voices = []
        for voice in voices:
            if voice.labels and category.lower() in str(voice.labels).lower():
                filtered_voices.append(voice)
        return filtered_voices
    
    def get_tts_models(self) -> List[Model]:
        """Get models that support text-to-speech"""
        models = self.get_models()
        return [model for model in models 
                if hasattr(model, 'can_do_text_to_speech') and model.can_do_text_to_speech]
    
    def get_voice_conversion_models(self) -> List[Model]:
        """Get models that support voice conversion"""
        models = self.get_models()
        return [model for model in models 
                if hasattr(model, 'can_do_voice_conversion') and model.can_do_voice_conversion]


class SessionManager:
    """Manage Streamlit session state"""
    
    @staticmethod
    def initialize_session():
        """Initialize session state variables"""
        defaults = {
            'api_key': '',
            'client': None,
            'voices_cache': None,
            'models_cache': None,
            'current_voice': None,
            'current_model': None,
            'chat_messages': [],
            'audio_history': [],
            'user_preferences': {
                'theme': 'light',
                'default_voice': None,
                'default_model': None,
                'auto_play': True,
            }
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def save_audio_to_history(audio_data: Dict[str, Any]):
        """Save generated audio to history"""
        if 'audio_history' not in st.session_state:
            st.session_state.audio_history = []
        
        st.session_state.audio_history.append(audio_data)
        
        # Keep only last 10 items
        if len(st.session_state.audio_history) > 10:
            st.session_state.audio_history = st.session_state.audio_history[-10:]
    
    @staticmethod
    def get_user_preference(key: str, default: Any = None) -> Any:
        """Get user preference"""
        return st.session_state.get('user_preferences', {}).get(key, default)
    
    @staticmethod
    def set_user_preference(key: str, value: Any):
        """Set user preference"""
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {}
        st.session_state.user_preferences[key] = value


class UIComponents:
    """Reusable UI components"""
    
    @staticmethod
    def render_voice_selector(voices: List[Voice], key: str = "voice_selector") -> Optional[Voice]:
        """Render voice selection dropdown"""
        if not voices:
            st.warning("No voices available")
            return None
        
        voice_options = {}
        for voice in voices:
            description = "No description"
            if voice.labels and 'description' in voice.labels:
                description = voice.labels['description']
            voice_options[f"{voice.name} - {description}"] = voice
        
        selected_voice_name = st.selectbox(
            "Select Voice",
            list(voice_options.keys()),
            key=key
        )
        
        return voice_options[selected_voice_name] if selected_voice_name else None
    
    @staticmethod
    def render_model_selector(models: List[Model], key: str = "model_selector") -> Optional[Model]:
        """Render model selection dropdown"""
        if not models:
            st.warning("No models available")
            return None
        
        model_options = {}
        for model in models:
            model_options[f"{model.name} - {model.description}"] = model
        
        selected_model_name = st.selectbox(
            "Select Model",
            list(model_options.keys()),
            key=key
        )
        
        return model_options[selected_model_name] if selected_model_name else None
    
    @staticmethod
    def render_audio_player(audio_bytes: bytes, title: str = "Generated Audio"):
        """Render audio player with title"""
        st.markdown(f"#### 🔊 {title}")
        st.audio(audio_bytes, format='audio/mp3')
    
    @staticmethod
    def render_feature_card(title: str, description: str, icon: str = "🔧"):
        """Render a feature card"""
        st.markdown(f"""
        <div class="feature-card">
            <h3>{icon} {title}</h3>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_metrics_row(metrics: Dict[str, Any]):
        """Render a row of metrics"""
        cols = st.columns(len(metrics))
        for i, (label, value) in enumerate(metrics.items()):
            with cols[i]:
                if isinstance(value, dict):
                    st.metric(
                        label,
                        value.get('value', ''),
                        value.get('delta', None)
                    )
                else:
                    st.metric(label, value)

    @staticmethod
    def render_section_header(title: str, description: str):
        """Render a consistent section header"""
        st.markdown(f"""
        <div class="section-header">
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)


class ConfigManager:
    """Manage application configuration"""
    
    DEFAULT_CONFIG = {
        'app': {
            'title': 'ElevenLabs Studio',
            'version': '1.0.0',
            'debug': False,
        },
        'models': {
            'tts': {
                'turbo': 'eleven_turbo_v2_5',
                'multilingual': 'eleven_multilingual_v2',
                'flash': 'eleven_flash_v2_5',
                'monolingual': 'eleven_monolingual_v1',
            },
            'asr': {
                'nova_2': 'nova-2',
                'nova_1': 'nova-1',
                'whisper': 'whisper-1',
            }
        },
        'defaults': {
            'voice_id': 'JBFqnCBsd6RMkjVDRZzb',
            'model_id': 'eleven_turbo_v2_5',
            'language': 'en',
        },
        'audio': {
            'default_format': 'mp3_44100_128',
            'quality_presets': {
                'low': 'mp3_22050_32',
                'medium': 'mp3_44100_128',
                'high': 'mp3_44100_192',
                'ultra': 'pcm_44100',
            }
        },
        'voice_settings': {
            'stability': 0.75,
            'similarity_boost': 0.75,
            'style': 0.0,
            'use_speaker_boost': True,
        },
        'limits': {
            'max_text_length': 5000,
            'max_file_size_mb': 25,
            'max_batch_size': 10,
        }
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get application configuration"""
        # In a real app, this would load from a config file
        return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def get_audio_formats(cls) -> List[str]:
        """Get available audio formats"""
        config = cls.get_config()
        return list(config['audio']['quality_presets'].values())
    
    @classmethod
    def get_quality_preset(cls, preset: str) -> str:
        """Get audio format for quality preset"""
        config = cls.get_config()
        return config['audio']['quality_presets'].get(preset, 'mp3_44100_128')


class ValidationUtils:
    """Validation utilities"""
    
    @staticmethod
    def validate_text_length(text: str, max_length: int = 5000) -> bool:
        """Validate text length"""
        return len(text) <= max_length
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Basic API key validation"""
        return bool(api_key and len(api_key) > 10)
    
    @staticmethod
    def validate_audio_file(file) -> bool:
        """Validate uploaded audio file"""
        if not file:
            return False
        
        # Check file size (25MB limit)
        if file.size > 25 * 1024 * 1024:
            st.error("File size exceeds 25MB limit")
            return False
        
        # Check file type
        allowed_types = ['audio/mpeg', 'audio/wav', 'audio/flac', 'audio/m4a']
        if file.type not in allowed_types:
            st.error(f"Unsupported file type: {file.type}")
            return False
        
        return True


class ErrorHandler:
    """Error handling utilities"""
    
    @staticmethod
    def handle_api_error(error: Exception, context: str = "API call"):
        """Handle and display API errors"""
        error_msg = str(error)
        
        # Common error patterns
        if "unauthorized" in error_msg.lower():
            st.error("🔑 API key is invalid or expired. Please check your credentials.")
        elif "quota" in error_msg.lower():
            st.error("💳 You've exceeded your API quota. Please upgrade your plan.")
        elif "rate limit" in error_msg.lower():
            st.error("⏱️ Rate limit exceeded. Please wait a moment before trying again.")
        elif "network" in error_msg.lower():
            st.error("🌐 Network error. Please check your internet connection.")
        else:
            st.error(f"❌ Error in {context}: {error_msg}")
    
    @staticmethod
    def safe_execute(func, *args, **kwargs):
        """Safely execute a function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.handle_api_error(e, func.__name__)
            return None
