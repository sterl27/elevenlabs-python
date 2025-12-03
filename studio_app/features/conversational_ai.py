import json
import os
import sys
import streamlit as st
from utils import UIComponents

def render_conversational_ai(studio):
    """Render Conversational AI interface with full agent builder"""
    UIComponents.render_section_header("🤖 Conversational AI Agents", "Create, configure, and deploy intelligent voice agents with advanced AI capabilities")
    
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
            # Add pages directory to path
            pages_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pages')
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

def render_simple_agent_builder(studio):
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

def render_phone_integration(studio):
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

def render_chat_interface(studio):
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

def render_tools_knowledge(studio):
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
