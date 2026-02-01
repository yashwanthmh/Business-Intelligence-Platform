"""
Reports & Analytics Module
AI-powered report generation and business analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import numpy as np
from modules.ai_service import AIService

class ReportsAnalytics:
    """Reports & Analytics Module"""
    
    def __init__(self):
        self.ai_service = AIService()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for reports module"""
        if 'reports_history' not in st.session_state:
            st.session_state.reports_history = []
        if 'current_report' not in st.session_state:
            st.session_state.current_report = None
    
    def render(self):
        """Render the Reports & Analytics interface"""
        st.markdown('<p class="main-header">📈 Reports & Analytics</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-generated executive reports and business intelligence</p>', unsafe_allow_html=True)
        
        if not self.ai_service.is_configured():
            st.warning("⚠️ Groq API key not configured. Please add your API key in Settings.")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Generate Report", "📊 Analytics Dashboard", "📚 Report Library", "📑 Templates"])
        
        with tab1:
            self._render_generate_report()
        with tab2:
            self._render_analytics_dashboard()
        with tab3:
            self._render_report_library()
        with tab4:
            self._render_report_templates()
    
    def _render_generate_report(self):
        """Render report generation interface"""
        st.markdown("### 📝 Generate Executive Report")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            report_name = st.text_input("Report Name", placeholder="e.g., Q1 2026 Manufacturing Performance")
            
            report_type = st.selectbox("Report Type", [
                "Executive Summary Report",
                "Operational Performance Report", 
                "Financial Analysis Report",
                "Quality Performance Report",
                "Project Status Report",
                "KPI Dashboard Report",
                "Trend Analysis Report",
                "Custom Report"
            ])
            
            data_method = st.radio("Data Input", ["Manual Entry", "Sample Data"], horizontal=True)
            
            if data_method == "Manual Entry":
                col1a, col1b = st.columns(2)
                with col1a:
                    revenue = st.number_input("Revenue ($)", value=5000000, step=100000)
                    production = st.number_input("Production Volume", value=25000, step=1000)
                    oee = st.number_input("OEE (%)", value=82.5, step=0.5)
                    quality = st.number_input("Quality Rate (%)", value=97.8, step=0.1)
                with col1b:
                    cost_unit = st.number_input("Cost/Unit ($)", value=45.50, step=0.50)
                    otd = st.number_input("On-Time Delivery (%)", value=94.5, step=0.5)
                    defects = st.number_input("Defect Rate (%)", value=2.2, step=0.1)
                    employees = st.number_input("Employees", value=250, step=10)
                
                report_data = {
                    "revenue": revenue, "production_volume": production, "oee": oee,
                    "quality_rate": quality, "cost_per_unit": cost_unit,
                    "on_time_delivery": otd, "defect_rate": defects, "employees": employees
                }
            else:
                report_data = {
                    "period": "Q1 2026", "revenue": 5250000, "production_volume": 26500,
                    "oee": 84.2, "quality_rate": 98.1, "cost_per_unit": 44.25,
                    "on_time_delivery": 95.8, "defect_rate": 1.9, "employees": 255,
                    "revenue_vs_target": "+5.2%", "production_vs_target": "+6.0%",
                    "top_products": ["Widget A", "Component B", "Assembly C"],
                    "challenges": ["Supply chain delays", "Equipment maintenance"],
                    "achievements": ["Record production month", "Zero safety incidents"]
                }
                st.json(report_data)
        
        with col2:
            st.markdown("#### Report Settings")
            period = st.selectbox("Period", ["Q1 2026", "Q4 2025", "Full Year 2025", "Custom"])
            audience = st.selectbox("Audience", ["Executive Team", "Board of Directors", "Operations", "All Stakeholders"])
            
            st.markdown("#### Include Sections")
            inc_summary = st.checkbox("Executive Summary", value=True)
            inc_performance = st.checkbox("Performance Analysis", value=True)
            inc_trends = st.checkbox("Trend Analysis", value=True)
            inc_recommendations = st.checkbox("Recommendations", value=True)
            inc_outlook = st.checkbox("Forward Outlook", value=True)
            
            additional_context = st.text_area("Additional Context", height=100, 
                placeholder="Any specific areas to focus on...")
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📊 Generate Report", type="primary", use_container_width=True):
                if not self.ai_service.is_configured():
                    st.error("Please configure your Groq API key in Settings.")
                else:
                    self._generate_report(
                        report_name=report_name, report_type=report_type,
                        data=report_data, period=period, audience=audience,
                        context=additional_context
                    )
        
        if st.session_state.current_report:
            self._display_report(st.session_state.current_report)
    
    def _generate_report(self, **kwargs):
        """Generate report using AI"""
        with st.spinner("🤖 AI is generating your executive report..."):
            parameters = {
                "period": kwargs.get('period'),
                "audience": kwargs.get('audience'),
                "additional_context": kwargs.get('context')
            }
            
            result = self.ai_service.generate_report(
                report_type=kwargs.get('report_type', 'Executive Report'),
                data=kwargs.get('data', {}),
                parameters=parameters
            )
            
            if 'error' in result:
                st.error(f"❌ {result['error']}")
            else:
                record = {
                    'timestamp': datetime.now().isoformat(),
                    'report_name': kwargs.get('report_name', 'Unnamed Report'),
                    'report_type': kwargs.get('report_type'),
                    'period': kwargs.get('period'),
                    'report': result.get('report', ''),
                    'data': kwargs.get('data', {})
                }
                st.session_state.current_report = record
                st.session_state.reports_history.append(record)
                st.success("✅ Report generated!")
    
    def _display_report(self, record):
        """Display generated report"""
        st.markdown("---")
        st.markdown("### 📋 Generated Report")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Report:** {record.get('report_name', 'Unnamed')}")
        with col2:
            st.markdown(f"**Type:** {record.get('report_type', 'N/A')}")
        with col3:
            st.markdown(f"**Period:** {record.get('period', 'N/A')}")
        
        st.markdown("---")
        st.markdown(record.get('report', ''))
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button("📥 Export JSON", json.dumps(record, indent=2),
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "application/json")
        with col2:
            text = f"Report: {record.get('report_name')}\n{'='*50}\n\n{record.get('report', '')}"
            st.download_button("📄 Export Text", text,
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "text/plain")
        with col3:
            if st.button("🔄 New Report"):
                st.session_state.current_report = None
                st.rerun()
    
    def _render_analytics_dashboard(self):
        """Render analytics dashboard"""
        st.markdown("### 📊 Analytics Dashboard")
        st.info("💡 Showing sample data. Connect your data sources for real-time analytics.")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Revenue", "$5.25M", "+5.2%")
        with col2:
            st.metric("Production", "26,500 units", "+6.0%")
        with col3:
            st.metric("OEE", "84.2%", "+2.1%")
        with col4:
            st.metric("Quality", "98.1%", "+0.3%")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Revenue Trend")
            months = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
            revenue = [4.8, 4.9, 5.1, 5.0, 5.2, 5.4]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=revenue, mode='lines+markers', 
                fill='tozeroy', line=dict(color='#667eea')))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), yaxis_title="Revenue ($M)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Production by Line")
            lines = ['Line A', 'Line B', 'Line C', 'Line D']
            production = [8500, 7200, 6800, 4000]
            fig = px.bar(x=lines, y=production, color=production, 
                color_continuous_scale='Purples')
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), 
                yaxis_title="Units", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Quality by Category")
            categories = ['Dimensional', 'Visual', 'Functional', 'Packaging']
            defects = [35, 28, 22, 15]
            fig = px.pie(values=defects, names=categories, 
                color_discrete_sequence=px.colors.sequential.Purples_r)
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### OEE Components")
            components = ['Availability', 'Performance', 'Quality']
            values = [90.5, 92.3, 98.1]
            colors = ['#667eea', '#764ba2', '#10B981']
            fig = go.Figure(go.Bar(x=components, y=values, marker_color=colors))
            fig.add_hline(y=85, line_dash="dash", annotation_text="Target")
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), yaxis_title="%")
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_report_library(self):
        """Render report library"""
        st.markdown("### 📚 Report Library")
        
        if not st.session_state.reports_history:
            st.info("No reports generated yet. Create your first report in 'Generate Report' tab.")
            return
        
        for i, record in enumerate(reversed(st.session_state.reports_history)):
            with st.expander(f"📊 {record.get('report_name', 'Unnamed')} - {record.get('timestamp', '')[:10]}"):
                st.markdown(f"**Type:** {record.get('report_type', 'N/A')}")
                st.markdown(f"**Period:** {record.get('period', 'N/A')}")
                
                if st.button(f"View Report", key=f"view_report_{i}"):
                    st.session_state.current_report = record
                    st.rerun()
    
    def _render_report_templates(self):
        """Render report templates"""
        st.markdown("### 📑 Report Templates")
        
        templates = {
            "Executive Summary": "High-level overview for C-suite with key metrics and strategic highlights",
            "Operational Performance": "Detailed operational KPIs, OEE analysis, and process metrics",
            "Financial Analysis": "Revenue, costs, margins, and financial performance indicators",
            "Quality Report": "Defect analysis, quality trends, and compliance status",
            "Project Status": "Initiative progress, milestones, and resource utilization"
        }
        
        for name, desc in templates.items():
            with st.expander(f"📄 {name}"):
                st.markdown(f"*{desc}*")
                st.markdown("**Typical Sections:**")
                st.markdown("- Executive Summary\n- Key Metrics\n- Trend Analysis\n- Recommendations")
                if st.button(f"Use Template", key=f"template_{name}"):
                    st.info(f"Template '{name}' selected. Go to 'Generate Report' tab.")
