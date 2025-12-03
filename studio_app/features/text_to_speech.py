import base64
import streamlit as st
from elevenlabs.types import VoiceSettings
from utils import UIComponents

def render_text_to_speech(studio):
    """Render Text-to-Speech interface"""
    UIComponents.render_section_header("🎵 Text-to-Speech", "Convert text to natural-sounding speech using advanced AI models")
    
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
