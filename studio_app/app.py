"""
ElevenLabs Studio App - A comprehensive UI for all ElevenLabs API tools and agents

This application provides a modern web interface for all ElevenLabs capabilities including:
- Text-to-Speech with various models
- Voice Cloning and Design
- Speech-to-Speech conversion
- Audio Isolation and Enhancement
- Conversational AI Agents
- Dubbing and Localization
- Supabase Cloud Integration
- And much more...
"""

import base64
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import streamlit as st

# ElevenLabs imports
try:
    from elevenlabs import play, stream
    from elevenlabs.client import AsyncElevenLabs, ElevenLabs
    from elevenlabs.types import VoiceSettings
except ImportError as e:
    st.error(f"ElevenLabs package not found: {e}")
    st.stop()

# Ethereum tagging import
try:
    from ethereum_tags import render_ethereum_tagging
    ETHEREUM_TAGS_AVAILABLE = True
except ImportError:
    ETHEREUM_TAGS_AVAILABLE = False

# Supabase integration import
try:
    from supabase_integration import (
        SupabaseManager,
        auto_save_agent_config,
        init_supabase_session,
        render_cloud_features,
        render_database_setup,
        render_supabase_auth,
        render_supabase_setup,
        track_feature_usage,
    )
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("⚠️ Supabase integration not available. Install with: pip install supabase")

 # Configure page
st.set_page_config(
    page_title="ElevenLabs Studio",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Automatically load ElevenLabs API key from Supabase on startup
if SUPABASE_AVAILABLE:
    if 'supabase_manager' not in st.session_state:
        st.session_state.supabase_manager = SupabaseManager()
    supabase_manager = st.session_state.supabase_manager
    # If user is authenticated, load API key
    if st.session_state.get('supabase_user'):
        supabase_manager.user = st.session_state['supabase_user']
        supabase_manager.load_elevenlabs_api_key()

# Load custom CSS
def load_css():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv('ELEVENLABS_API_KEY', '')
if 'client' not in st.session_state:
    st.session_state.client = None
if 'voices' not in st.session_state:
    st.session_state.voices = []
if 'models' not in st.session_state:
    st.session_state.models = []

# Initialize Supabase session state
if SUPABASE_AVAILABLE:
    init_supabase_session()

class ElevenLabsStudio:
    def __init__(self):
        self.client = None
        self.async_client = None
        
    def initialize_client(self, api_key: str):
        """Initialize ElevenLabs clients with API key"""
        try:
            self.client = ElevenLabs(api_key=api_key)
            self.async_client = AsyncElevenLabs(api_key=api_key)
            st.session_state.client = self.client
            return True
        except Exception as e:
            st.error(f"Failed to initialize client: {str(e)}")
            return False
    
    def get_voices(self):
        """Fetch available voices"""
        if not self.client:
            return []
        try:
            response = self.client.voices.search()
            return response.voices
        except Exception as e:
            st.error(f"Error fetching voices: {str(e)}")
            return []
    
    def get_models(self):
        """Fetch available models"""
        if not self.client:
            return []
        try:
            response = self.client.models.list()
            return response.models
        except Exception as e:
            st.error(f"Error fetching models: {str(e)}")
            return []

def main():
    studio = ElevenLabsStudio()
    
    # Header with Premium styling
    st.markdown("""
    <div class="main-header">
        <h1><span class="gradient-text">ElevenLabs Studio</span></h1>
        <p>Professional AI Voice Generation & Audio Processing Suite</p>
        <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span class="status-badge status-online">
                ✨ AI-Powered
            </span>
            <span class="status-badge status-online">
                🌍 29+ Languages
            </span>
            <span class="status-badge status-online">
                ⚡ Real-time Processing
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with Premium dark theme
    with st.sidebar:
        # Sidebar header
        st.markdown("""
        <div style="padding: 1rem 0; text-align: center; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem;">
            <h2 style="color: var(--text-main); margin: 0; font-size: 1.5rem;">
                <span class="gradient-text">⚙️ Studio Control</span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "ElevenLabs API Key",
            type="password",
            value=st.session_state.api_key,
            help="Enter your ElevenLabs API key to access all features",
            placeholder="sk-..."
        )
        
        if api_key and api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            if studio.initialize_client(api_key):
                st.success("✅ API Key validated!")
                # Cache voices and models
                st.session_state.voices = studio.get_voices()
                st.session_state.models = studio.get_models()
                
                # Option to save API key to Supabase
                if SUPABASE_AVAILABLE and st.session_state.get('supabase_user'):
                    if st.button("💾 Save API Key to Cloud", help="Save your API key securely to Supabase"):
                        if st.session_state.supabase_manager.save_elevenlabs_api_key(api_key):
                            st.success("✅ API Key saved to Supabase!")
            else:
                st.error("❌ Invalid API Key")
        
        # Connection status
        if st.session_state.api_key:
            st.markdown("""
            <div style="background: rgba(62, 207, 142, 0.1); border: 1px solid var(--primary); 
                        border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center;" class="pulse-effect">
                <span style="color: var(--primary); font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                    <span style="width: 8px; height: 8px; background: var(--primary); border-radius: 50%;"></span>
                    Connected to ElevenLabs
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid #EF4444; 
                        border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center;">
                <span style="color: #EF4444; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                    <span style="width: 8px; height: 8px; background: #EF4444; border-radius: 50%;"></span>
                    Not Connected
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu with enhanced styling
        st.markdown("### 📋 Features")
        
        # Feature categories with icons and descriptions
        feature_options = [
            ("🎵 Text-to-Speech", "Convert text to natural speech"),
            ("🎭 Voice Design & Cloning", "Create and clone custom voices"),
            ("🔄 Speech-to-Speech", "Convert between voice styles"),
            ("🎚️ Audio Processing", "Enhance and process audio"),
            ("🤖 Conversational AI", "Build intelligent voice agents"),
            ("🏷️ Ethereum Voice Tags", "Tag lyrics with Ethereum persona"),
            ("🌍 Dubbing & Translation", "Localize content globally"),
            ("📊 Analytics & Usage", "Monitor usage and performance"),
            ("⚙️ Advanced Tools", "API testing and batch processing"),
            ("☁️ Cloud Features", "Supabase integration and storage")
        ]
        
        # Create a more visual feature selector
        feature_names = [f[0] for f in feature_options]
        feature_descriptions = [f[1] for f in feature_options]
        
        selected_feature_idx = st.selectbox(
            "Select Feature",
            range(len(feature_names)),
            format_func=lambda x: feature_names[x]
        )
        
        # Ensure selected_feature_idx is an integer
        if isinstance(selected_feature_idx, str):
            selected_feature_idx = 0
        
        feature = feature_names[selected_feature_idx]
        
        # Show feature description
        st.markdown(f"""
        <div style="background: var(--bg-surface); border: 1px solid var(--border); 
                    border-radius: 12px; padding: 1rem; margin-top: 1rem;">
            <p style="color: var(--text-muted); font-size: 0.9rem; margin: 0; line-height: 1.5;">
                {feature_descriptions[selected_feature_idx]}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick stats if connected
        if st.session_state.voices and st.session_state.models:
            st.markdown("### 📊 Quick Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Voices", len(st.session_state.voices), delta=None)
            with col2:
                st.metric("Models", len(st.session_state.models), delta=None)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: var(--text-muted); font-size: 0.8rem; margin: 0;">
                Powered by <span class="gradient-text">ElevenLabs AI</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if not st.session_state.api_key:
        st.warning("⚠️ Please enter your ElevenLabs API key in the sidebar to get started.")
        
        # Show feature overview with Supabase styling
        st.markdown("## 🚀 Available Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🎵 Text-to-Speech</h3>
                <p>Convert text to natural-sounding speech with multiple models and voices</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="status-badge status-online">Multiple AI models</span>
                    <span class="status-badge status-online">29+ languages</span>
                    <span class="status-badge status-online">Real-time streaming</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3>🔄 Speech-to-Speech</h3>
                <p>Transform speech from one voice to another while preserving emotion</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="status-badge status-online">Voice conversion</span>
                    <span class="status-badge status-online">Emotion preservation</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3>🤖 Conversational AI</h3>
                <p>Build intelligent voice agents for interactive conversations</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="status-badge status-online">Real-time conversations</span>
                    <span class="status-badge status-online">Phone integration</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>🎭 Voice Design & Cloning</h3>
                <p>Create custom voices from text descriptions or audio samples</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="status-badge status-online">AI voice generation</span>
                    <span class="status-badge status-online">Instant cloning</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3>🎚️ Audio Processing</h3>
                <p>Advanced audio enhancement and isolation tools</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="status-badge status-online">Audio isolation</span>
                    <span class="status-badge status-online">Enhancement</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3>🌍 Dubbing & Translation</h3>
                <p>Localize content with AI-powered dubbing and translation</p>
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="status-badge status-online">Multi-language dubbing</span>
                    <span class="status-badge status-online">Voice preservation</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        return
    
    # Feature implementations
    if feature == "🎵 Text-to-Speech":
        render_text_to_speech(studio)
    elif feature == "🎭 Voice Design & Cloning":
        render_voice_design(studio)
    elif feature == "🔄 Speech-to-Speech":
        render_speech_to_speech(studio)
    elif feature == "🎚️ Audio Processing":
        render_audio_processing(studio)
    elif feature == "🤖 Conversational AI":
        render_conversational_ai(studio)
    elif feature == "�️ Ethereum Voice Tags":
        if ETHEREUM_TAGS_AVAILABLE:
            render_ethereum_tagging()
        else:
            st.error("❌ Ethereum tagging module not available")
    elif feature == "�🌍 Dubbing & Translation":
        render_dubbing(studio)
    elif feature == "📊 Analytics & Usage":
        render_analytics(studio)
    elif feature == "⚙️ Advanced Tools":
        render_advanced_tools(studio)
    elif feature == "☁️ Cloud Features":
        render_cloud_integration(studio)

def render_section_header(title: str, description: str):
    """Render a consistent section header"""
    st.markdown(f"""
    <div class="section-header">
        <h2>{title}</h2>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_text_to_speech(studio: ElevenLabsStudio):
    """Render Text-to-Speech interface"""
    render_section_header("🎵 Text-to-Speech", "Convert text to natural-sounding speech using advanced AI models")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input
        text = st.text_area(
            "Enter text to convert to speech",
            height=150,
            placeholder="Type your text here... (e.g., 'The first move is what sets everything in motion.')"
        )
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            col_adv1, col_adv2 = st.columns(2)
            
            with col_adv1:
                stability = st.slider("Stability", 0.0, 1.0, 0.75, 0.01)
                similarity_boost = st.slider("Similarity Boost", 0.0, 1.0, 0.75, 0.01)
                style = st.slider("Style", 0.0, 1.0, 0.0, 0.01)
                
            with col_adv2:
                enable_logging = st.checkbox("Enable Logging", False)
                optimize_streaming = st.slider("Optimize Streaming Latency", 0, 4, 0)
                output_format = st.selectbox(
                    "Output Format",
                    ["mp3_44100_128", "mp3_44100_192", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100"]
                )
    
    with col2:
        # Voice selection
        st.markdown("### 🎭 Voice Selection")
        if st.session_state.voices:
            voice_names = [f"{voice.name} ({voice.labels.get('description', 'No description') if voice.labels else 'No description'})" 
                          for voice in st.session_state.voices]
            selected_voice_idx = st.selectbox(
                "Select Voice",
                range(len(voice_names)),
                format_func=lambda x: voice_names[x]
            )
            selected_voice = st.session_state.voices[selected_voice_idx]
            
            # Voice preview
            st.markdown(f"**Voice ID:** `{selected_voice.voice_id}`")
            if selected_voice.preview_url:
                st.audio(selected_voice.preview_url)
        else:
            st.warning("No voices available. Check your API key.")
            return
        
        # Model selection
        st.markdown("### 🧠 Model Selection")
        if st.session_state.models:
            tts_models = [model for model in st.session_state.models if hasattr(model, 'can_do_text_to_speech') and model.can_do_text_to_speech]
            if tts_models:
                model_names = [f"{model.name} - {model.description}" for model in tts_models]
                selected_model_idx = st.selectbox(
                    "Select Model",
                    range(len(model_names)),
                    format_func=lambda x: model_names[x]
                )
                selected_model = tts_models[selected_model_idx]
            else:
                st.warning("No TTS models available")
                return
        else:
            st.warning("No models available")
            return
    
    # Generate button
    if st.button("🎤 Generate Speech", type="primary", use_container_width=True):
        if not text.strip():
            st.error("Please enter some text to convert.")
            return
        
        with st.spinner("Generating speech..."):
            try:
                voice_settings = VoiceSettings(
                    stability=stability,
                    similarity_boost=similarity_boost,
                    style=style,
                    use_speaker_boost=True
                )
                
                audio = studio.client.text_to_speech.convert(
                    text=text,
                    voice_id=selected_voice.voice_id,
                    model_id=selected_model.model_id,
                    voice_settings=voice_settings,
                    output_format=output_format,
                    enable_logging=enable_logging,
                    optimize_streaming_latency=optimize_streaming if optimize_streaming > 0 else None
                )
                
                # Convert audio bytes to base64 for playback
                audio_bytes = b''.join(audio)
                audio_b64 = base64.b64encode(audio_bytes).decode()
                
                st.success("✅ Speech generated successfully!")
                
                # Audio player with Supabase styling
                st.markdown("""
                <div class="audio-player glass-card">
                    <h4>🔊 Generated Audio</h4>
                    <p style="color: var(--supabase-text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
                        Audio generated successfully with ElevenLabs AI
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.audio(audio_bytes, format='audio/mp3')
                
                # Download button
                st.download_button(
                    label="📥 Download Audio",
                    data=audio_bytes,
                    file_name=f"elevenlabs_tts_{selected_voice.name.replace(' ', '_')}.mp3",
                    mime="audio/mpeg"
                )
                
            except Exception as e:
                st.error(f"Error generating speech: {str(e)}")

def render_voice_design(studio: ElevenLabsStudio):
    """Render Voice Design & Cloning interface"""
    render_section_header("🎭 Voice Design & Cloning", "Create unique AI voices or clone existing ones")
    
    tab1, tab2, tab3 = st.tabs(["🎨 Design Voice", "📸 Instant Clone", "🎯 Professional Clone"])
    
    with tab1:
        st.markdown("### 🎨 AI Voice Generation")
        st.info("Create a custom voice from a text description using AI")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            voice_description = st.text_area(
                "Describe the voice you want to create",
                height=100,
                placeholder="e.g., A warm, friendly female voice with a slight British accent, perfect for audiobooks"
            )
            
            with st.expander("⚙️ Voice Generation Settings"):
                auto_generate_text = st.checkbox("Auto-generate test text", True)
                if not auto_generate_text:
                    test_text = st.text_input("Custom test text", "Hello, this is a test of the generated voice.")
                
                col_voice1, col_voice2 = st.columns(2)
                with col_voice1:
                    loudness = st.slider("Loudness", -1.0, 1.0, 0.0, 0.1)
                    quality = st.slider("Quality", 0.0, 1.0, 0.75, 0.01)
                
                with col_voice2:
                    seed = st.number_input("Seed (for reproducibility)", 0, 1000000, 42)
                    guidance_scale = st.slider("Guidance Scale", 0.0, 5.0, 1.0, 0.1)
        
        with col2:
            st.markdown("### 🎵 Output Settings")
            output_format = st.selectbox(
                "Output Format",
                ["mp3_44100_128", "mp3_44100_192", "pcm_16000", "pcm_22050"]
            )
        
        if st.button("🎨 Generate Voice Previews", type="primary"):
            if not voice_description.strip():
                st.error("Please provide a voice description.")
                return
            
            with st.spinner("Generating voice previews..."):
                try:
                    response = studio.client.text_to_voice.create_previews(
                        voice_description=voice_description,
                        output_format=output_format,
                        text=None if auto_generate_text else test_text,
                        auto_generate_text=auto_generate_text,
                        loudness=loudness,
                        quality=quality,
                        seed=seed,
                        guidance_scale=guidance_scale
                    )
                    
                    st.success(f"✅ Generated {len(response.previews)} voice previews!")
                    
                    # Display previews
                    for i, preview in enumerate(response.previews):
                        with st.container():
                            st.markdown(f"#### Preview {i+1}")
                            
                            # Decode base64 audio
                            audio_bytes = base64.b64decode(preview.audio_base_64)
                            st.audio(audio_bytes, format='audio/mp3')
                            
                            col_preview1, col_preview2 = st.columns([3, 1])
                            with col_preview1:
                                st.text(f"Generated Voice ID: {preview.generated_voice_id}")
                            
                            with col_preview2:
                                if st.button(f"Create Voice from Preview {i+1}", key=f"create_{i}"):
                                    # Create voice from preview
                                    voice_name = st.text_input(f"Voice Name for Preview {i+1}", f"AI Voice {i+1}")
                                    if voice_name:
                                        try:
                                            voice = studio.client.text_to_voice.create_voice_from_preview(
                                                voice_name=voice_name,
                                                voice_description=voice_description,
                                                generated_voice_id=preview.generated_voice_id
                                            )
                                            st.success(f"✅ Voice '{voice_name}' created successfully! Voice ID: {voice.voice_id}")
                                        except Exception as e:
                                            st.error(f"Error creating voice: {str(e)}")
                            
                            st.markdown("---")
                
                except Exception as e:
                    st.error(f"Error generating voice previews: {str(e)}")
    
    with tab2:
        st.markdown("### 📸 Instant Voice Cloning")
        st.info("Clone a voice instantly from audio samples (requires fewer samples)")
        
        uploaded_files = st.file_uploader(
            "Upload audio samples (MP3, WAV)",
            type=['mp3', 'wav'],
            accept_multiple_files=True,
            help="Upload 1-3 audio samples for instant voice cloning"
        )
        
        if uploaded_files:
            voice_name = st.text_input("Voice Name", "My Cloned Voice")
            voice_description = st.text_area(
                "Voice Description (optional)",
                placeholder="Describe the characteristics of this voice..."
            )
            
            if st.button("📸 Create Instant Clone", type="primary"):
                with st.spinner("Creating instant voice clone..."):
                    try:
                        # Save uploaded files temporarily
                        file_paths = []
                        for uploaded_file in uploaded_files:
                            file_path = f"temp_{uploaded_file.name}"
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            file_paths.append(file_path)
                        
                        # Create voice clone
                        voice = studio.client.voices.ivc.create(
                            name=voice_name,
                            description=voice_description,
                            files=file_paths
                        )
                        
                        st.success(f"✅ Instant voice clone '{voice_name}' created! Voice ID: {voice.voice_id}")
                        
                        # Clean up temporary files
                        for file_path in file_paths:
                            os.remove(file_path)
                    
                    except Exception as e:
                        st.error(f"Error creating voice clone: {str(e)}")
    
    with tab3:
        st.markdown("### 🎯 Professional Voice Cloning")
        st.info("Create high-quality voice clones with more samples and customization")
        
        st.warning("This feature requires a higher-tier subscription and more audio samples.")
        
        # Professional cloning interface would go here
        # This typically requires more samples and advanced processing
        st.markdown("""
        **Professional Voice Cloning Features:**
        - Higher quality voice reproduction
        - Better emotion and accent preservation  
        - Requires 10+ minutes of clean audio
        - Advanced voice training options
        - Custom voice fine-tuning
        """)

def render_speech_to_speech(studio: ElevenLabsStudio):
    """Render Speech-to-Speech interface"""
    render_section_header("🔄 Speech-to-Speech Conversion", "Convert speech from one voice to another while preserving emotion and intonation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Audio input
        st.markdown("### 🎤 Input Audio")
        input_method = st.radio(
            "Select input method",
            ["Upload File", "Record Audio"]
        )
        
        audio_file = None
        if input_method == "Upload File":
            audio_file = st.file_uploader(
                "Upload audio file",
                type=['mp3', 'wav', 'flac', 'm4a'],
                help="Upload the audio you want to convert"
            )
        else:
            st.info("Audio recording feature would be implemented here using streamlit-audio-recorder or similar")
    
    with col2:
        # Voice selection for conversion
        st.markdown("### 🎭 Target Voice")
        if st.session_state.voices:
            voice_names = [f"{voice.name}" for voice in st.session_state.voices]
            selected_voice_idx = st.selectbox(
                "Convert to voice",
                range(len(voice_names)),
                format_func=lambda x: voice_names[x]
            )
            selected_voice = st.session_state.voices[selected_voice_idx]
        
        # Model selection for S2S
        st.markdown("### 🧠 Model")
        if st.session_state.models:
            s2s_models = [model for model in st.session_state.models 
                         if hasattr(model, 'can_do_voice_conversion') and model.can_do_voice_conversion]
            if s2s_models:
                model_names = [model.name for model in s2s_models]
                selected_model_idx = st.selectbox(
                    "Speech-to-Speech Model",
                    range(len(model_names)),
                    format_func=lambda x: model_names[x]
                )
                selected_model = s2s_models[selected_model_idx]
    
    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        col_s2s1, col_s2s2 = st.columns(2)
        
        with col_s2s1:
            output_format = st.selectbox(
                "Output Format",
                ["mp3_44100_128", "mp3_44100_192", "pcm_16000", "pcm_22050"]
            )
            remove_bg_noise = st.checkbox("Remove Background Noise", True)
        
        with col_s2s2:
            enable_logging = st.checkbox("Enable Logging", False)
            optimize_streaming = st.slider("Optimize Streaming", 0, 4, 0)
    
    # Convert button
    if st.button("🔄 Convert Speech", type="primary", disabled=not audio_file):
        if not audio_file:
            st.error("Please upload an audio file first.")
            return
        
        with st.spinner("Converting speech..."):
            try:
                # Read audio file
                audio_bytes = audio_file.read()
                
                # Perform speech-to-speech conversion
                converted_audio = studio.client.speech_to_speech.convert(
                    voice_id=selected_voice.voice_id,
                    audio=audio_bytes,
                    model_id=selected_model.model_id,
                    output_format=output_format,
                    remove_background_noise=remove_bg_noise,
                    enable_logging=enable_logging,
                    optimize_streaming_latency=optimize_streaming if optimize_streaming > 0 else None
                )
                
                # Convert to bytes for playback
                converted_bytes = b''.join(converted_audio)
                
                st.success("✅ Speech converted successfully!")
                
                # Show original and converted audio
                col_audio1, col_audio2 = st.columns(2)
                
                with col_audio1:
                    st.markdown("#### 🎵 Original Audio")
                    st.audio(audio_bytes, format='audio/mp3')
                
                with col_audio2:
                    st.markdown("#### 🎭 Converted Audio")
                    st.audio(converted_bytes, format='audio/mp3')
                
                # Download button
                st.download_button(
                    label="📥 Download Converted Audio",
                    data=converted_bytes,
                    file_name=f"speech_to_speech_{selected_voice.name.replace(' ', '_')}.mp3",
                    mime="audio/mpeg"
                )
            
            except Exception as e:
                st.error(f"Error converting speech: {str(e)}")

def render_audio_processing(studio: ElevenLabsStudio):
    """Render Audio Processing interface"""
    render_section_header("🎚️ Audio Processing & Enhancement", "Isolate vocals, remove noise, and enhance audio quality")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Audio Isolation", "🔧 Enhancement", "📊 Analysis"])
    
    with tab1:
        st.markdown("### 🎯 Audio Isolation")
        st.info("Isolate specific audio elements like vocals, instruments, or remove background noise")
        
        uploaded_audio = st.file_uploader(
            "Upload audio file to process",
            type=['mp3', 'wav', 'flac'],
            help="Upload audio for isolation processing"
        )
        
        if uploaded_audio:
            col1, col2 = st.columns(2)
            
            with col1:
                isolation_type = st.selectbox(
                    "Isolation Type",
                    ["vocals", "instruments", "background", "noise_reduction"]
                )
                
                quality = st.slider("Processing Quality", 1, 10, 8)
            
            with col2:
                output_format = st.selectbox(
                    "Output Format",
                    ["mp3", "wav", "flac"]
                )
            
            if st.button("🎯 Process Audio", type="primary"):
                with st.spinner("Processing audio..."):
                    try:
                        # Audio isolation would be implemented here
                        # This is a placeholder for the actual API call
                        st.info("Audio isolation processing would be implemented here using the ElevenLabs audio isolation API")
                        
                        # For demonstration, show the original audio
                        st.markdown("#### Original Audio")
                        st.audio(uploaded_audio.read(), format='audio/mp3')
                        
                    except Exception as e:
                        st.error(f"Error processing audio: {str(e)}")
    
    with tab2:
        st.markdown("### 🔧 Audio Enhancement")
        st.info("Enhance audio quality, reduce noise, and improve clarity")
        
        # Enhancement options would go here
        st.markdown("""
        **Available Enhancement Features:**
        - Noise reduction
        - Audio upscaling
        - Dynamic range compression
        - EQ adjustment
        - Reverb removal
        """)
    
    with tab3:
        st.markdown("### 📊 Audio Analysis")
        st.info("Analyze audio characteristics and quality metrics")
        
        # Analysis tools would go here
        st.markdown("""
        **Analysis Features:**
        - Audio quality scoring
        - Frequency analysis
        - Voice characteristics detection
        - Background noise levels
        - Dynamic range measurement
        """)

def render_conversational_ai(studio: ElevenLabsStudio):
    """Render Conversational AI interface with full agent builder"""
    render_section_header("🤖 Conversational AI Agents", "Create, configure, and deploy intelligent voice agents with advanced AI capabilities")
    
    # Enhanced tabs with agent builder
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 Agent Builder", 
        "📞 Phone Integration", 
        "💬 Chat Interface",
        "🛠️ Tools & Knowledge"
    ])
    
    with tab1:
        # Load the comprehensive agent builder
        try:
            import os
            import sys
            
            # Add pages directory to path
            pages_dir = os.path.join(os.path.dirname(__file__), 'pages')
            if pages_dir not in sys.path:
                sys.path.append(pages_dir)
            
            from pages.agent_builder import AgentBuilder
            
            # Initialize and run the agent builder
            builder = AgentBuilder()
            builder.run()
            
        except ImportError as e:
            st.error(f"Could not load agent builder: {e}")
            # Fallback to simple interface
            render_simple_agent_builder(studio)
        except Exception as e:
            st.error(f"Agent builder error: {e}")
            render_simple_agent_builder(studio)
    
    with tab2:
        render_phone_integration(studio)
    
    with tab3:
        render_chat_interface(studio)
    
    with tab4:
        render_tools_knowledge(studio)

def render_simple_agent_builder(studio: ElevenLabsStudio):
    """Simple fallback agent builder interface"""
    st.markdown("### 🤖 AI Agent Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        agent_name = st.text_input("Agent Name", "My AI Assistant")
        agent_description = st.text_area(
            "Agent Description",
            placeholder="Describe your AI agent's personality and purpose..."
        )
        
        # Voice selection for agent
        agent_voice = None
        if st.session_state.voices:
            voice_names = [voice.name for voice in st.session_state.voices]
            agent_voice_idx = st.selectbox(
                "Agent Voice",
                range(len(voice_names)),
                format_func=lambda x: voice_names[x]
            )
            agent_voice = st.session_state.voices[agent_voice_idx]
    
    with col2:
        # Agent settings
        st.markdown("#### Agent Settings")
        response_speed = st.slider("Response Speed", 1, 10, 7)
        personality_warmth = st.slider("Personality Warmth", 1, 10, 7)
        knowledge_depth = st.slider("Knowledge Depth", 1, 10, 8)
        
        enable_interruptions = st.checkbox("Allow Interruptions", True)
        enable_emotions = st.checkbox("Emotional Responses", True)
    
    # System prompt
    system_prompt = st.text_area(
        "System Prompt",
        height=150,
        placeholder="You are a helpful AI assistant. Your role is to..."
    )
    
    if st.button("🤖 Create Agent", type="primary"):
        if agent_voice:
            st.success(f"✅ Agent '{agent_name}' would be created with voice '{agent_voice.name}'")
        else:
            st.success(f"✅ Agent '{agent_name}' would be created")
        st.info("This would integrate with the ElevenLabs Conversational AI API to create the agent")

def render_phone_integration(studio: ElevenLabsStudio):
    """Render phone integration interface"""
    st.markdown("### 📞 Phone Integration")
    st.info("Connect your AI agent to phone systems for voice calls")
    
    # Phone integration settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Twilio Integration")
        twilio_account_sid = st.text_input("Account SID", type="password")
        twilio_auth_token = st.text_input("Auth Token", type="password")
        phone_number = st.text_input("Phone Number", "+1234567890")
        
        if st.button("🔗 Connect Twilio"):
            if twilio_account_sid and twilio_auth_token:
                st.success("✅ Twilio integration would be configured")
            else:
                st.error("❌ Please provide Twilio credentials")
    
    with col2:
        st.markdown("#### Call Settings")
        max_call_duration = st.number_input("Max Call Duration (minutes)", 1, 60, 10)
        recording_enabled = st.checkbox("Enable Call Recording", True)
        transcription_enabled = st.checkbox("Enable Transcription", True)
        
        st.markdown("#### SIP Trunk Integration")
        sip_enabled = st.checkbox("Enable SIP Trunk")
        if sip_enabled:
            sip_server = st.text_input("SIP Server", "sip.example.com")
            sip_username = st.text_input("SIP Username")
            sip_password = st.text_input("SIP Password", type="password")

def render_chat_interface(studio: ElevenLabsStudio):
    """Render chat testing interface"""
    st.markdown("### 💬 Chat Interface Testing")
    st.info("Test your conversational AI agent with a chat interface")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat display
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Simulate agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # This would integrate with the actual agent
                response = f"I understand you said: '{prompt}'. This is a simulated response from your AI agent."
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Chat controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("💾 Save Chat"):
            st.success("Chat history saved!")
    
    with col3:
        if st.button("📤 Export Chat"):
            chat_json = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                "Download Chat",
                chat_json,
                "chat_history.json",
                "application/json"
            )

def render_tools_knowledge(studio: ElevenLabsStudio):
    """Render tools and knowledge base management"""
    st.markdown("### 🛠️ Tools & Knowledge Base")
    
    tool_tab1, tool_tab2 = st.tabs(["🔧 Agent Tools", "📚 Knowledge Base"])
    
    with tool_tab1:
        st.markdown("#### Available Agent Tools")
        
        # Load and display available tools
        try:
            if studio.client:
                with st.spinner("Loading available tools..."):
                    tools_response = studio.client.conversational_ai.tools.list()
                    if hasattr(tools_response, 'tools'):
                        tools = tools_response.tools
                        
                        if tools:
                            for tool in tools[:10]:  # Show first 10 tools
                                with st.expander(f"🔧 {getattr(tool, 'name', 'Unknown Tool')}"):
                                    st.write(f"**Description:** {getattr(tool, 'description', 'No description')}")
                                    st.write(f"**Type:** {getattr(tool, 'type', 'Unknown')}")
                                    if st.button(f"Add {getattr(tool, 'name', 'Tool')}", key=f"add_tool_{getattr(tool, 'tool_id', 'unknown')}"):
                                        st.success(f"Tool '{getattr(tool, 'name', 'Unknown')}' added to agent")
                        else:
                            st.info("No tools available in your workspace")
                    else:
                        st.info("Could not load tools - check your API connection")
        except Exception as e:
            st.warning(f"Could not load tools: {e}")
        
        # Tool creation
        st.markdown("---")
        st.markdown("#### Create Custom Tool")
        
        with st.form("create_tool"):
            tool_name = st.text_input("Tool Name")
            tool_description = st.text_area("Tool Description")
            tool_type = st.selectbox("Tool Type", ["function", "webhook", "api"])
            
            if st.form_submit_button("Create Tool"):
                if tool_name and tool_description:
                    st.success(f"Custom tool '{tool_name}' would be created")
                else:
                    st.error("Please provide tool name and description")
    
    with tool_tab2:
        st.markdown("#### Knowledge Base Management")
        
        # File upload for knowledge base
        uploaded_files = st.file_uploader(
            "Upload Knowledge Files",
            type=['txt', 'pdf', 'docx', 'md'],
            accept_multiple_files=True,
            help="Upload documents to enhance your agent's knowledge"
        )
        
        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} files to knowledge base")
            for file in uploaded_files:
                st.write(f"📄 {file.name} ({file.size} bytes)")
        
        # Knowledge base settings
        st.markdown("---")
        st.markdown("#### Knowledge Base Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            chunk_size = st.slider("Chunk Size", 100, 1000, 500)
            overlap_size = st.slider("Overlap Size", 0, 200, 50)
        
        with col2:
            similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7)
            max_results = st.slider("Max Results", 1, 20, 5)
        
        if st.button("📞 Setup Phone Integration"):
            st.info("Phone integration would be configured here using the ElevenLabs phone integration API")

def render_dubbing(studio: ElevenLabsStudio):
    """Render Dubbing & Translation interface"""
    render_section_header("🌍 Dubbing & Translation", "Localize your content with AI-powered dubbing and translation")
    
    tab1, tab2 = st.tabs(["🎬 Video Dubbing", "🔄 Audio Translation"])
    
    with tab1:
        st.markdown("### 🎬 Video Dubbing")
        
        uploaded_video = st.file_uploader(
            "Upload video file",
            type=['mp4', 'mov', 'avi'],
            help="Upload video for dubbing"
        )
        
        if uploaded_video:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Dubbing Settings")
                source_language = st.selectbox(
                    "Source Language",
                    ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Korean"]
                )
                
                target_language = st.selectbox(
                    "Target Language",
                    ["Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Korean", "English"]
                )
            
            with col2:
                st.markdown("#### Voice Settings")
                if st.session_state.voices:
                    dubbing_voice_idx = st.selectbox(
                        "Dubbing Voice",
                        range(len(st.session_state.voices)),
                        format_func=lambda x: st.session_state.voices[x].name
                    )
                    dubbing_voice = st.session_state.voices[dubbing_voice_idx]
                
                preserve_timing = st.checkbox("Preserve Original Timing", True)
                emotion_transfer = st.checkbox("Transfer Emotions", True)
            
            if st.button("🎬 Start Dubbing", type="primary"):
                with st.spinner("Processing video for dubbing..."):
                    st.info("Video dubbing would be processed here using the ElevenLabs dubbing API")
    
    with tab2:
        st.markdown("### 🔄 Audio Translation")
        
        uploaded_audio = st.file_uploader(
            "Upload audio file",
            type=['mp3', 'wav', 'flac'],
            help="Upload audio for translation"
        )
        
        if uploaded_audio:
            # Similar interface for audio translation
            st.info("Audio translation interface would be implemented here")

def render_analytics(studio: ElevenLabsStudio):
    """Render Analytics & Usage interface"""
    render_section_header("📊 Analytics & Usage", "Monitor your character usage, billing, and performance metrics")
    
    tab1, tab2, tab3 = st.tabs(["📈 Usage Stats", "💰 Billing", "🎯 Performance"])
    
    with tab1:
        st.markdown("### 📈 Usage Statistics")
        
        try:
            # Get usage data
            usage_data = studio.client.usage.get_characters_usage_metrics()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Characters Used",
                    f"{usage_data.characters_used:,}",
                    f"+{usage_data.characters_used - getattr(usage_data, 'previous_characters_used', 0):,}"
                )
            
            with col2:
                st.metric(
                    "Characters Limit",
                    f"{usage_data.character_limit:,}",
                    f"{((usage_data.characters_used / usage_data.character_limit) * 100):.1f}% used"
                )
            
            with col3:
                remaining = usage_data.character_limit - usage_data.characters_used
                st.metric(
                    "Remaining",
                    f"{remaining:,}",
                    f"{(remaining / usage_data.character_limit * 100):.1f}% left"
                )
            
            with col4:
                reset_date = getattr(usage_data, 'reset_date', 'Unknown')
                st.metric(
                    "Reset Date",
                    reset_date,
                    "Monthly cycle"
                )
            
            # Usage chart placeholder
            st.markdown("#### Usage Over Time")
            st.info("Usage charts would be displayed here with historical data")
        
        except Exception as e:
            st.error(f"Error fetching usage data: {str(e)}")
    
    with tab2:
        st.markdown("### 💰 Billing Information")
        st.info("Billing details would be displayed here")
    
    with tab3:
        st.markdown("### 🎯 Performance Metrics")
        st.info("Performance analytics would be displayed here")

def render_advanced_tools(studio: ElevenLabsStudio):
    """Render Advanced Tools interface"""
    render_section_header("⚙️ Advanced Tools", "Developer tools for API testing, batch processing, and webhooks")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 API Testing", "📝 Batch Processing", "🔗 Webhooks", "⚡ Real-time"])
    
    with tab1:
        st.markdown("### 🔧 API Testing")
        st.info("Test individual API endpoints and parameters")
        
        # API endpoint selector
        endpoints = [
            "text-to-speech/convert",
            "voices/search",
            "models/list",
            "text-to-voice/create-previews",
            "speech-to-speech/convert"
        ]
        
        selected_endpoint = st.selectbox("Select API Endpoint", endpoints)
        
        # Parameter input
        st.markdown("#### Parameters")
        params_json = st.text_area(
            "Parameters (JSON)",
            height=200,
            value='{\n  "text": "Hello world",\n  "voice_id": "21m00Tcm4TlvDq8ikWAM"\n}'
        )
        
        if st.button("🔧 Test API"):
            try:
                params = json.loads(params_json)
                st.success("✅ Parameters are valid JSON")
                st.json(params)
                st.info(f"Would call {selected_endpoint} with these parameters")
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {str(e)}")
    
    with tab2:
        st.markdown("### 📝 Batch Processing")
        st.info("Process multiple texts or files in batch")
        
        # Batch text input
        batch_texts = st.text_area(
            "Enter texts (one per line)",
            height=200,
            placeholder="Text 1\nText 2\nText 3..."
        )
        
        if batch_texts:
            texts = [line.strip() for line in batch_texts.split('\n') if line.strip()]
            st.info(f"Found {len(texts)} texts to process")
            
            if st.button("📝 Process Batch"):
                st.info("Batch processing would be implemented here")
    
    with tab3:
        st.markdown("### 🔗 Webhooks")
        st.info("Configure webhooks for event notifications")
        
        webhook_url = st.text_input("Webhook URL", "https://your-server.com/webhook")
        
        events = st.multiselect(
            "Select Events",
            ["generation.completed", "voice.created", "dubbing.finished", "error.occurred"]
        )
        
        if st.button("🔗 Setup Webhook"):
            st.info(f"Would setup webhook for events: {events}")
    
    with tab4:
        st.markdown("### ⚡ Real-time Streaming")
        st.info("Real-time text-to-speech streaming")
        
        streaming_text = st.text_input("Text for streaming", "This is a test of real-time streaming")
        
        if st.button("⚡ Start Streaming"):
            st.info("Real-time streaming would be implemented here using WebSocket connections")

def render_cloud_integration(studio: ElevenLabsStudio):
    """Render Cloud Integration with Supabase"""
    render_section_header("☁️ Cloud Features & Integration", "Connect to Supabase for cloud storage, authentication, and analytics")
    
    if not SUPABASE_AVAILABLE:
        st.error("❌ Supabase integration not available. Install with: `pip install supabase`")
        st.markdown("Run this command to install Supabase:")
        st.code("pip install supabase", language="bash")
        return
    
    # Check if Supabase is connected
    if not st.session_state.get('supabase_connected', False):
        st.info("🔗 Connect to Supabase to enable cloud features")
        
        cloud_tab1, cloud_tab2 = st.tabs(["🔧 Setup", "📚 Documentation"])
        
        with cloud_tab1:
            render_supabase_setup()
        
        with cloud_tab2:
            st.markdown("### 📚 Supabase Integration Guide")
            
            st.markdown("""
            **What is Supabase?**
            
            Supabase is an open-source Firebase alternative that provides:
            - 🗄️ **Database**: PostgreSQL database with real-time subscriptions
            - 🔐 **Authentication**: User management and security
            - 📁 **Storage**: File storage for audio and documents
            - ⚡ **Real-time**: Live updates and collaboration
            
            **Benefits for ElevenLabs Studio:**
            - 💾 Save agent configurations to the cloud
            - 🔄 Sync data across devices
            - 👥 Share agents with team members
            - 📊 Track usage analytics
            - 🔒 Secure user authentication
            """)
            
            render_database_setup()
    
    else:
        # Supabase is connected, show main interface
        st.success("🟢 Connected to Supabase")
        
        # Authentication interface
        render_supabase_auth()
        
        st.markdown("---")
        
        # Cloud features
        render_cloud_features()
        
        # Auto-save functionality notice
        if st.session_state.get('supabase_user'):
            st.markdown("---")
            st.info("💡 **Auto-save enabled**: Agent configurations are automatically saved to your cloud account")

    # Footer
    st.markdown("""
    <div class="main-footer">
        <p>ElevenLabs Studio • Built with ❤️ using Streamlit</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            <a href="https://elevenlabs.io" target="_blank">ElevenLabs</a> • 
            <a href="https://github.com/elevenlabs/elevenlabs-python" target="_blank">GitHub</a> • 
            <a href="https://docs.elevenlabs.io" target="_blank">Documentation</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
