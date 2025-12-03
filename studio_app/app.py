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

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import streamlit as st

# ElevenLabs imports
try:
    from elevenlabs.client import AsyncElevenLabs, ElevenLabs
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
        init_supabase_session,
    )
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("⚠️ Supabase integration not available. Install with: pip install supabase")

# Feature imports
from features.text_to_speech import render_text_to_speech
from features.voice_design import render_voice_design
from features.speech_to_speech import render_speech_to_speech
from features.audio_processing import render_audio_processing
from features.conversational_ai import render_conversational_ai
from features.dubbing import render_dubbing
from features.analytics import render_analytics
from features.advanced_tools import render_advanced_tools
from features.cloud_integration import render_cloud_integration

 # Configure page
st.set_page_config(
    page_title="ElevenLabs Studio",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Automatically load ElevenLabs API key from Supabase on startup
# Automatically load ElevenLabs API key from Supabase on startup
if SUPABASE_AVAILABLE:
    if 'supabase_manager' not in st.session_state:
        st.session_state.supabase_manager = SupabaseManager()
    supabase_manager = st.session_state.supabase_manager
    
    # Try to connect if credentials exist in session state
    if st.session_state.get('supabase_url') and st.session_state.get('supabase_key'):
        if not supabase_manager.client:
            supabase_manager.initialize(st.session_state.supabase_url, st.session_state.supabase_key)
            
    # If user is authenticated, load API key
    if st.session_state.get('supabase_user'):
        supabase_manager.user = st.session_state['supabase_user']
        saved_key = supabase_manager.load_elevenlabs_api_key()
        if saved_key:
            st.session_state.api_key = saved_key
            # Also update environment variable for this session
            os.environ['ELEVENLABS_API_KEY'] = saved_key

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
    elif feature == "🏷️ Ethereum Voice Tags":
        if ETHEREUM_TAGS_AVAILABLE:
            render_ethereum_tagging()
        else:
            st.error("❌ Ethereum tagging module not available")
    elif feature == "🌍 Dubbing & Translation":
        render_dubbing(studio)
    elif feature == "📊 Analytics & Usage":
        render_analytics(studio)
    elif feature == "⚙️ Advanced Tools":
        render_advanced_tools(studio)
    elif feature == "☁️ Cloud Features":
        render_cloud_integration(studio)

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
