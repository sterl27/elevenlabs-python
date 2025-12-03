from elevenlabs import generate, play, save, set_api_key, voices

# === Step 1: Set your ElevenLabs API key ===
set_api_key("your-elevenlabs-api-key")  # Replace with your actual API key

# === Step 2: Define voice name and sample prompt ===
VOICE_NAME = "Ethereum"  # Must match the name from your VoiceLab voice or custom upload
TEXT_INPUT = """
Yo, it's Ethereum. Southern roots in my lungs, gospel in my breath.
Every line’s a sermon, wrapped in truth and bass.
Ain’t just rap—it’s revelation.
"""

# === Step 3: List available voices to confirm if Ethereum exists ===
available_voices = Voices.from_api()
available_voices = voices()
voice_ids = {v.name: v.voice_id for v in available_voices}
if VOICE_NAME not in voice_ids:
    raise ValueError(f"Voice '{VOICE_NAME}' not found. Available voices: {list(voice_ids.keys())}")
# === Step 4: Generate speech ===
audio = generate(
    text=TEXT_INPUT,
    voice=voice_ids[VOICE_NAME],
    model="eleven_monolingual_v1"  # or use "eleven_multilingual_v2" if cross-language support needed
)

# === Step 5: Play and save the output ===
play(audio)
save(audio, f"{VOICE_NAME}_sample_output.wav")

print(f"Audio generated and saved as '{VOICE_NAME}_sample_output.wav'")
