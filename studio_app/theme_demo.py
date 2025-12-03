"""
Supabase Dark Theme Demo Component
This demonstrates the new Supabase-inspired dark theme for ElevenLabs Studio
"""

import streamlit as st


def show_theme_demo():
    """Display a demo of the Supabase dark theme components"""
    
    st.markdown("# 🎨 Supabase Dark Theme Demo")
    st.markdown("---")
    
    # Theme showcase
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card glass-card">
            <h3><span class="gradient-text">🌙 Dark Theme Elements</span></h3>
            <p>Experience the modern Supabase-inspired design with:</p>
            <div style="margin-top: 1rem;">
                <span style="background: rgba(62, 207, 142, 0.2); color: var(--supabase-green); 
                             padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.75rem; margin-right: 0.5rem;">
                    Glass morphism effects
                </span>
                <span style="background: rgba(62, 207, 142, 0.2); color: var(--supabase-green); 
                             padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.75rem; margin-right: 0.5rem;">
                    Gradient accents
                </span>
                <span style="background: rgba(62, 207, 142, 0.2); color: var(--supabase-green); 
                             padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.75rem;">
                    Smooth animations
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive elements demo
        st.markdown("### 🎛️ Interactive Components")
        demo_text = st.text_input("Text Input", placeholder="Type something...")
        demo_slider = st.slider("Slider Control", 0, 100, 50)
        demo_select = st.selectbox("Dropdown", ["Option 1", "Option 2", "Option 3"])
        
    with col2:
        st.markdown("""
        <div class="audio-player glass-card">
            <h4>🎵 Audio Player Component</h4>
            <p style="color: var(--supabase-text-muted); font-size: 0.9rem;">
                Enhanced audio player with glass morphism effects
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Status indicators
        st.markdown("### 📊 Status Indicators")
        
        col_status1, col_status2, col_status3 = st.columns(3)
        
        with col_status1:
            st.markdown("""
            <div style="background: rgba(62, 207, 142, 0.1); border: 1px solid var(--supabase-green); 
                        border-radius: 8px; padding: 1rem; text-align: center;">
                <div style="color: var(--supabase-green); font-size: 1.5rem; margin-bottom: 0.5rem;">✅</div>
                <div style="color: var(--supabase-green); font-weight: 500;">Connected</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_status2:
            st.markdown("""
            <div style="background: rgba(251, 191, 36, 0.1); border: 1px solid #FBBF24; 
                        border-radius: 8px; padding: 1rem; text-align: center;">
                <div style="color: #FBBF24; font-size: 1.5rem; margin-bottom: 0.5rem;">⏳</div>
                <div style="color: #FBBF24; font-weight: 500;">Processing</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_status3:
            st.markdown("""
            <div style="background: rgba(240, 82, 82, 0.1); border: 1px solid #F05252; 
                        border-radius: 8px; padding: 1rem; text-align: center;">
                <div style="color: #F05252; font-size: 1.5rem; margin-bottom: 0.5rem;">❌</div>
                <div style="color: #F05252; font-weight: 500;">Error</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Buttons demo
    st.markdown("### 🎯 Button Styles")
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        st.button("Primary Action", type="primary")
    with col_btn2:
        st.button("Secondary Action")
    with col_btn3:
        st.button("Success", help="Success action")
    with col_btn4:
        st.button("Warning", help="Warning action")
    
    # Metrics showcase
    st.markdown("### 📈 Enhanced Metrics")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.metric("Voices Available", "847", delta="23")
    with col_m2:
        st.metric("Characters Used", "1.2M", delta="-50K")
    with col_m3:
        st.metric("Success Rate", "99.8%", delta="0.2%")
    with col_m4:
        st.metric("Avg Response", "2.1s", delta="-0.3s")
    
    # Theme comparison
    st.markdown("---")
    st.markdown("## 🔄 Theme Comparison")
    
    col_compare1, col_compare2 = st.columns(2)
    
    with col_compare1:
        st.markdown("""
        ### 🌅 Previous Theme
        - Basic gradients
        - Light-focused design
        - Standard buttons
        - Simple cards
        """)
    
    with col_compare2:
        st.markdown("""
        ### 🌙 Supabase Dark Theme
        - <span class="gradient-text">Glass morphism effects</span>
        - Professional dark design
        - Enhanced interactive elements
        - Modern card styling with borders
        """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("---")
    st.markdown("## ✨ New Theme Features")
    
    features = [
        ("🎨 Color Palette", "Supabase green (#3ECF8E) as primary with dark backgrounds"),
        ("🔤 Typography", "Inter font family for modern, clean text"),
        ("🪟 Glass Effects", "Translucent cards with backdrop blur"),
        ("🌈 Gradients", "Subtle gradients for accent elements"),
        ("⚡ Animations", "Smooth hover and transition effects"),
        ("📱 Responsive", "Optimized for all screen sizes"),
        ("🎯 Focus States", "Enhanced focus indicators for accessibility"),
        ("🔄 Loading States", "Shimmer animations for loading content")
    ]
    
    for icon_title, description in features:
        st.markdown(f"""
        <div style="background: var(--supabase-bg-alt); border: 1px solid var(--supabase-border); 
                    border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;">
            <strong style="color: var(--supabase-text);">{icon_title}</strong>
            <span style="color: var(--supabase-text-muted); margin-left: 1rem;">{description}</span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_theme_demo()
