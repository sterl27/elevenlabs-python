"""
ElevenLabs Studio Demo Script
============================

This script demonstrates how to use the ElevenLabs Studio app programmatically
and shows examples of all the main features.
"""

import os
import sys
from pathlib import Path

# Add the studio app directory to Python path
studio_dir = Path(__file__).parent
sys.path.insert(0, str(studio_dir))

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs.types import VoiceSettings
except ImportError:
    print("❌ ElevenLabs package not installed. Run: pip install elevenlabs")
    sys.exit(1)

def demo_text_to_speech():
    """Demonstrate text-to-speech functionality"""
    print("\n🎵 Text-to-Speech Demo")
    print("=" * 40)
    
    # Initialize client (requires API key)
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("⚠️  No API key found. Set ELEVENLABS_API_KEY environment variable.")
        return
    
    try:
        client = ElevenLabs(api_key=api_key)
        
        # Get available voices
        print("📋 Fetching available voices...")
        voices_response = client.voices.search()
        voices = voices_response.voices
        print(f"✅ Found {len(voices)} voices")
        
        # Show first few voices
        for i, voice in enumerate(voices[:3]):
            print(f"  {i+1}. {voice.name} (ID: {voice.voice_id})")
        
        # Generate speech with first voice
        if voices:
            voice = voices[0]
            text = "Welcome to ElevenLabs Studio! This is a demonstration of our text-to-speech capabilities."
            
            print(f"\n🎤 Generating speech with voice: {voice.name}")
            print(f"📝 Text: {text}")
            
            voice_settings = VoiceSettings(
                stability=0.75,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            )
            
            audio = client.text_to_speech.convert(
                text=text,
                voice_id=voice.voice_id,
                model_id="eleven_multilingual_v2",
                voice_settings=voice_settings,
                output_format="mp3_44100_128"
            )
            
            # Save audio to file
            audio_bytes = b''.join(audio)
            output_file = "demo_output.mp3"
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            
            print(f"✅ Audio generated and saved to: {output_file}")
            print(f"📊 Audio size: {len(audio_bytes)} bytes")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def demo_voice_design():
    """Demonstrate voice design functionality"""
    print("\n🎭 Voice Design Demo")
    print("=" * 40)
    
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("⚠️  No API key found. Set ELEVENLABS_API_KEY environment variable.")
        return
    
    try:
        client = ElevenLabs(api_key=api_key)
        
        voice_description = "A warm, friendly female voice with a slight British accent, perfect for audiobooks"
        
        print("🎨 Generating voice preview...")
        print(f"📝 Description: {voice_description}")
        
        response = client.text_to_voice.create_previews(
            voice_description=voice_description,
            output_format="mp3_44100_128",
            auto_generate_text=True,
            loudness=0.0,
            quality=0.75,
            seed=42,
            guidance_scale=1.0
        )
        
        print(f"✅ Generated {len(response.previews)} voice previews")
        
        for i, preview in enumerate(response.previews):
            print(f"  Preview {i+1}: Voice ID {preview.generated_voice_id}")
            
            # Save preview audio
            import base64
            audio_bytes = base64.b64decode(preview.audio_base_64)
            output_file = f"voice_preview_{i+1}.mp3"
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            print(f"    Saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def demo_models_and_features():
    """Demonstrate available models and features"""
    print("\n🧠 Models & Features Demo")
    print("=" * 40)
    
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("⚠️  No API key found. Set ELEVENLABS_API_KEY environment variable.")
        return
    
    try:
        client = ElevenLabs(api_key=api_key)
        
        # Get available models
        print("📋 Fetching available models...")
        models_response = client.models.list()
        models = models_response  # models_response is already a list of Model objects
        print(f"✅ Found {len(models)} models")
        
        # Show models and their capabilities
        for model in models:
            print(f"\n  📦 {model.name}")
            print(f"     Description: {model.description}")
            print(f"     Model ID: {model.model_id}")
            
            # Check capabilities
            capabilities = []
            if hasattr(model, 'can_do_text_to_speech') and model.can_do_text_to_speech:
                capabilities.append("Text-to-Speech")
            if hasattr(model, 'can_do_voice_conversion') and model.can_do_voice_conversion:
                capabilities.append("Voice Conversion")
            if hasattr(model, 'can_do_streaming') and model.can_do_streaming:
                capabilities.append("Streaming")
            
            if capabilities:
                print(f"     Capabilities: {', '.join(capabilities)}")
        
        # Show usage information
        print("\n💳 Usage Information")
        try:
            usage = client.usage.get_usage()
            print(f"  Characters used: {usage.characters_used:,}")
            print(f"  Character limit: {usage.character_limit:,}")
            remaining = usage.character_limit - usage.characters_used
            print(f"  Remaining: {remaining:,} ({(remaining/usage.character_limit*100):.1f}%)")
        except Exception as e:
            print(f"  ⚠️  Could not fetch usage data: {str(e)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main demo function"""
    print("🎤 ElevenLabs Studio Demo")
    print("=" * 50)
    print("This demo shows the capabilities of the ElevenLabs Studio app.")
    print("Make sure you have set your ELEVENLABS_API_KEY environment variable.")
    print()
    
    # Check for API key
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ No API key found!")
        print("Please set your API key:")
        print("  Windows: set ELEVENLABS_API_KEY=your_key_here")
        print("  macOS/Linux: export ELEVENLABS_API_KEY=your_key_here")
        print("  Or create a .env file with: ELEVENLABS_API_KEY=your_key_here")
        return
    
    print(f"✅ API key found: {api_key[:8]}...")
    
    # Run demos
    try:
        demo_models_and_features()
        demo_text_to_speech()
        demo_voice_design()
        
        print("\n🎉 Demo completed!")
        print("\nTo run the full Studio app:")
        print("  1. cd studio_app")
        print("  2. python run.py")
        print("  3. Open http://localhost:8501 in your browser")
        
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")

if __name__ == "__main__":
    main()
