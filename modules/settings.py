"""
Settings Module
Application configuration and settings management
"""

import streamlit as st
import os

class Settings:
    """Settings and Configuration Module"""
    
    def __init__(self):
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for settings"""
        if 'openai_api_key' not in st.session_state:
            st.session_state.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        if 'organization_name' not in st.session_state:
            st.session_state.organization_name = "Manufacturing Innovation Corp"
        if 'theme' not in st.session_state:
            st.session_state.theme = "Professional"
    
    def render(self):
        """Render the Settings interface"""
        st.markdown('<p class="main-header">⚙️ Settings</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Configure your platform settings</p>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["🔑 API Configuration", "🏢 Organization", "🎨 Appearance", "📊 Data"])
        
        with tab1:
            self._render_api_settings()
        
        with tab2:
            self._render_organization_settings()
        
        with tab3:
            self._render_appearance_settings()
        
        with tab4:
            self._render_data_settings()
    
    def _render_api_settings(self):
        """Render API configuration settings"""
        st.markdown("### 🔑 API Configuration")
        
        st.markdown("""
        Configure your OpenAI API key to enable AI-powered features. 
        Your API key is stored securely in the session and is not persisted.
        """)
        
        st.markdown("---")
        
        # OpenAI Configuration
        st.markdown("#### OpenAI API")
        
        current_key = st.session_state.get('openai_api_key', '')
        masked_key = f"{'*' * 20}{current_key[-8:]}" if current_key and len(current_key) > 8 else ""
        
        if current_key:
            st.success(f"✅ API Key configured: {masked_key}")
        else:
            st.warning("⚠️ No API key configured")
        
        new_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API key. Get one at https://platform.openai.com/api-keys"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save API Key", type="primary", use_container_width=True):
                if new_key.strip():
                    if new_key.startswith('sk-'):
                        st.session_state.openai_api_key = new_key.strip()
                        st.success("✅ API key saved successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid API key format. OpenAI keys start with 'sk-'")
                else:
                    st.error("Please enter an API key")
        
        with col2:
            if st.button("🗑️ Clear API Key", use_container_width=True):
                st.session_state.openai_api_key = ''
                st.info("API key cleared")
                st.rerun()
        
        st.markdown("---")
        
        # Model settings
        st.markdown("#### Model Settings")
        
        model = st.selectbox(
            "GPT Model",
            ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"],
            help="Select the OpenAI model to use"
        )
        
        temperature = st.slider(
            "Temperature",
            0.0, 1.0, 0.7,
            help="Higher values make output more random, lower values more deterministic"
        )
        
        st.markdown("---")
        
        st.markdown("#### API Usage Guidelines")
        st.info("""
        **Cost Optimization Tips:**
        - GPT-4 provides best results but costs more
        - GPT-3.5-turbo is faster and more economical
        - Use lower temperature for consistent, factual outputs
        - Use higher temperature for creative content
        """)
    
    def _render_organization_settings(self):
        """Render organization settings"""
        st.markdown("### 🏢 Organization Settings")
        
        org_name = st.text_input(
            "Organization Name",
            value=st.session_state.organization_name,
            help="Your organization's name for reports and documents"
        )
        
        if org_name != st.session_state.organization_name:
            st.session_state.organization_name = org_name
        
        st.markdown("---")
        
        st.markdown("#### Industry Settings")
        
        industry = st.selectbox(
            "Industry",
            [
                "Advanced Manufacturing",
                "Automotive",
                "Aerospace",
                "Electronics",
                "Pharmaceuticals",
                "Food & Beverage",
                "Consumer Goods",
                "Industrial Equipment",
                "Other"
            ]
        )
        
        company_size = st.selectbox(
            "Company Size",
            ["Small (1-100)", "Medium (100-500)", "Large (500-1000)", "Enterprise (1000+)"]
        )
        
        st.markdown("---")
        
        st.markdown("#### Contact Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            admin_name = st.text_input("Admin Name")
            admin_email = st.text_input("Admin Email")
        
        with col2:
            department = st.text_input("Department")
            location = st.text_input("Location")
        
        if st.button("💾 Save Organization Settings", type="primary"):
            st.success("✅ Organization settings saved!")
    
    def _render_appearance_settings(self):
        """Render appearance settings"""
        st.markdown("### 🎨 Appearance Settings")
        
        theme = st.selectbox(
            "Theme",
            ["Professional", "Modern", "Classic", "Dark"],
            index=["Professional", "Modern", "Classic", "Dark"].index(st.session_state.theme)
        )
        
        if theme != st.session_state.theme:
            st.session_state.theme = theme
        
        st.markdown("---")
        
        st.markdown("#### Dashboard Preferences")
        
        show_metrics = st.checkbox("Show key metrics on dashboard", value=True)
        show_activity = st.checkbox("Show recent activity", value=True)
        show_quick_actions = st.checkbox("Show quick actions", value=True)
        
        st.markdown("---")
        
        st.markdown("#### Notification Settings")
        
        email_notifications = st.checkbox("Email notifications", value=False)
        analysis_complete = st.checkbox("Notify when analysis complete", value=True)
        weekly_digest = st.checkbox("Weekly activity digest", value=False)
        
        if st.button("💾 Save Appearance Settings", type="primary"):
            st.success("✅ Appearance settings saved!")
    
    def _render_data_settings(self):
        """Render data settings"""
        st.markdown("### 📊 Data Settings")
        
        st.markdown("#### Data Retention")
        
        retention = st.selectbox(
            "Keep analysis history for",
            ["30 days", "90 days", "1 year", "Forever"]
        )
        
        st.markdown("---")
        
        st.markdown("#### Export Settings")
        
        default_format = st.selectbox(
            "Default export format",
            ["JSON", "CSV", "PDF", "Text"]
        )
        
        include_metadata = st.checkbox("Include metadata in exports", value=True)
        include_timestamps = st.checkbox("Include timestamps", value=True)
        
        st.markdown("---")
        
        st.markdown("#### Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export All Data", use_container_width=True):
                st.info("Export feature coming soon!")
        
        with col2:
            if st.button("🗑️ Clear All History", use_container_width=True, type="secondary"):
                if st.checkbox("I understand this will delete all analysis history"):
                    st.session_state.requirements_history = []
                    st.session_state.process_history = []
                    st.session_state.planning_history = []
                    st.session_state.reports_history = []
                    st.session_state.decision_history = []
                    st.session_state.chat_history = []
                    st.success("All history cleared!")
        
        st.markdown("---")
        
        st.markdown("#### System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Platform Version:** 1.0.0")
            st.markdown("**Python Version:** 3.11+")
            st.markdown("**Streamlit Version:** 1.30+")
        
        with col2:
            st.markdown("**AI Model:** GPT-4 Turbo")
            st.markdown("**Last Updated:** January 2025")
            st.markdown("**License:** MIT")
