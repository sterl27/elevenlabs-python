import base64
import os
import streamlit as st
from utils import UIComponents

def render_voice_design(studio):
    """Render Voice Design & Cloning interface"""
    UIComponents.render_section_header("🎭 Voice Design & Cloning", "Create unique AI voices or clone existing ones")
    
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
