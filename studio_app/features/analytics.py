import streamlit as st
from utils import UIComponents

def render_analytics(studio):
    """Render Analytics & Usage interface"""
    UIComponents.render_section_header("📊 Analytics & Usage", "Monitor your character usage, billing, and performance metrics")
    
    tab1, tab2, tab3 = st.tabs(["📈 Usage Stats", "💰 Billing", "🎯 Performance"])
    
    with tab1:
        st.markdown("### 📈 Usage Statistics")
        
        try:
            # Get usage data
            usage_data = studio.client.usage.get_characters_usage_metrics()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Characters Used",
                    f"{usage_data.characters_used:,}",
                    f"+{usage_data.characters_used - getattr(usage_data, 'previous_characters_used', 0):,}"
                )
            
            with col2:
                st.metric(
                    "Characters Limit",
                    f"{usage_data.character_limit:,}",
                    f"{((usage_data.characters_used / usage_data.character_limit) * 100):.1f}% used"
                )
            
            with col3:
                remaining = usage_data.character_limit - usage_data.characters_used
                st.metric(
                    "Remaining",
                    f"{remaining:,}",
                    f"{(remaining / usage_data.character_limit * 100):.1f}% left"
                )
            
            with col4:
                reset_date = getattr(usage_data, 'reset_date', 'Unknown')
                st.metric(
                    "Reset Date",
                    reset_date,
                    "Monthly cycle"
                )
            
            # Usage chart placeholder
            st.markdown("#### Usage Over Time")
            st.info("Usage charts would be displayed here with historical data")
        
        except Exception as e:
            st.error(f"Error fetching usage data: {str(e)}")
    
    with tab2:
        st.markdown("### 💰 Billing Information")
        st.info("Billing details would be displayed here")
    
    with tab3:
        st.markdown("### 🎯 Performance Metrics")
        st.info("Performance analytics would be displayed here")
