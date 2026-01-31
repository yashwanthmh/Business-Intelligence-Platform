"""
AI-Powered Business Analysis and Decision Intelligence Platform
For Advanced Manufacturing Innovation Organizations

Main Application Entry Point
"""

import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Manufacturing Intelligence Platform",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #5A6C7D;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .module-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .module-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .status-active {
        color: #10B981;
        font-weight: 600;
    }
    .status-pending {
        color: #F59E0B;
        font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True  # Set to True for demo
if 'current_module' not in st.session_state:
    st.session_state.current_module = 'dashboard'

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/factory.png", width=80)
    st.markdown("## 🏭 MIP")
    st.markdown("*Manufacturing Intelligence Platform*")
    st.markdown("---")
    
    # Navigation menu
    st.markdown("### 📍 Navigation")
    
    modules = {
        "📊 Dashboard": "dashboard",
        "📋 Requirements Analysis": "requirements",
        "⚙️ Process Optimization": "process",
        "📅 Strategic Planning": "planning",
        "📈 Reports & Analytics": "reports",
        "🎯 Decision Support": "decisions",
        "💬 AI Assistant": "assistant",
        "⚙️ Settings": "settings"
    }
    
    for label, module in modules.items():
        if st.button(label, key=f"nav_{module}", use_container_width=True):
            st.session_state.current_module = module
    
    st.markdown("---")
    st.markdown("### 🔌 System Status")
    st.markdown("🟢 **AI Engine:** Online")
    st.markdown("🟢 **Database:** Connected")
    st.markdown(f"📅 **Date:** {datetime.now().strftime('%Y-%m-%d')}")

# Main Content Area
def render_dashboard():
    """Render the main dashboard"""
    st.markdown('<p class="main-header">📊 Executive Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time insights for manufacturing intelligence</p>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Active Projects",
            value="24",
            delta="+3 this month"
        )
    
    with col2:
        st.metric(
            label="⚡ Process Efficiency",
            value="94.2%",
            delta="+2.1%"
        )
    
    with col3:
        st.metric(
            label="📋 Requirements Analyzed",
            value="156",
            delta="+12 this week"
        )
    
    with col4:
        st.metric(
            label="💡 AI Recommendations",
            value="38",
            delta="5 pending review"
        )
    
    st.markdown("---")
    
    # Recent Activity and Quick Actions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Recent Analysis Activities")
        
        activities = [
            {"time": "2 hours ago", "action": "Requirements analysis completed", "project": "Smart Factory Phase 2", "status": "✅"},
            {"time": "4 hours ago", "action": "Process optimization report generated", "project": "Assembly Line Automation", "status": "✅"},
            {"time": "6 hours ago", "action": "Strategic planning review", "project": "Q1 2026 Roadmap", "status": "🔄"},
            {"time": "1 day ago", "action": "Decision support analysis", "project": "Equipment Investment", "status": "✅"},
            {"time": "2 days ago", "action": "KPI report generated", "project": "Manufacturing Excellence", "status": "✅"},
        ]
        
        for activity in activities:
            with st.container():
                cols = st.columns([1, 3, 2, 1])
                cols[0].markdown(f"*{activity['time']}*")
                cols[1].markdown(f"**{activity['action']}**")
                cols[2].markdown(f"_{activity['project']}_")
                cols[3].markdown(activity['status'])
    
    with col2:
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📝 New Requirements Analysis", use_container_width=True):
            st.session_state.current_module = 'requirements'
            st.rerun()
        
        if st.button("📊 Generate Report", use_container_width=True):
            st.session_state.current_module = 'reports'
            st.rerun()
        
        if st.button("💬 Ask AI Assistant", use_container_width=True):
            st.session_state.current_module = 'assistant'
            st.rerun()
        
        if st.button("🎯 Decision Analysis", use_container_width=True):
            st.session_state.current_module = 'decisions'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📈 This Week")
        st.progress(0.75, text="Weekly Goals: 75%")

def render_requirements():
    """Render the Requirements Analysis module"""
    from modules.requirements_analysis import RequirementsAnalyzer
    analyzer = RequirementsAnalyzer()
    analyzer.render()

def render_process():
    """Render the Process Optimization module"""
    from modules.process_optimization import ProcessOptimizer
    optimizer = ProcessOptimizer()
    optimizer.render()

def render_planning():
    """Render the Strategic Planning module"""
    from modules.strategic_planning import StrategicPlanner
    planner = StrategicPlanner()
    planner.render()

def render_reports():
    """Render the Reports & Analytics module"""
    from modules.reports_analytics import ReportsAnalytics
    reports = ReportsAnalytics()
    reports.render()

def render_decisions():
    """Render the Decision Support module"""
    from modules.decision_support import DecisionSupport
    decisions = DecisionSupport()
    decisions.render()

def render_assistant():
    """Render the AI Assistant module"""
    from modules.ai_assistant import AIAssistant
    assistant = AIAssistant()
    assistant.render()

def render_settings():
    """Render the Settings module"""
    from modules.settings import Settings
    settings = Settings()
    settings.render()

# Route to appropriate module
module_renderers = {
    'dashboard': render_dashboard,
    'requirements': render_requirements,
    'process': render_process,
    'planning': render_planning,
    'reports': render_reports,
    'decisions': render_decisions,
    'assistant': render_assistant,
    'settings': render_settings
}

# Render current module
current_renderer = module_renderers.get(st.session_state.current_module, render_dashboard)
current_renderer()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; padding: 1rem;'>
        <p>🏭 Manufacturing Intelligence Platform | Powered by AI | © 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)
