import streamlit as st
from utils import UIComponents

def render_speech_to_speech(studio):
    """Render Speech-to-Speech interface"""
    UIComponents.render_section_header("🔄 Speech-to-Speech Conversion", "Convert speech from one voice to another while preserving emotion and intonation")
    
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
