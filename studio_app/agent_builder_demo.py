"""
Demo script to test the Conversational AI Agent Builder
Run this to see the new agent builder page in action
"""

import os
import sys

import streamlit as st

# Add the current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configure the page
st.set_page_config(
    page_title="ElevenLabs Agent Builder Demo",
    page_icon="🤖",
    layout="wide"
)

try:
    # Import the agent builder
    from pages.agent_builder import AgentBuilder
    
    # Initialize and run the agent builder
    st.markdown("# 🤖 ElevenLabs Conversational AI Agent Builder Demo")
    st.markdown("---")
    
    builder = AgentBuilder()
    builder.run()
    
except ImportError as e:
    st.error(f"Could not import agent builder: {e}")
    st.info("Make sure the agent_builder.py file is in the pages/ directory")
    
    # Show file structure
    st.markdown("### File Structure Check:")
    for root, dirs, files in os.walk(current_dir):
        level = root.replace(current_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        st.text(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                st.text(f"{subindent}{file}")

except Exception as e:
    st.error(f"Error running agent builder: {e}")
    st.exception(e)
