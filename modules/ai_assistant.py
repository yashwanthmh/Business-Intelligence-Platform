"""
AI Assistant Module
Conversational AI assistant for business analysis
"""

import streamlit as st
from datetime import datetime
from modules.ai_service import AIService

class AIAssistant:
    """Conversational AI Assistant Module"""
    
    def __init__(self):
        self.ai_service = AIService()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'conversation_context' not in st.session_state:
            st.session_state.conversation_context = []
    
    def render(self):
        """Render the AI Assistant interface"""
        st.markdown('<p class="main-header">💬 AI Assistant</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Your intelligent business analysis companion</p>', unsafe_allow_html=True)
        
        if not self.ai_service.is_configured():
            st.warning("⚠️ Groq API key not configured. Please add your API key in Settings to chat with AI.")
        
        # Sidebar for assistant options
        with st.sidebar:
            st.markdown("### 💬 Assistant Options")
            
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.conversation_context = []
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 💡 Quick Prompts")
            
            quick_prompts = [
                "Analyze our OEE performance",
                "Suggest process improvements",
                "Create a project timeline",
                "Review quality metrics",
                "Recommend cost reductions",
                "Draft executive summary"
            ]
            
            for prompt in quick_prompts:
                if st.button(prompt, key=f"quick_{prompt}", use_container_width=True):
                    self._process_message(prompt)
        
        # Main chat area
        self._render_chat_interface()
    
    def _render_chat_interface(self):
        """Render the main chat interface"""
        
        # Chat container
        chat_container = st.container()
        
        # Display chat history
        with chat_container:
            if not st.session_state.chat_history:
                # Welcome message
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 2rem; border-radius: 12px; color: white; margin-bottom: 1rem;">
                    <h3>👋 Hello! I'm your AI Business Analyst</h3>
                    <p>I can help you with:</p>
                    <ul>
                        <li><strong>Requirements Analysis</strong> - Analyze and structure business requirements</li>
                        <li><strong>Process Optimization</strong> - Identify improvement opportunities</li>
                        <li><strong>Strategic Planning</strong> - Develop plans and roadmaps</li>
                        <li><strong>Report Generation</strong> - Create executive summaries and reports</li>
                        <li><strong>Decision Support</strong> - Analyze options and provide recommendations</li>
                    </ul>
                    <p><em>Ask me anything about your manufacturing operations!</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display messages
            for message in st.session_state.chat_history:
                role = message.get('role', 'user')
                content = message.get('content', '')
                timestamp = message.get('timestamp', '')
                
                if role == 'user':
                    with st.chat_message("user"):
                        st.markdown(content)
                        st.caption(timestamp)
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(content)
                        st.caption(timestamp)
        
        # Input area
        st.markdown("---")
        
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.chat_input("Ask me anything about business analysis...")
        
        if user_input:
            self._process_message(user_input)
    
    def _process_message(self, message: str):
        """Process user message and get AI response"""
        # Add user message to history
        user_msg = {
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().strftime('%H:%M')
        }
        st.session_state.chat_history.append(user_msg)
        
        # Add to conversation context for AI
        st.session_state.conversation_context.append({
            'role': 'user',
            'content': message
        })
        
        # Get AI response
        if not self.ai_service.is_configured():
            assistant_msg = {
                'role': 'assistant',
                'content': "⚠️ I'm not configured yet. Please add your Groq API key in the Settings to chat with me.",
                'timestamp': datetime.now().strftime('%H:%M')
            }
        else:
            with st.spinner("🤔 Thinking..."):
                result = self.ai_service.chat(
                    message=message,
                    conversation_history=st.session_state.conversation_context[-10:]  # Last 10 messages for context
                )
                
                if 'error' in result:
                    response = f"❌ Sorry, I encountered an error: {result['error']}"
                else:
                    response = result.get('response', "I'm sorry, I couldn't generate a response.")
                
                assistant_msg = {
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().strftime('%H:%M')
                }
                
                # Add to conversation context
                st.session_state.conversation_context.append({
                    'role': 'assistant',
                    'content': response
                })
        
        st.session_state.chat_history.append(assistant_msg)
        st.rerun()
