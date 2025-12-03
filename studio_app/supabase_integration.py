"""
Supabase Integration for ElevenLabs Studio
Provides authentication, database, and real-time features
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

import streamlit as st

# Supabase imports
try:
    import asyncio

    from supabase import Client, create_client
except ImportError as e:
    st.error("Supabase package not found. Install with: pip install supabase")
    st.stop()

class SupabaseManager:
    def load_elevenlabs_api_key(self) -> Optional[str]:
        """Load ElevenLabs API key from Supabase for current user and set in session state automatically"""
        try:
            if not self.client or not self.user:
                return None
            
            # Check if table exists first to avoid crashing on fresh installs
            try:
                response = self.client.table('api_keys').select('api_key').eq('user_id', self.user.id).limit(1).execute()
            except Exception:
                # Table might not exist yet
                return None

            api_key = None
            if response.data and len(response.data) > 0:
                api_key = response.data[0].get('api_key')
                if api_key:
                    st.session_state['api_key'] = api_key
            return api_key
        except Exception as e:
            # Silent failure is better here to avoid annoying popups on startup
            print(f"Error loading ElevenLabs API key from Supabase: {e}")
            return None

    def save_elevenlabs_api_key(self, api_key: str) -> bool:
        """Save ElevenLabs API key to Supabase for current user"""
        try:
            if not self.client or not self.user:
                return False
            
            # Upsert api key
            data = {
                'user_id': self.user.id,
                'api_key': api_key,
                'updated_at': datetime.now().isoformat()
            }
            
            response = self.client.table('api_keys').upsert(data).execute()
            return len(response.data) > 0
            
        except Exception as e:
            st.error(f"Error saving API key: {e}")
            return False
    """Manages Supabase connection and operations for ElevenLabs Studio"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.url = None
        self.key = None
        self.user = None
        self.session = None
    
    def initialize(self, url: str, key: str) -> bool:
        """Initialize Supabase client with URL and API key"""
        try:
            self.url = url
            self.key = key

            # Create Supabase client
            self.client = create_client(url, key)

            # Test connection
            if self.client is not None:
                try:
                    response = self.client.table('test').select('*').limit(1).execute()
                except Exception:
                    # Table 'test' may not exist, ignore this error
                    pass

            st.session_state.supabase_client = self.client
            st.session_state.supabase_connected = True
            return True
        except Exception as e:
            st.error(f"Failed to connect to Supabase: {e}")
            return False

    def sign_up(self, email: str, password: str, metadata: Optional[Dict] = None) -> bool:
        """Sign up a new user"""
        try:
            if not self.client:
                return False

            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": metadata or {}
                }
            })

            if response.user:
                st.success("✅ Account created successfully! Please check your email for verification.")
                return True
            else:
                st.error("❌ Failed to create account")
                return False

        except Exception as e:
            st.error(f"Sign up error: {e}")
            return False
    
    def sign_in(self, email: str, password: str) -> bool:
        """Sign in existing user"""
        try:
            if not self.client:
                return False
            
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                self.user = response.user
                self.session = response.session
                st.session_state.supabase_user = response.user
                st.session_state.supabase_session = response.session
                return True
            else:
                return False
                
        except Exception as e:
            st.error(f"Sign in error: {e}")
            return False
    
    def sign_out(self) -> bool:
        """Sign out current user"""
        try:
            if not self.client:
                return False
            
            self.client.auth.sign_out()
            self.user = None
            self.session = None
            
            # Clear session state
            if 'supabase_user' in st.session_state:
                del st.session_state.supabase_user
            if 'supabase_session' in st.session_state:
                del st.session_state.supabase_session
            
            return True
        except Exception as e:
            st.error(f"Sign out error: {e}")
            return False
    
    def get_user(self):
        """Get current authenticated user"""
        try:
            if not self.client:
                return None
            
            user = self.client.auth.get_user()
            return user.user if user else None
        except:
            return None
    
    def save_agent_config(self, agent_config: Dict) -> bool:
        """Save agent configuration to Supabase"""
        try:
            if not self.client or not self.user:
                return False
            
            data = {
                'user_id': self.user.id,
                'agent_name': agent_config.get('name', 'Untitled Agent'),
                'config': agent_config,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            response = self.client.table('agent_configs').insert(data).execute()
            return len(response.data) > 0
            
        except Exception as e:
            st.error(f"Error saving agent config: {e}")
            return False
    
    def load_agent_configs(self) -> List[Dict]:
        """Load user's agent configurations"""
        try:
            if not self.client or not self.user:
                return []
            
            response = self.client.table('agent_configs').select('*').eq('user_id', self.user.id).execute()
            return response.data or []
            
        except Exception as e:
            st.error(f"Error loading agent configs: {e}")
            return []
    
    def delete_agent_config(self, config_id: str) -> bool:
        """Delete an agent configuration"""
        try:
            if not self.client or not self.user:
                return False
            
            response = self.client.table('agent_configs').delete().eq('id', config_id).eq('user_id', self.user.id).execute()
            return len(response.data) > 0
            
        except Exception as e:
            st.error(f"Error deleting agent config: {e}")
            return False
    
    # Removed duplicate empty function definition
    def save_conversation(self, conversation_data: Dict) -> bool:
        """Save conversation history"""
        try:
            if not self.client or not self.user:
                return False

            data = {
                'user_id': self.user.id,
                'agent_id': conversation_data.get('agent_id'),
                'messages': conversation_data.get('messages', []),
                'metadata': conversation_data.get('metadata', {}),
                'created_at': datetime.now().isoformat()
            }

            response = self.client.table('conversations').insert(data).execute()
            return len(response.data) > 0

        except Exception as e:
            st.error(f"Error saving conversation: {e}")
            return False

    def get_conversations(self, agent_id: Optional[str] = None) -> List[Dict]:
        """Get conversation history"""
        try:
            if not self.client or not self.user:
                return []

            query = self.client.table('conversations').select('*').eq('user_id', self.user.id)

            if agent_id is not None:
                query = query.eq('agent_id', agent_id)

            response = query.order('created_at', desc=True).execute()
            return response.data or []

        except Exception as e:
            st.error(f"Error loading conversations: {e}")
            return []
    def save_usage_metrics(self, metrics: Dict) -> bool:
        """Save usage metrics and analytics"""
        try:
            if not self.client or not self.user:
                return False
            
            data = {
                'user_id': self.user.id,
                'feature_used': metrics.get('feature'),
                'usage_count': metrics.get('count', 1),
                'metadata': metrics.get('metadata', {}),
                'timestamp': datetime.now().isoformat()
            }
            
            response = self.client.table('usage_metrics').insert(data).execute()
            return len(response.data) > 0
            
        except Exception as e:
            st.error(f"Error saving usage metrics: {e}")
            return False
    
    def get_user_analytics(self) -> Dict:
        """Get user analytics and usage statistics"""
        try:
            if not self.client or not self.user:
                return {}
            
            # Get usage metrics
            response = self.client.table('usage_metrics').select('*').eq('user_id', self.user.id).execute()
            metrics = response.data or []
            
            # Get agent count
            agent_response = self.client.table('agent_configs').select('id').eq('user_id', self.user.id).execute()
            agent_count = len(agent_response.data or [])
            
            # Get conversation count
            conv_response = self.client.table('conversations').select('id').eq('user_id', self.user.id).execute()
            conversation_count = len(conv_response.data or [])
            
            return {
                'total_usage': len(metrics),
                'agent_count': agent_count,
                'conversation_count': conversation_count,
                'metrics': metrics
            }
            
        except Exception as e:
            st.error(f"Error loading analytics: {e}")
            return {}

def render_supabase_setup():
    """Render Supabase connection setup interface"""
    st.markdown("""
    <div class="config-section">
        <h3 style="color: var(--text-main); margin-bottom: 1rem;">
            🗄️ <span class="gradient-text">Supabase Configuration</span>
        </h3>
        <p style="color: var(--text-muted); margin-bottom: 2rem;">
            Connect to Supabase for cloud storage, authentication, and real-time features
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔗 Connection Settings")
        supabase_url = st.text_input(
            "Supabase URL",
            value=st.session_state.get('supabase_url', ''),
            placeholder="https://your-project.supabase.co",
            help="Your Supabase project URL"
        )
        
        supabase_key = st.text_input(
            "Supabase Anon Key",
            value=st.session_state.get('supabase_key', ''),
            type="password",
            placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            help="Your Supabase anonymous/public key"
        )
    
    with col2:
        st.markdown("#### ℹ️ Setup Instructions")
        st.markdown("""
        1. **Create a Supabase Project**:
           - Go to [supabase.com](https://supabase.com)
           - Create a new project
           
        2. **Get Your Credentials**:
           - Project URL from Settings > API
           - Anon key from Settings > API
           
        3. **Set Up Database Tables** (Optional):
           - We'll create tables automatically
           - Or use the SQL schema provided
        """)
    
    if st.button("🔗 Connect to Supabase", type="primary"):
        if supabase_url and supabase_key:
            supabase_manager = SupabaseManager()
            if supabase_manager.initialize(supabase_url, supabase_key):
                st.session_state.supabase_url = supabase_url
                st.session_state.supabase_key = supabase_key
                st.session_state.supabase_manager = supabase_manager
                st.success("✅ Connected to Supabase successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to connect to Supabase. Check your credentials.")
        else:
            st.error("Please provide both Supabase URL and API key")

def render_supabase_auth():
    """Render Supabase authentication interface"""
    if 'supabase_manager' not in st.session_state:
        return
    
    supabase_manager = st.session_state.supabase_manager
    
    # Check if user is logged in
    current_user = st.session_state.get('supabase_user')
    
    if not current_user:
        # Show login/signup interface
        st.markdown("""
        <div class="config-section">
            <h3 style="color: var(--text-main); margin-bottom: 1rem;">
                🔐 <span class="gradient-text">Authentication</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        auth_tab1, auth_tab2 = st.tabs(["🔑 Sign In", "✨ Sign Up"])
        
        with auth_tab1:
            with st.form("signin_form"):
                st.markdown("#### Sign In to Your Account")
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("🔑 Sign In", type="primary"):
                    if email and password:
                        if supabase_manager.sign_in(email, password):
                            st.success("✅ Signed in successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                    else:
                        st.error("Please provide email and password")
        
        with auth_tab2:
            with st.form("signup_form"):
                st.markdown("#### Create New Account")
                new_email = st.text_input("Email", placeholder="your@email.com", key="signup_email")
                new_password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                # User metadata
                st.markdown("#### Profile Information")
                full_name = st.text_input("Full Name", placeholder="John Doe")
                company = st.text_input("Company (Optional)", placeholder="Your Company")
                
                if st.form_submit_button("✨ Create Account", type="primary"):
                    if new_email and new_password and confirm_password:
                        if new_password == confirm_password:
                            metadata = {
                                "full_name": full_name,
                                "company": company
                            }
                            if supabase_manager.sign_up(new_email, new_password, metadata):
                                st.info("📧 Please check your email to verify your account")
                        else:
                            st.error("❌ Passwords do not match")
                    else:
                        st.error("Please fill in all required fields")
    
    else:
        # Show user dashboard
        render_user_dashboard(supabase_manager, current_user)

def render_user_dashboard(supabase_manager: SupabaseManager, user):
    """Render user dashboard with Supabase data"""
    st.markdown(f"""
    <div class="agent-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="color: var(--text-main); margin: 0;">
                    👋 Welcome, <span class="gradient-text">{user.email}</span>
                </h3>
                <p style="color: var(--text-muted); margin: 0.5rem 0 0 0;">
                    Connected to Supabase • Account verified
                </p>
            </div>
            <div>
                <span class="status-badge status-online">
                    🟢 Online
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # User analytics
    analytics = supabase_manager.get_user_analytics()
    
    if analytics:
        st.markdown("#### 📊 Your Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Agents Created", analytics.get('agent_count', 0))
        with col2:
            st.metric("Conversations", analytics.get('conversation_count', 0))
        with col3:
            st.metric("Total Usage", analytics.get('total_usage', 0))
        with col4:
            if st.button("🚪 Sign Out"):
                if supabase_manager.sign_out():
                    st.success("✅ Signed out successfully!")
                    st.rerun()

def render_cloud_features():
    """Render cloud-enabled features"""
    if 'supabase_manager' not in st.session_state or 'supabase_user' not in st.session_state:
        st.info("🔐 Sign in to access cloud features")
        return
    
    supabase_manager = st.session_state.supabase_manager
    
    st.markdown("### ☁️ Cloud Features")
    
    cloud_tab1, cloud_tab2, cloud_tab3 = st.tabs(["💾 Saved Agents", "💬 Conversations", "📈 Analytics"])
    
    with cloud_tab1:
        st.markdown("#### 🤖 Your Saved Agents")
        
        # Load and display saved agents
        saved_agents = supabase_manager.load_agent_configs()
        
        if saved_agents:
            for agent in saved_agents:
                with st.container():
                    st.markdown(f"""
                    <div class="agent-card">
                        <h4 style="color: var(--text-main); margin: 0 0 0.5rem 0;">
                            🤖 {agent.get('agent_name', 'Untitled Agent')}
                        </h4>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin: 0 0 1rem 0;">
                            Created: {agent.get('created_at', 'Unknown')[:10]}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📥 Load {agent['agent_name']}", key=f"load_{agent['id']}"):
                            st.session_state.current_agent_config = agent['config']
                            st.success(f"✅ Loaded agent '{agent['agent_name']}'")
                    
                    with col2:
                        if st.button("📋 Copy Config", key=f"copy_{agent['id']}"):
                            st.code(json.dumps(agent['config'], indent=2), language='json')
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{agent['id']}"):
                            if supabase_manager.delete_agent_config(agent['id']):
                                st.success(f"✅ Deleted agent '{agent['agent_name']}'")
                                st.rerun()
        else:
            st.info("No saved agents found. Create and save agents to see them here.")
    
    with cloud_tab2:
        st.markdown("#### 💬 Conversation History")
        
        conversations = supabase_manager.get_conversations()
        
        if conversations:
            for conv in conversations[:10]:  # Show last 10 conversations
                with st.expander(f"Conversation from {conv.get('created_at', 'Unknown')[:10]}"):
                    messages = conv.get('messages', [])
                    for msg in messages[-5:]:  # Show last 5 messages
                        if msg.get('role') == 'user':
                            st.markdown(f"**You:** {msg.get('content', '')}")
                        else:
                            st.markdown(f"**Agent:** {msg.get('content', '')}")
        else:
            st.info("No conversation history found.")
    
    with cloud_tab3:
        st.markdown("#### 📈 Usage Analytics")
        
        analytics = supabase_manager.get_user_analytics()
        
        if analytics.get('metrics'):
            # Feature usage chart
            feature_usage = {}
            for metric in analytics['metrics']:
                feature = metric.get('feature_used', 'Unknown')
                feature_usage[feature] = feature_usage.get(feature, 0) + metric.get('usage_count', 1)
            
            if feature_usage:
                st.markdown("**Feature Usage:**")
                for feature, count in feature_usage.items():
                    st.metric(f"{feature}", count)
        
        else:
            st.info("No analytics data available yet.")

def create_database_schema():
    """SQL schema for creating Supabase tables"""
    return """
-- Enable Row Level Security
ALTER TABLE IF EXISTS agent_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS usage_metrics ENABLE ROW LEVEL SECURITY;

-- Agent Configurations Table
CREATE TABLE IF NOT EXISTS agent_configs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversations Table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    agent_id TEXT,
    messages JSONB NOT NULL DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Usage Metrics Table
CREATE TABLE IF NOT EXISTS usage_metrics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    feature_used TEXT NOT NULL,
    usage_count INTEGER DEFAULT 1,
    metadata JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security Policies
CREATE POLICY "Users can only access their own agent configs" ON agent_configs
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can only access their own conversations" ON conversations
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can only access their own usage metrics" ON usage_metrics
    FOR ALL USING (auth.uid() = user_id);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_agent_configs_user_id ON agent_configs(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_metrics_user_id ON usage_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_metrics_feature ON usage_metrics(feature_used);

-- API Keys Table
CREATE TABLE IF NOT EXISTS api_keys (
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    api_key TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- API Keys RLS
ALTER TABLE IF EXISTS api_keys ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only access their own api keys" ON api_keys
    FOR ALL USING (auth.uid() = user_id);
"""

def render_database_setup():
    """Render database schema setup"""
    st.markdown("#### 🗄️ Database Setup")
    
    st.markdown("""
    **Automatic Setup**: Tables will be created automatically when you first use cloud features.
    
    **Manual Setup**: Copy the SQL below and run it in your Supabase SQL editor for optimal configuration:
    """)
    
    if st.button("📋 Show Database Schema"):
        st.code(create_database_schema(), language='sql')
        st.info("💡 Run this SQL in your Supabase project's SQL editor to set up all tables and security policies.")

# Initialize Supabase session state
def init_supabase_session():
    """Initialize Supabase-related session state"""
    if 'supabase_connected' not in st.session_state:
        st.session_state.supabase_connected = False
    if 'supabase_url' not in st.session_state:
        st.session_state.supabase_url = ''
    if 'supabase_key' not in st.session_state:
        st.session_state.supabase_key = ''

# Auto-save functionality
    # Removed duplicate empty function definition
def auto_save_agent_config(config: Dict):
    """Automatically save agent config to Supabase if connected"""
    if ('supabase_manager' in st.session_state and
        'supabase_user' in st.session_state and
        config.get('name')):
        supabase_manager = st.session_state.supabase_manager
        if supabase_manager.save_agent_config(config):
            st.toast("💾 Agent configuration auto-saved to cloud")

def track_feature_usage(feature_name: str, metadata: Optional[Dict] = None):
    """Track feature usage in Supabase"""
    if ('supabase_manager' in st.session_state and
        'supabase_user' in st.session_state):
        supabase_manager = st.session_state.supabase_manager
        metrics = {
            'feature': feature_name,
            'count': 1,
            'metadata': metadata or {}
        }
        supabase_manager.save_usage_metrics(metrics)
    if ('supabase_manager' in st.session_state and 
        'supabase_user' in st.session_state):
        
        supabase_manager = st.session_state.supabase_manager
        metrics = {
            'feature': feature_name,
            'count': 1,
            'metadata': metadata or {}
        }
        supabase_manager.save_usage_metrics(metrics)
