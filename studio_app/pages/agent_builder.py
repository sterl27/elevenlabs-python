"""
ElevenLabs Studio - Conversational AI Agent Builder
Advanced agent creation and management with full configuration options
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict

import streamlit as st

# Import ElevenLabs components
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs.types import (
        AgentConfig,
        AgentPlatformSettingsRequestModel,
        AsrConversationalConfig,
        ConversationalConfig,
        ConversationConfig,
        LanguagePresetOutput,
        ToolRequestModel,
        TtsConversationalConfigOutput,
        TurnConfig,
    )
except ImportError as e:
    st.error(f"ElevenLabs import error: {e}")
    st.stop()

def load_css():
    """Load custom CSS for the agent builder"""
    # Load main style.css
    try:
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback if running from pages directory
        try:
            with open('../style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except:
            pass
            
    # Agent Builder Specific Styles
    st.markdown("""
    <style>
    /* Agent Builder Specific Styles */
    .agent-builder-container {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-md);
    }
    
    .config-section {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(12px);
    }
    
    .agent-card {
        background: linear-gradient(145deg, var(--bg-surface), rgba(62, 207, 142, 0.05));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        border-color: var(--primary);
        box-shadow: var(--shadow-glow);
        transform: translateY(-2px);
    }
    
    .tool-card {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    
    .tool-card:hover {
        border-color: var(--primary);
        background: rgba(62, 207, 142, 0.05);
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .status-active {
        background: rgba(62, 207, 142, 0.1);
        color: var(--primary);
        border: 1px solid var(--primary);
    }
    
    .status-inactive {
        background: rgba(161, 161, 170, 0.1);
        color: var(--text-muted);
        border: 1px solid var(--border);
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.1);
        color: #EF4444;
        border: 1px solid #EF4444;
    }
    
    .agent-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
    }
    
    .config-preview {
        background: #000000;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #e2e8f0;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .tool-builder {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .test-interface {
        background: linear-gradient(145deg, var(--bg-surface), rgba(62, 207, 142, 0.03));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .conversation-bubble {
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        max-width: 80%;
        box-shadow: var(--shadow-sm);
    }
    
    .user-bubble {
        margin-left: auto;
        background: var(--gradient-primary);
        color: white;
        border: none;
    }
    
    .agent-bubble {
        margin-right: auto;
        background: var(--bg-card);
        border: 1px solid var(--border);
    }
    </style>
    """, unsafe_allow_html=True)

class AgentBuilder:
    """Comprehensive agent builder with full configuration management"""
    
    def __init__(self):
        self.client = None
        self.init_client()
        self.init_session_state()
    
    def init_client(self):
        """Initialize ElevenLabs client"""
        try:
            api_key = st.session_state.get('elevenlabs_api_key')
            if api_key:
                self.client = ElevenLabs(api_key=api_key)
        except Exception as e:
            st.error(f"Failed to initialize client: {e}")
    
    def init_session_state(self):
        """Initialize session state for agent builder"""
        if 'agents' not in st.session_state:
            st.session_state.agents = {}
        if 'current_agent_config' not in st.session_state:
            st.session_state.current_agent_config = self.get_default_config()
        if 'available_tools' not in st.session_state:
            st.session_state.available_tools = []
        if 'custom_tools' not in st.session_state:
            st.session_state.custom_tools = []
        if 'test_conversation' not in st.session_state:
            st.session_state.test_conversation = []
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default agent configuration"""
        return {
            'name': 'New Agent',
            'description': 'A conversational AI agent',
            'tags': [],
            'conversation': {
                'system_prompt': 'You are a helpful AI assistant.',
                'first_message': 'Hello! How can I help you today?',
                'language': 'en',
                'max_duration_seconds': 600,
                'time_out_seconds': 30
            },
            'voice': {
                'voice_id': 'JBFqnCBsd6RMkjVDRZzb',
                'model_id': 'eleven_turbo_v2_5',
                'stability': 0.5,
                'similarity_boost': 0.75,
                'style': 0.0,
                'use_speaker_boost': True
            },
            'asr': {
                'provider': 'elevenlabs',
                'language': 'en',
                'model': 'nova-2'
            },
            'turn_detection': {
                'type': 'server_vad',
                'threshold': 0.5,
                'prefix_padding_ms': 300,
                'silence_duration_ms': 1000
            },
            'tools': [],
            'knowledge_base': {
                'enabled': False,
                'files': []
            },
            'platform_settings': {
                'webhook_url': '',
                'max_concurrent_calls': 10
            }
        }
    
    def render_header(self):
        """Render the agent builder header"""
        st.markdown("""
        <div class="agent-builder-container">
            <h1 style="color: var(--text-main); margin-bottom: 0.5rem;">
                🤖 <span class="gradient-text">Conversational AI Agent Builder</span>
            </h1>
            <p style="color: var(--text-muted); font-size: 1.1rem; margin-bottom: 2rem;">
                Create, configure, and deploy intelligent conversational agents with advanced AI capabilities
            </p>
            
            <div class="agent-metrics">
                <div class="metric-card">
                    <div style="color: var(--primary); font-size: 1.5rem; font-weight: bold;">
                        {agents_count}
                    </div>
                    <div style="color: var(--text-muted); font-size: 0.9rem;">
                        Active Agents
                    </div>
                </div>
                <div class="metric-card">
                    <div style="color: var(--primary); font-size: 1.5rem; font-weight: bold;">
                        {tools_count}
                    </div>
                    <div style="color: var(--text-muted); font-size: 0.9rem;">
                        Available Tools
                    </div>
                </div>
                <div class="metric-card">
                    <div style="color: var(--primary); font-size: 1.5rem; font-weight: bold;">
                        {conversations_count}
                    </div>
                    <div style="color: var(--text-muted); font-size: 0.9rem;">
                        Test Conversations
                    </div>
                </div>
            </div>
        </div>
        """.format(
            agents_count=len(st.session_state.agents),
            tools_count=len(st.session_state.available_tools) + len(st.session_state.custom_tools),
            conversations_count=len(st.session_state.test_conversation)
        ), unsafe_allow_html=True)
    
    def render_agent_list(self):
        """Render list of existing agents"""
        st.markdown('<div class="section-header">🎯 Your Agents</div>', unsafe_allow_html=True)
        
        if not st.session_state.agents:
            st.info("No agents created yet. Use the builder below to create your first agent!")
            return
        
        for agent_id, agent_data in st.session_state.agents.items():
            with st.container():
                tags_html = ''.join([f'<span class="status-badge status-active">{tag}</span>' 
                                     for tag in agent_data.get('tags', [])])
                st.markdown(f"""
                <div class="agent-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="color: var(--text-main); margin: 0;">{agent_data['name']}</h3>
                        <div>
                            <span class="status-badge status-active">Active</span>
                        </div>
                    </div>
                    <p style="color: var(--text-muted); margin-bottom: 1rem;">
                        {agent_data.get('description', 'No description')}
                    </p>
                    <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                        {tags_html}
                    </div>
                    <div style="display: flex; gap: 1rem; align-items: center;">
                        <small style="color: var(--text-muted);">
                            Created: {agent_data.get('created_at', 'Unknown')}
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button(f"Edit {agent_data['name']}", key=f"edit_{agent_id}"):
                        st.session_state.current_agent_config = agent_data
                        st.rerun()
                with col2:
                    if st.button(f"Test {agent_data['name']}", key=f"test_{agent_id}"):
                        st.session_state.testing_agent = agent_id
                        st.rerun()
                with col3:
                    if st.button(f"Deploy {agent_data['name']}", key=f"deploy_{agent_id}"):
                        self.deploy_agent(agent_id, agent_data)
                with col4:
                    if st.button(f"Delete {agent_data['name']}", key=f"delete_{agent_id}"):
                        del st.session_state.agents[agent_id]
                        st.rerun()
    
    def render_agent_configurator(self):
        """Render the main agent configuration interface"""
        st.markdown('<div class="section-header">⚙️ Agent Configuration</div>', unsafe_allow_html=True)
        
        # Configuration tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎭 Basic Settings", 
            "🗣️ Voice & Speech", 
            "🧠 Conversation", 
            "🛠️ Tools & Actions", 
            "📚 Knowledge Base", 
            "🔧 Advanced"
        ])
        
        with tab1:
            self.render_basic_settings()
        
        with tab2:
            self.render_voice_settings()
        
        with tab3:
            self.render_conversation_settings()
        
        with tab4:
            self.render_tools_settings()
        
        with tab5:
            self.render_knowledge_base_settings()
        
        with tab6:
            self.render_advanced_settings()
    
    def render_basic_settings(self):
        """Render basic agent settings"""
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        
        config = st.session_state.current_agent_config
        
        col1, col2 = st.columns(2)
        with col1:
            config['name'] = st.text_input(
                "Agent Name",
                value=config.get('name', ''),
                help="A unique name for your agent"
            )
            
            config['description'] = st.text_area(
                "Description",
                value=config.get('description', ''),
                help="Describe what your agent does"
            )
        
        with col2:
            # Tags management
            st.subheader("Tags")
            current_tags = config.get('tags', [])
            
            new_tag = st.text_input("Add Tag", placeholder="e.g., customer-service")
            if st.button("Add Tag") and new_tag and new_tag not in current_tags:
                current_tags.append(new_tag)
                config['tags'] = current_tags
                st.rerun()
            
            # Display current tags
            if current_tags:
                st.write("Current tags:")
                for i, tag in enumerate(current_tags):
                    col_tag, col_remove = st.columns([3, 1])
                    with col_tag:
                        st.write(f"• {tag}")
                    with col_remove:
                        if st.button("❌", key=f"remove_tag_{i}"):
                            current_tags.remove(tag)
                            config['tags'] = current_tags
                            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_voice_settings(self):
        """Render voice and TTS settings"""
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        
        config = st.session_state.current_agent_config
        voice_config = config.setdefault('voice', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎤 Voice Selection")
            
            # Voice selection
            if self.client:
                try:
                    voices_response = self.client.voices.search()
                    voices = voices_response.voices if hasattr(voices_response, 'voices') else []
                    voice_options = {f"{voice.name} ({voice.voice_id})": voice.voice_id 
                                   for voice in voices[:20]}  # Limit to first 20
                    
                    selected_voice = st.selectbox(
                        "Select Voice",
                        options=list(voice_options.keys()),
                        index=0 if voice_options else 0,
                        help="Choose the voice for your agent"
                    )
                    
                    if selected_voice:
                        voice_config['voice_id'] = voice_options[selected_voice]
                        
                except Exception as e:
                    st.warning(f"Could not load voices: {e}")
                    voice_config['voice_id'] = st.text_input(
                        "Voice ID",
                        value=voice_config.get('voice_id', 'JBFqnCBsd6RMkjVDRZzb'),
                        help="Enter a voice ID manually"
                    )
            else:
                voice_config['voice_id'] = st.text_input(
                    "Voice ID",
                    value=voice_config.get('voice_id', 'JBFqnCBsd6RMkjVDRZzb'),
                    help="Enter a voice ID (requires API key)"
                )
            
            # Model selection
            voice_config['model_id'] = st.selectbox(
                "TTS Model",
                options=[
                    'eleven_multilingual_v2',
                    'eleven_turbo_v2_5',
                    'eleven_flash_v2_5',
                    'eleven_monolingual_v1'
                ],
                index=1,
                help="Choose the text-to-speech model"
            )
        
        with col2:
            st.subheader("🎛️ Voice Settings")
            
            voice_config['stability'] = st.slider(
                "Stability",
                min_value=0.0,
                max_value=1.0,
                value=voice_config.get('stability', 0.5),
                step=0.05,
                help="Higher values make the voice more consistent"
            )
            
            voice_config['similarity_boost'] = st.slider(
                "Similarity Boost",
                min_value=0.0,
                max_value=1.0,
                value=voice_config.get('similarity_boost', 0.75),
                step=0.05,
                help="Higher values make the voice more similar to the original"
            )
            
            voice_config['style'] = st.slider(
                "Style",
                min_value=0.0,
                max_value=1.0,
                value=voice_config.get('style', 0.0),
                step=0.05,
                help="Style exaggeration (only available for certain voices)"
            )
            
            voice_config['use_speaker_boost'] = st.checkbox(
                "Use Speaker Boost",
                value=voice_config.get('use_speaker_boost', True),
                help="Enhance voice clarity and quality"
            )
        
        # ASR Settings
        st.markdown("---")
        st.subheader("🎧 Speech Recognition (ASR)")
        
        asr_config = config.setdefault('asr', {})
        
        col_asr1, col_asr2 = st.columns(2)
        with col_asr1:
            asr_config['provider'] = st.selectbox(
                "ASR Provider",
                options=['elevenlabs', 'openai'],
                index=0,
                help="Choose the speech recognition provider"
            )
            
            asr_config['language'] = st.selectbox(
                "Language",
                options=['en', 'es', 'fr', 'de', 'it', 'pt', 'zh', 'ja', 'ko'],
                index=0,
                help="Primary language for speech recognition"
            )
        
        with col_asr2:
            if asr_config.get('provider') == 'openai':
                asr_config['model'] = st.selectbox(
                    "ASR Model",
                    options=['whisper-1'],
                    index=0
                )
            else:
                asr_config['model'] = st.selectbox(
                    "ASR Model",
                    options=['nova-2', 'nova-1'],
                    index=0
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_conversation_settings(self):
        """Render conversation and AI settings"""
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        
        config = st.session_state.current_agent_config
        conv_config = config.setdefault('conversation', {})
        
        st.subheader("💬 Conversation Setup")
        
        conv_config['system_prompt'] = st.text_area(
            "System Prompt",
            value=conv_config.get('system_prompt', 'You are a helpful AI assistant.'),
            height=150,
            help="Define your agent's personality and behavior"
        )
        
        conv_config['first_message'] = st.text_input(
            "First Message",
            value=conv_config.get('first_message', 'Hello! How can I help you today?'),
            help="The agent's opening message"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            conv_config['language'] = st.selectbox(
                "Primary Language",
                options=['en', 'es', 'fr', 'de', 'it', 'pt', 'zh', 'ja', 'ko'],
                index=0,
                help="Default conversation language"
            )
            
            conv_config['max_duration_seconds'] = st.number_input(
                "Max Duration (seconds)",
                min_value=60,
                max_value=3600,
                value=conv_config.get('max_duration_seconds', 600),
                help="Maximum conversation duration"
            )
        
        with col2:
            conv_config['time_out_seconds'] = st.number_input(
                "Timeout (seconds)",
                min_value=10,
                max_value=300,
                value=conv_config.get('time_out_seconds', 30),
                help="Conversation timeout period"
            )
        
        # Turn Detection
        st.markdown("---")
        st.subheader("🔄 Turn Detection")
        
        turn_config = config.setdefault('turn_detection', {})
        
        col_turn1, col_turn2 = st.columns(2)
        
        with col_turn1:
            turn_config['type'] = st.selectbox(
                "Detection Type",
                options=['server_vad', 'none'],
                index=0,
                help="Method for detecting when user stops speaking"
            )
            
            if turn_config['type'] == 'server_vad':
                turn_config['threshold'] = st.slider(
                    "VAD Threshold",
                    min_value=0.0,
                    max_value=1.0,
                    value=turn_config.get('threshold', 0.5),
                    step=0.05,
                    help="Voice activity detection sensitivity"
                )
        
        with col_turn2:
            if turn_config['type'] == 'server_vad':
                turn_config['prefix_padding_ms'] = st.number_input(
                    "Prefix Padding (ms)",
                    min_value=0,
                    max_value=1000,
                    value=turn_config.get('prefix_padding_ms', 300),
                    help="Audio padding before speech detection"
                )
                
                turn_config['silence_duration_ms'] = st.number_input(
                    "Silence Duration (ms)",
                    min_value=500,
                    max_value=5000,
                    value=turn_config.get('silence_duration_ms', 1000),
                    help="Silence duration to trigger turn end"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_tools_settings(self):
        """Render tools and actions configuration"""
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        
        st.subheader("🛠️ Tools & Actions")
        
        # Load available tools
        self.load_available_tools()
        
        # Tool tabs
        tool_tab1, tool_tab2, tool_tab3 = st.tabs(["Available Tools", "Custom Tools", "Tool Builder"])
        
        with tool_tab1:
            self.render_available_tools()
        
        with tool_tab2:
            self.render_custom_tools()
        
        with tool_tab3:
            self.render_tool_builder()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_available_tools(self):
        """Render available tools from ElevenLabs"""
        if not st.session_state.available_tools:
            st.info("No tools available. Connect with API key to load tools.")
            return
        
        config = st.session_state.current_agent_config
        selected_tools = config.setdefault('tools', [])
        
        st.write("Select tools to add to your agent:")
        
        for tool in st.session_state.available_tools:
            tool_id = tool.get('tool_id', tool.get('id', ''))
            tool_name = tool.get('name', 'Unknown Tool')
            tool_desc = tool.get('description', 'No description available')
            
            with st.container():
                st.markdown(f"""
                <div class="tool-card">
                    <h4 style="color: var(--text-main); margin: 0 0 0.5rem 0;">{tool_name}</h4>
                    <p style="color: var(--text-muted); margin: 0 0 1rem 0; font-size: 0.9rem;">
                        {tool_desc}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                is_selected = any(t.get('tool_id') == tool_id for t in selected_tools)
                
                if st.checkbox(f"Use {tool_name}", value=is_selected, key=f"tool_{tool_id}"):
                    if not is_selected:
                        selected_tools.append({
                            'tool_id': tool_id,
                            'name': tool_name,
                            'description': tool_desc,
                            'type': 'elevenlabs'
                        })
                        config['tools'] = selected_tools
                else:
                    if is_selected:
                        selected_tools[:] = [t for t in selected_tools if t.get('tool_id') != tool_id]
                        config['tools'] = selected_tools
    
    def render_custom_tools(self):
        """Render custom tools management"""
        st.write("Custom tools created in this session:")
        
        config = st.session_state.current_agent_config
        selected_tools = config.setdefault('tools', [])
        
        for i, tool in enumerate(st.session_state.custom_tools):
            with st.container():
                st.markdown(f"""
                <div class="tool-card">
                    <h4 style="color: var(--text-main); margin: 0 0 0.5rem 0;">{tool['name']}</h4>
                    <p style="color: var(--text-muted); margin: 0 0 1rem 0; font-size: 0.9rem;">
                        {tool['description']}
                    </p>
                    <div style="display: flex; gap: 0.5rem;">
                        <span class="status-badge status-active">Custom</span>
                        <span class="status-badge status-active">{tool.get('type', 'function')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    is_selected = any(t.get('custom_id') == tool.get('id') for t in selected_tools)
                    if st.checkbox(f"Use {tool['name']}", value=is_selected, key=f"custom_tool_{i}"):
                        if not is_selected:
                            selected_tools.append({
                                'custom_id': tool.get('id'),
                                'name': tool['name'],
                                'description': tool['description'],
                                'type': 'custom',
                                'config': tool
                            })
                            config['tools'] = selected_tools
                    else:
                        if is_selected:
                            selected_tools[:] = [t for t in selected_tools 
                                               if t.get('custom_id') != tool.get('id')]
                            config['tools'] = selected_tools
                
                with col2:
                    if st.button(f"Delete {tool['name']}", key=f"delete_custom_{i}"):
                        st.session_state.custom_tools.pop(i)
                        st.rerun()
    
    def render_tool_builder(self):
        """Render tool builder interface"""
        st.markdown('<div class="tool-builder">', unsafe_allow_html=True)
        
        st.subheader("🔧 Create Custom Tool")
        
        with st.form("tool_builder_form"):
            tool_name = st.text_input("Tool Name", placeholder="e.g., Weather Checker")
            tool_description = st.text_area(
                "Tool Description", 
                placeholder="What does this tool do?",
                help="Describe the tool's functionality for the AI agent"
            )
            
            tool_type = st.selectbox(
                "Tool Type",
                options=["function", "webhook", "api_call"],
                help="Type of tool to create"
            )
            
            # Initialize all possible variables to avoid unbound errors
            function_code = ""
            parameters_json = ""
            webhook_url = ""
            http_method = ""
            headers_json = ""
            api_url = ""
            api_method = ""
            api_headers = ""
            api_params = ""

            if tool_type == "function":
                st.subheader("Function Configuration")
                function_code = st.text_area(
                    "Function Code (Python)",
                    placeholder="""def my_function(param1, param2):
    # Your function logic here
    return result""",
                    height=200
                )
                
                parameters_json = st.text_area(
                    "Parameters Schema (JSON)",
                    placeholder="""{
    "param1": {
        "type": "string",
        "description": "Description of param1"
    },
    "param2": {
        "type": "number",
        "description": "Description of param2"
    }
}""",
                    height=150
                )
            
            elif tool_type == "webhook":
                st.subheader("Webhook Configuration")
                webhook_url = st.text_input("Webhook URL", placeholder="https://your-api.com/webhook")
                http_method = st.selectbox("HTTP Method", options=["POST", "GET", "PUT", "DELETE"])
                headers_json = st.text_area(
                    "Headers (JSON)",
                    placeholder='{"Authorization": "Bearer token", "Content-Type": "application/json"}',
                    height=100
                )
            
            elif tool_type == "api_call":
                st.subheader("API Call Configuration")
                api_url = st.text_input("API Endpoint", placeholder="https://api.example.com/data")
                api_method = st.selectbox("HTTP Method", options=["GET", "POST", "PUT", "DELETE"])
                api_headers = st.text_area(
                    "Headers (JSON)",
                    placeholder='{"Authorization": "Bearer token"}',
                    height=100
                )
                api_params = st.text_area(
                    "Request Parameters Schema (JSON)",
                    placeholder='{"query": {"type": "string", "description": "Search query"}}',
                    height=100
                )
            
            expects_response = st.checkbox(
                "Tool Expects Response",
                value=True,
                help="Whether the tool returns data that the agent should use"
            )
            
            if st.form_submit_button("Create Tool", type="primary"):
                if tool_name and tool_description:
                    tool_config = {
                        'id': str(uuid.uuid4()),
                        'name': tool_name,
                        'description': tool_description,
                        'type': tool_type,
                        'expects_response': expects_response,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    if tool_type == "function":
                        tool_config.update({
                            'function_code': function_code,
                            'parameters': parameters_json
                        })
                    elif tool_type == "webhook":
                        tool_config.update({
                            'webhook_url': webhook_url,
                            'http_method': http_method,
                            'headers': headers_json
                        })
                    elif tool_type == "api_call":
                        tool_config.update({
                            'api_url': api_url,
                            'api_method': api_method,
                            'api_headers': api_headers,
                            'api_parameters': api_params
                        })
                    
                    st.session_state.custom_tools.append(tool_config)
                    st.success(f"Tool '{tool_name}' created successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in tool name and description.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_knowledge_base_settings(self):
        """Render knowledge base configuration"""
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        
        config = st.session_state.current_agent_config
        kb_config = config.setdefault('knowledge_base', {})
        
        st.subheader("📚 Knowledge Base")
        
        kb_config['enabled'] = st.checkbox(
            "Enable Knowledge Base",
            value=kb_config.get('enabled', False),
            help="Allow your agent to access custom knowledge"
        )
        
        if kb_config['enabled']:
            st.subheader("📄 Knowledge Sources")
            
            # File upload
            uploaded_files = st.file_uploader(
                "Upload Knowledge Files",
                type=['txt', 'pdf', 'docx', 'md'],
                accept_multiple_files=True,
                help="Upload documents for your agent to reference"
            )
            
            if uploaded_files:
                kb_files = kb_config.setdefault('files', [])
                for file in uploaded_files:
                    file_info = {
                        'name': file.name,
                        'type': file.type,
                        'size': file.size,
                        'content': file.read().decode('utf-8') if file.type == 'text/plain' else None
                    }
                    
                    # Check if file already exists
                    if not any(f['name'] == file.name for f in kb_files):
                        kb_files.append(file_info)
                        st.success(f"Added {file.name} to knowledge base")
                
                kb_config['files'] = kb_files
            
            # Display current files
            if kb_config.get('files'):
                st.subheader("Current Knowledge Files")
                for i, file_info in enumerate(kb_config['files']):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"📄 {file_info['name']}")
                    with col2:
                        st.write(f"{file_info.get('size', 0)} bytes")
                    with col3:
                        if st.button("Remove", key=f"remove_kb_file_{i}"):
                            kb_config['files'].pop(i)
                            st.rerun()
            
            # Web scraping
            st.markdown("---")
            st.subheader("🌐 Web Knowledge")
            
            url_input = st.text_input(
                "Add URL to Knowledge Base",
                placeholder="https://example.com/knowledge-page"
            )
            
            if st.button("Add URL") and url_input:
                # Placeholder for web scraping functionality
                st.info("Web scraping feature coming soon!")
            
            # Knowledge base settings
            st.markdown("---")
            st.subheader("⚙️ Knowledge Base Settings")
            
            col1, col2 = st.columns(2)
            with col1:
                kb_config['chunk_size'] = st.number_input(
                    "Chunk Size",
                    min_value=100,
                    max_value=2000,
                    value=kb_config.get('chunk_size', 500),
                    help="Size of text chunks for processing"
                )
            
            with col2:
                kb_config['similarity_threshold'] = st.slider(
                    "Similarity Threshold",
                    min_value=0.0,
                    max_value=1.0,
                    value=kb_config.get('similarity_threshold', 0.7),
                    step=0.05,
                    help="Minimum similarity for knowledge retrieval"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_advanced_settings(self):
        """Render advanced configuration options"""
        st.markdown('<div class="config-section">', unsafe_allow_html=True)
        
        config = st.session_state.current_agent_config
        platform_config = config.setdefault('platform_settings', {})
        
        st.subheader("🔧 Platform Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            platform_config['webhook_url'] = st.text_input(
                "Webhook URL",
                value=platform_config.get('webhook_url', ''),
                help="URL to receive conversation events"
            )
            
            platform_config['max_concurrent_calls'] = st.number_input(
                "Max Concurrent Calls",
                min_value=1,
                max_value=100,
                value=platform_config.get('max_concurrent_calls', 10),
                help="Maximum number of simultaneous conversations"
            )
        
        with col2:
            platform_config['enable_interruptions'] = st.checkbox(
                "Enable Interruptions",
                value=platform_config.get('enable_interruptions', True),
                help="Allow users to interrupt the agent"
            )
            
            platform_config['enable_backchannel'] = st.checkbox(
                "Enable Backchannel",
                value=platform_config.get('enable_backchannel', False),
                help="Enable natural conversation responses"
            )
        
        # Security settings
        st.markdown("---")
        st.subheader("🔒 Security & Privacy")
        
        security_config = config.setdefault('security', {})
        
        security_config['require_auth'] = st.checkbox(
            "Require Authentication",
            value=security_config.get('require_auth', False),
            help="Require user authentication for conversations"
        )
        
        security_config['log_conversations'] = st.checkbox(
            "Log Conversations",
            value=security_config.get('log_conversations', True),
            help="Store conversation logs for analysis"
        )
        
        security_config['data_retention_days'] = st.number_input(
            "Data Retention (Days)",
            min_value=1,
            max_value=365,
            value=security_config.get('data_retention_days', 30),
            help="How long to keep conversation data"
        )
        
        # Configuration preview
        st.markdown("---")
        st.subheader("📋 Configuration Preview")
        
        if st.button("Show Configuration JSON"):
            st.markdown('<div class="config-preview">', unsafe_allow_html=True)
            st.code(json.dumps(config, indent=2), language='json')
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_action_buttons(self):
        """Render main action buttons"""
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Agent", type="primary"):
                self.save_agent()
        
        with col2:
            if st.button("🧪 Test Agent"):
                st.session_state.show_test_interface = True
                st.rerun()
        
        with col3:
            if st.button("🚀 Deploy Agent"):
                self.deploy_current_agent()
        
        with col4:
            if st.button("📤 Export Config"):
                self.export_agent_config()
    
    def render_test_interface(self):
        """Render agent testing interface"""
        if not st.session_state.get('show_test_interface', False):
            return
        
        st.markdown('<div class="section-header">🧪 Agent Testing</div>', unsafe_allow_html=True)
        st.markdown('<div class="test-interface">', unsafe_allow_html=True)
        
        # Test conversation interface
        st.subheader("💬 Test Conversation")
        
        # Display conversation history
        if st.session_state.test_conversation:
            for message in st.session_state.test_conversation:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="conversation-bubble user-bubble">
                        <strong>You:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="conversation-bubble agent-bubble">
                        <strong>Agent:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Test input
        with st.form("test_message_form"):
            test_message = st.text_input("Send a test message:", placeholder="Hello, how are you?")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("Send Message", type="primary"):
                    if test_message:
                        # Add user message
                        st.session_state.test_conversation.append({
                            'role': 'user',
                            'content': test_message,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Simulate agent response
                        agent_response = self.simulate_agent_response(test_message)
                        st.session_state.test_conversation.append({
                            'role': 'agent',
                            'content': agent_response,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        st.rerun()
            
            with col2:
                if st.form_submit_button("Clear Conversation"):
                    st.session_state.test_conversation = []
                    st.rerun()
        
        # Test controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Test Voice"):
                st.info("Voice testing requires audio integration")
        
        with col2:
            if st.button("📊 View Analytics"):
                self.show_test_analytics()
        
        if st.button("❌ Close Test Interface"):
            st.session_state.show_test_interface = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def load_available_tools(self):
        """Load available tools from ElevenLabs API"""
        if not self.client:
            return
        
        try:
            tools_response = self.client.conversational_ai.tools.list()
            if hasattr(tools_response, 'tools'):
                st.session_state.available_tools = tools_response.tools
            else:
                st.session_state.available_tools = []
        except Exception as e:
            st.warning(f"Could not load tools: {e}")
            st.session_state.available_tools = []
    
    def save_agent(self):
        """Save the current agent configuration"""
        config = st.session_state.current_agent_config
        agent_id = config.get('id', str(uuid.uuid4()))
        
        # Add metadata
        config['id'] = agent_id
        config['created_at'] = config.get('created_at', datetime.now().isoformat())
        config['updated_at'] = datetime.now().isoformat()
        
        # Save to session state
        st.session_state.agents[agent_id] = config.copy()
        
        st.success(f"Agent '{config['name']}' saved successfully!")
    
    def deploy_agent(self, agent_id: str, agent_data: Dict[str, Any]):
        """Deploy an agent to ElevenLabs"""
        if not self.client:
            st.error("Please connect with API key to deploy agents")
            return
        
        try:
            # Convert config to ElevenLabs format
            conversational_config = self.convert_to_elevenlabs_config(agent_data)
            
            # Create agent
            response = self.client.conversational_ai.agents.create(
                conversation_config=conversational_config,
                name=agent_data.get('name'),
                tags=agent_data.get('tags', [])
            )
            
            st.success(f"Agent deployed successfully! Agent ID: {response.agent_id}")
            
        except Exception as e:
            st.error(f"Deployment failed: {e}")
    
    def deploy_current_agent(self):
        """Deploy the current agent configuration"""
        config = st.session_state.current_agent_config
        if not config.get('name'):
            st.error("Please set an agent name before deploying")
            return
        
        # Save first
        self.save_agent()
        
        # Then deploy
        agent_id = config['id']
        self.deploy_agent(agent_id, config)
    
    def export_agent_config(self):
        """Export agent configuration as JSON"""
        config = st.session_state.current_agent_config
        config_json = json.dumps(config, indent=2)
        
        st.download_button(
            label="Download Configuration",
            data=config_json,
            file_name=f"{config.get('name', 'agent')}_config.json",
            mime="application/json"
        )
    
    def simulate_agent_response(self, message: str) -> str:
        """Simulate agent response for testing"""
        config = st.session_state.current_agent_config
        system_prompt = config.get('conversation', {}).get('system_prompt', '')
        
        # Simple response simulation
        responses = [
            "I understand your message. How can I help you further?",
            "That's interesting! Can you tell me more about that?",
            "Based on my configuration, I would suggest...",
            "Let me think about that for a moment...",
            "I'm here to help! What would you like to know?",
        ]
        
        import random
        return random.choice(responses)
    
    def show_test_analytics(self):
        """Show test conversation analytics"""
        conversation = st.session_state.test_conversation
        
        if not conversation:
            st.info("No test conversation data available")
            return
        
        st.subheader("📊 Test Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            user_messages = len([m for m in conversation if m['role'] == 'user'])
    def convert_to_elevenlabs_config(self, config: Dict[str, Any]) -> 'ConversationalConfig':
        """Convert internal config to ElevenLabs ConversationalConfig"""
        # This is a placeholder - actual implementation would need to map
        # all the configuration fields to the proper ElevenLabs types
        try:
            return ConversationalConfig()
        except Exception as e:
            st.error(f"Config conversion error: {e}")
            return ConversationalConfig()
    
    def convert_to_elevenlabs_config(self, config: Dict[str, Any]) -> 'ConversationalConfig':
        """Convert internal config to ElevenLabs ConversationalConfig"""
        # This is a placeholder - actual implementation would need to map
        # all the configuration fields to the proper ElevenLabs types
        try:
            return ConversationalConfig()
        except Exception as e:
            st.error(f"Config conversion error: {e}")
            return None
    
    def run(self):
        """Main application runner"""
        load_css()
        
        self.render_header()
        
        # Main interface tabs
        tab1, tab2, tab3 = st.tabs(["🏠 Agent Manager", "⚙️ Agent Builder", "🧪 Testing"])
        
        with tab1:
            self.render_agent_list()
        
        with tab2:
            self.render_agent_configurator()
            self.render_action_buttons()
        
        with tab3:
            self.render_test_interface()

# Main execution
if __name__ == "__main__":
    builder = AgentBuilder()
    builder.run()
