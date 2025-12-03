import streamlit as st
from utils import UIComponents

# Supabase integration import
try:
    from supabase_integration import (
        render_cloud_features,
        render_database_setup,
        render_supabase_auth,
        render_supabase_setup,
    )
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

def render_cloud_integration(studio):
    """Render Cloud Integration with Supabase"""
    UIComponents.render_section_header("☁️ Cloud Features & Integration", "Connect to Supabase for cloud storage, authentication, and analytics")
    
    if not SUPABASE_AVAILABLE:
        st.error("❌ Supabase integration not available. Install with: `pip install supabase`")
        st.markdown("Run this command to install Supabase:")
        st.code("pip install supabase", language="bash")
        return
    
    # Check if Supabase is connected
    if not st.session_state.get('supabase_connected', False):
        st.info("🔗 Connect to Supabase to enable cloud features")
        
        cloud_tab1, cloud_tab2 = st.tabs(["🔧 Setup", "📚 Documentation"])
        
        with cloud_tab1:
            render_supabase_setup()
        
        with cloud_tab2:
            st.markdown("### 📚 Supabase Integration Guide")
            
            st.markdown("""
            **What is Supabase?**
            
            Supabase is an open-source Firebase alternative that provides:
            - 🗄️ **Database**: PostgreSQL database with real-time subscriptions
            - 🔐 **Authentication**: User management and security
            - 📁 **Storage**: File storage for audio and documents
            - ⚡ **Real-time**: Live updates and collaboration
            
            **Benefits for ElevenLabs Studio:**
            - 💾 Save agent configurations to the cloud
            - 🔄 Sync data across devices
            - 👥 Share agents with team members
            - 📊 Track usage analytics
            - 🔒 Secure user authentication
            """)
            
            render_database_setup()
    
    else:
        # Supabase is connected, show main interface
        st.success("🟢 Connected to Supabase")
        
        # Authentication interface
        render_supabase_auth()
        
        st.markdown("---")
        
        # Cloud features
        render_cloud_features()
        
        # Auto-save functionality notice
        if st.session_state.get('supabase_user'):
            st.markdown("---")
            st.info("💡 **Auto-save enabled**: Agent configurations are automatically saved to your cloud account")
