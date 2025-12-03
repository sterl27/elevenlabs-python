"""
Ethereum Voice Tagging Toolkit for ElevenLabs Studio
Provides persona-based tag validation and embedding for voice generation
"""

import json
import re
from typing import Any, Dict, List

import streamlit as st


class EthereumTagValidator:
    """Validator for Ethereum persona tags with deep taxonomy"""
    
    def __init__(self, persona_path: str = None):
        self.persona_data = {}
        self.valid_tags = set()
        if persona_path:
            self.load_persona(persona_path)
    
    def load_persona(self, path: str) -> bool:
        """Load persona card with tag taxonomy"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.persona_data = json.load(f)
            
            # Extract all tags from persona
            self.valid_tags = set()
            for key, value in self.persona_data.items():
                if isinstance(value, list) and "tags" in key.lower():
                    self.valid_tags.update(f"[{tag.upper()}]" for tag in value)
                elif key == "name" and isinstance(value, str):
                    self.valid_tags.add(f"[{value.upper()}]")
            
            return True
        except Exception as e:
            st.error(f"Error loading persona: {e}")
            return False
    
    def validate_lyrics(self, lyrics: str) -> Dict[str, List[str]]:
        """Validate tags in lyrics against persona taxonomy"""
        # Find all tags in lyrics
        found_tags = set(re.findall(r'\[[^\[\]]+\]', lyrics))
        
        # Normalize for comparison
        found_normalized = {tag.upper() for tag in found_tags}
        valid_normalized = {tag.upper() for tag in self.valid_tags}
        
        # Calculate differences
        used_tags = list(found_tags)
        invalid_tags = [tag for tag in found_tags if tag.upper() not in valid_normalized]
        missing_core = [tag for tag in self.valid_tags if "[ETHEREUM]" in tag.upper() and tag.upper() not in found_normalized]
        
        return {
            "used": used_tags,
            "invalid": invalid_tags,
            "missing_core": missing_core,
            "total_valid": len(self.valid_tags),
            "coverage": len(found_normalized & valid_normalized) / len(valid_normalized) if valid_normalized else 0
        }
    
    def auto_embed_tags(self, lyrics: str, inject_count: int = 6) -> str:
        """Auto-embed Ethereum tags into lyrics"""
        if not self.valid_tags:
            return lyrics
        
        # Ensure ETHEREUM tag is present
        if "[ETHEREUM]" not in lyrics.upper():
            lyrics = "[ETHEREUM]\n" + lyrics
        
        # Get priority tags (first inject_count)
        priority_tags = list(self.valid_tags)[:inject_count]
        
        # Embed missing priority tags
        for tag in priority_tags:
            if tag.upper() not in lyrics.upper():
                lyrics += f"\n{tag}"
        
        return lyrics
    
    def get_tag_suggestions(self, category: str = None) -> List[str]:
        """Get tag suggestions by category"""
        if not self.persona_data:
            return []
        
        if category:
            category_key = f"{category.lower()}_tags"
            return self.persona_data.get(category_key, [])
        
        # Return all tags
        all_tags = []
        for key, value in self.persona_data.items():
            if isinstance(value, list) and "tags" in key.lower():
                all_tags.extend(value)
        return all_tags

def create_default_persona() -> Dict[str, Any]:
    """Create default Ethereum persona if none exists"""
    return {
        "name": "ETHEREUM",
        "description": "Ethereum blockchain voice persona with deep technical and philosophical understanding",
        "core_tags": [
            "ETHEREUM", "BLOCKCHAIN", "DECENTRALIZED", "SMART_CONTRACTS", 
            "WEB3", "DEFI", "CRYPTO", "VITALIK", "GAS", "PROOF_OF_STAKE"
        ],
        "technical_tags": [
            "EVM", "SOLIDITY", "MERKLE_TREE", "CONSENSUS", "VALIDATOR",
            "SHARDING", "LAYER2", "ROLLUPS", "PLASMA", "STATE_CHANNEL"
        ],
        "philosophical_tags": [
            "FREEDOM", "SOVEREIGNTY", "PERMISSIONLESS", "TRUSTLESS",
            "IMMUTABLE", "TRANSPARENT", "GLOBAL", "INCLUSIVE"
        ],
        "energy_tags": [
            "ELECTRIC", "DIGITAL_FIRE", "QUANTUM", "INFINITE",
            "REVOLUTIONARY", "UNSTOPPABLE", "FUTURE", "TRANSFORMATION"
        ],
        "voice_style_tags": [
            "DEEP", "RESONANT", "AUTHORITATIVE", "MYSTIC",
            "TECHNICAL", "PASSIONATE", "VISIONARY", "CONFIDENT"
        ]
    }

def render_ethereum_tagging():
    """Render the Ethereum tagging interface"""
    st.markdown("## 🏷️ Ethereum Voice Tagging")
    st.markdown("---")
    
    # Initialize validator
    if 'ethereum_validator' not in st.session_state:
        st.session_state.ethereum_validator = EthereumTagValidator()
        # Load default persona
        default_persona = create_default_persona()
        st.session_state.ethereum_validator.persona_data = default_persona
        st.session_state.ethereum_validator.valid_tags = set()
        for key, value in default_persona.items():
            if isinstance(value, list) and "tags" in key.lower():
                st.session_state.ethereum_validator.valid_tags.update(f"[{tag}]" for tag in value)
    
    validator = st.session_state.ethereum_validator
    
    # Tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs(["🎤 Tag Lyrics", "📋 Persona Manager", "🔍 Validator", "🎵 Voice Preview"])
    
    with tab1:
        st.markdown("### 🎤 Tag Your Lyrics with Ethereum Voice")
        
        # Text input for lyrics
        lyrics_input = st.text_area(
            "Enter your lyrics:",
            height=200,
            placeholder="Enter your lyrics here...\nUse [TAGS] to mark voice style elements"
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏷️ Auto-Embed Tags", type="primary"):
                if lyrics_input:
                    embedded_lyrics = validator.auto_embed_tags(lyrics_input)
                    st.session_state.processed_lyrics = embedded_lyrics
                    st.success("✅ Tags embedded successfully!")
        
        with col2:
            if st.button("🔍 Validate Tags"):
                if lyrics_input:
                    validation = validator.validate_lyrics(lyrics_input)
                    st.session_state.validation_result = validation
        
        with col3:
            inject_count = st.number_input("Tags to inject", min_value=1, max_value=20, value=6)
        
        # Show processed lyrics
        if 'processed_lyrics' in st.session_state:
            st.markdown("### 📝 Tagged Lyrics")
            st.text_area(
                "Processed lyrics with tags:",
                st.session_state.processed_lyrics,
                height=150,
                key="output_lyrics"
            )
            
            # Download button
            st.download_button(
                "📥 Download Tagged Lyrics",
                st.session_state.processed_lyrics,
                file_name="ethereum_tagged_lyrics.txt",
                mime="text/plain"
            )
    
    with tab2:
        st.markdown("### 📋 Ethereum Persona Manager")
        
        # Upload custom persona
        uploaded_persona = st.file_uploader(
            "Upload Persona JSON",
            type=['json'],
            help="Upload a custom Ethereum persona card"
        )
        
        if uploaded_persona:
            try:
                persona_data = json.loads(uploaded_persona.read())
                validator.persona_data = persona_data
                validator.valid_tags = set()
                for key, value in persona_data.items():
                    if isinstance(value, list) and "tags" in key.lower():
                        validator.valid_tags.update(f"[{tag}]" for tag in value)
                st.success("✅ Persona loaded successfully!")
            except Exception as e:
                st.error(f"Error loading persona: {e}")
        
        # Show current persona stats
        st.markdown("#### 📊 Current Persona Stats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Tags", len(validator.valid_tags))
        with col2:
            st.metric("Categories", len([k for k in validator.persona_data.keys() if "tags" in k.lower()]))
        with col3:
            st.metric("Core Identity", validator.persona_data.get("name", "ETHEREUM"))
        
        # Tag categories
        if validator.persona_data:
            st.markdown("#### 🏷️ Available Tag Categories")
            for key, value in validator.persona_data.items():
                if isinstance(value, list) and "tags" in key.lower():
                    with st.expander(f"{key.replace('_', ' ').title()} ({len(value)} tags)"):
                        tag_display = " ".join([f"`[{tag}]`" for tag in value])
                        st.markdown(tag_display)
    
    with tab3:
        st.markdown("### 🔍 Tag Validation Results")
        
        if 'validation_result' in st.session_state:
            validation = st.session_state.validation_result
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Used Tags", len(validation["used"]))
            with col2:
                st.metric("Invalid Tags", len(validation["invalid"]))
            with col3:
                st.metric("Missing Core", len(validation["missing_core"]))
            with col4:
                st.metric("Coverage", f"{validation['coverage']:.1%}")
            
            # Detailed results
            if validation["used"]:
                st.markdown("#### ✅ Used Tags")
                st.success(" ".join([f"`{tag}`" for tag in validation["used"]]))
            
            if validation["invalid"]:
                st.markdown("#### ❌ Invalid Tags")
                st.error(" ".join([f"`{tag}`" for tag in validation["invalid"]]))
            
            if validation["missing_core"]:
                st.markdown("#### ⚠️ Missing Core Tags")
                st.warning(" ".join([f"`{tag}`" for tag in validation["missing_core"]]))
        else:
            st.info("👆 Process some lyrics in the 'Tag Lyrics' tab to see validation results")
    
    with tab4:
        st.markdown("### 🎵 Voice Preview with ElevenLabs")
        
        if 'processed_lyrics' in st.session_state:
            st.markdown("#### 🎤 Generate Ethereum Voice")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Voice selection (would integrate with your existing voice manager)
                st.selectbox(
                    "Select Ethereum Voice",
                    ["Ethereum Core", "Ethereum Mystic", "Ethereum Technical", "Ethereum Visionary"],
                    help="Choose the Ethereum voice variant"
                )
            
            with col2:
                # Style modifiers based on tags
                st.multiselect(
                    "Voice Style Modifiers",
                    ["Deep", "Resonant", "Technical", "Passionate", "Authoritative"],
                    default=["Deep", "Resonant"]
                )
            
            # Preview button (would integrate with your ElevenLabs client)
            if st.button("🎤 Generate Voice Preview", type="primary"):
                st.info("🔗 This would integrate with your ElevenLabs client to generate audio")
                st.markdown("**Tagged lyrics ready for voice generation:**")
                st.code(st.session_state.processed_lyrics[:200] + "...")
        else:
            st.info("👆 Process some lyrics first to enable voice preview")

if __name__ == "__main__":
    render_ethereum_tagging()
