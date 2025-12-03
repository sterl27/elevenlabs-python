# 🎤 ElevenLabs Studio

A comprehensive web application that provides a modern UI for all ElevenLabs API tools and agents. This studio app gives you access to the full power of ElevenLabs' AI voice technology through an intuitive, feature-rich interface, including specialized Ethereum voice persona tagging for blockchain-themed content creation.

![ElevenLabs Studio](https://img.shields.io/badge/ElevenLabs-Studio-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge)

## 🌟 Features

### 🎵 Text-to-Speech
- **Multiple AI Models**: Eleven Multilingual v2, Flash v2.5, Turbo v2.5
- **29+ Languages**: Support for global voice generation
- **Real-time Streaming**: Live audio generation
- **Voice Customization**: Adjust stability, similarity, and style
- **Multiple Output Formats**: MP3, WAV, PCM in various quality levels

### 🎭 Voice Design & Cloning
- **AI Voice Generation**: Create custom voices from text descriptions
- **Instant Voice Cloning**: Clone voices with just a few audio samples
- **Professional Voice Cloning**: High-quality voice reproduction
- **Voice Previews**: Test and compare different voice variations

### 🔄 Speech-to-Speech
- **Voice Conversion**: Transform speech from one voice to another
- **Emotion Preservation**: Maintain original emotion and intonation
- **Background Noise Removal**: Clean audio processing
- **Multiple Input Formats**: Support for various audio file types

### 🎚️ Audio Processing
- **Audio Isolation**: Separate vocals, instruments, and background elements
- **Enhancement Tools**: Improve audio quality and clarity
- **Noise Reduction**: Remove background noise and artifacts
- **Audio Analysis**: Comprehensive audio quality metrics

### 🤖 Conversational AI
- **AI Agent Builder**: Create intelligent voice agents
- **Phone Integration**: Connect agents to phone systems
- **Real-time Chat**: Test agents with interactive chat interface
- **Custom Personalities**: Define agent behavior and responses

### �️ Ethereum Voice Tagging
- **Persona-Based Tagging**: Tag lyrics with Ethereum blockchain persona
- **Deep Tag Taxonomy**: Technical, philosophical, and energy-based voice tags
- **Auto-Embedding**: Automatically inject relevant Ethereum voice tags
- **Tag Validation**: Validate lyrics against comprehensive tag library
- **Voice Style Modifiers**: Apply blockchain-themed voice characteristics
- **Lyric Processing**: Upload, validate, and enhance text for voice generation

### �🌍 Dubbing & Translation
- **Video Dubbing**: Localize video content with AI voices
- **Audio Translation**: Translate speech while preserving voice characteristics
- **Multi-language Support**: Support for major world languages
- **Timeline Synchronization**: Maintain original timing and pacing

### 📊 Analytics & Usage
- **Usage Tracking**: Monitor character usage and limits
- **Performance Metrics**: Analyze generation quality and speed
- **Billing Information**: Track costs and subscription details
- **Historical Data**: View usage trends over time

### ⚙️ Advanced Tools
- **API Testing**: Test individual endpoints and parameters
- **Batch Processing**: Process multiple files or texts at once
- **Webhook Integration**: Set up event notifications
- **Real-time Streaming**: WebSocket-based live audio streaming

### ☁️ Cloud Features (Supabase)
- **Cloud Storage**: Save agent configurations and conversation history
- **Authentication**: Secure user login and account management
- **Database Integration**: Persistent storage for agents and analytics
- **API Key Management**: Securely store and retrieve your ElevenLabs API key
- **Cross-Device Sync**: Access your data from anywhere

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- ElevenLabs API key ([Get one here](https://elevenlabs.io/))
- Supabase Account (Optional, for cloud features)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/elevenlabs/elevenlabs-python.git
   cd elevenlabs-python/studio_app
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   
   **Option A: Python script**
   ```bash
   python run.py
   ```
   
   **Option B: PowerShell (Windows)**
   ```powershell
   .\run.ps1
   ```
   
   **Option C: Direct Streamlit**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**:
   The app will automatically open at `http://localhost:8501`

### First Time Setup

1. **Enter API Key**: In the sidebar, enter your ElevenLabs API key.
2. **Connect Supabase (Optional)**: 
   - Go to "☁️ Cloud Features" in the sidebar.
   - Enter your Supabase URL and Anon Key.
   - Log in or Sign up to enable cloud storage and analytics.
   - Click "💾 Save API Key to Cloud" to securely store your ElevenLabs key.
3. **Start Creating**: Choose any feature from the navigation menu.

## ☁️ Deployment

### Google Cloud Run (Recommended)

This application is ready to be deployed to Google Cloud Run, which offers a generous free tier and automatic scaling.

1.  **Install Google Cloud SDK**: Ensure you have the `gcloud` CLI installed and authenticated.

2.  **Deploy Script**:
    Run the included deployment script (Windows PowerShell):
    ```powershell
    .\deploy.ps1
    ```
    This script will:
    - Check your authentication
    - Set the project context
    - Build and deploy the Docker container

3.  **Environment Variables**:
    For security, API keys are NOT included in the deployment. You must set them in the Cloud Console:
    - Go to [Google Cloud Run Console](https://console.cloud.google.com/run)
    - Select your service (`elevenlabs-studio`)
    - Click **Edit & Deploy New Revision**
    - Under **Variables & Secrets**, add:
        - `ELEVENLABS_API_KEY`
        - `SUPABASE_URL`
        - `SUPABASE_KEY`
    - Click **Deploy**

### Docker

You can also run the application locally using Docker:

1.  **Build the image**:
    ```bash
    docker build -t elevenlabs-studio .
    ```

2.  **Run the container**:
    ```bash
    docker run -p 8080:8080 -e ELEVENLABS_API_KEY=your_key elevenlabs-studio
    ```

## 📋 Usage Guide

### Text-to-Speech
1. Navigate to "🎵 Text-to-Speech"
2. Enter your text in the text area
3. Select a voice and model
4. Adjust voice settings if needed
5. Click "🎤 Generate Speech"
6. Play or download the generated audio

### Voice Design
1. Go to "🎭 Voice Design & Cloning"
2. Choose "🎨 Design Voice" tab
3. Describe your desired voice
4. Adjust generation settings
5. Click "🎨 Generate Voice Previews"
6. Listen to previews and create your favorite

### Speech-to-Speech
1. Select "🔄 Speech-to-Speech"
2. Upload an audio file
3. Choose target voice
4. Configure processing options
5. Click "🔄 Convert Speech"

### Conversational AI
1. Open "🤖 Conversational AI"
2. Use "🤖 Agent Builder" to create an agent
3. Configure voice, personality, and behavior
4. Test with the "💬 Chat Interface"

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the studio_app directory:
```env
ELEVENLABS_API_KEY=your_api_key_here
STREAMLIT_SERVER_PORT=8501
STREAMLIT_THEME_PRIMARY_COLOR=#3ECF8E
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### Config File
Modify `utils.py` to customize default settings:
- Audio quality presets
- Voice settings defaults
- File size limits
- UI preferences

## 🎨 Customization

### Themes
The app uses a centralized `style.css` file for theming. Modify this file to change:
- Color schemes (using CSS variables)
- Layout styling
- Component appearance
- Animations and glassmorphism effects

### Features
Add new features by:
1. Creating a new module in `features/` (e.g., `my_feature.py`)
2. Implementing a `render_my_feature(studio)` function
3. Importing it in `app.py`
4. Adding it to the `feature_options` list in `app.py`

## 📁 Project Structure

studio_app/
├── app.py                 # Main Streamlit application
├── utils.py              # Utility functions and classes
├── supabase_integration.py # Supabase cloud integration
├── style.css             # Custom dark theme and styling
├── requirements.txt      # Python dependencies
├── run.py               # Python launcher script
├── run.ps1              # PowerShell launcher script
├── features/             # Feature modules
│   ├── __init__.py
│   ├── advanced_tools.py
│   ├── analytics.py
│   ├── audio_processing.py
│   ├── cloud_integration.py
│   ├── conversational_ai.py
│   ├── dubbing.py
│   ├── speech_to_speech.py
│   ├── text_to_speech.py
│   └── voice_design.py
├── pages/
│   └── agent_builder.py # Advanced Agent Builder page
├── .streamlit/
│   └── config.toml      # Streamlit configuration
└── README.md            # This file
```

## 🐛 Troubleshooting

### Common Issues

**API Key Issues**
- Ensure your API key is valid and has sufficient credits
- Check if you're using the correct key for your account tier

**Audio Playback Problems**
- Try different browsers (Chrome recommended)
- Check browser audio permissions
- Ensure audio codec support

**Performance Issues**
- Close other browser tabs
- Check internet connection stability
- Consider reducing audio quality for faster processing

**Installation Problems**
- Ensure Python 3.8+ is installed
- Try creating a fresh virtual environment
- Update pip: `python -m pip install --upgrade pip`

### Error Messages

| Error | Solution |
|-------|----------|
| `Import "streamlit" could not be resolved` | Run `pip install streamlit` |
| `Invalid API key` | Check your ElevenLabs API key |
| `Quota exceeded` | Upgrade your ElevenLabs plan |
| `Network error` | Check internet connection |

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
git clone https://github.com/elevenlabs/elevenlabs-python.git
cd elevenlabs-python/studio_app
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🔗 Links

- [ElevenLabs Website](https://elevenlabs.io/)
- [ElevenLabs API Documentation](https://elevenlabs.io/docs)
- [ElevenLabs Python SDK](https://github.com/elevenlabs/elevenlabs-python)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 💬 Support

- **Documentation**: Check the [ElevenLabs API docs](https://elevenlabs.io/docs)
- **Community**: Join the [ElevenLabs Discord](https://discord.gg/elevenlabs)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/elevenlabs/elevenlabs-python/issues)

---

**Made with ❤️ using ElevenLabs AI and Streamlit**
