"""
Process Optimization Module
AI-powered manufacturing process analysis and optimization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from modules.ai_service import AIService

class ProcessOptimizer:
    """Manufacturing Process Optimization Module"""
    
    def __init__(self):
        self.ai_service = AIService()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for process module"""
        if 'process_history' not in st.session_state:
            st.session_state.process_history = []
        if 'current_optimization' not in st.session_state:
            st.session_state.current_optimization = None
    
    def render(self):
        """Render the Process Optimization interface"""
        st.markdown('<p class="main-header">⚙️ Process Optimization</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-driven analysis and optimization of manufacturing processes</p>', unsafe_allow_html=True)
        
        # Check if AI is configured
        if not self.ai_service.is_configured():
            st.warning("⚠️ Groq API key not configured. Please add your API key in Settings to enable AI analysis.")
        
        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Process Analysis", "📊 Metrics Dashboard", "📈 Optimization History", "🎯 Benchmarks"])
        
        with tab1:
            self._render_process_analysis()
        
        with tab2:
            self._render_metrics_dashboard()
        
        with tab3:
            self._render_optimization_history()
        
        with tab4:
            self._render_benchmarks()
    
    def _render_process_analysis(self):
        """Render the process analysis form"""
        st.markdown("### 🔍 Analyze & Optimize Process")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Process Information
            st.markdown("#### Process Information")
            
            process_name = st.text_input("Process Name", placeholder="e.g., Assembly Line A - Widget Production")
            
            process_type = st.selectbox(
                "Process Type",
                [
                    "Assembly",
                    "Machining",
                    "Fabrication",
                    "Quality Inspection",
                    "Packaging",
                    "Material Handling",
                    "Testing",
                    "Maintenance",
                    "Other"
                ]
            )
            
            process_description = st.text_area(
                "Process Description",
                placeholder="""Describe the process in detail:
- What are the main steps?
- What equipment is used?
- What are the inputs and outputs?
- What are the current challenges?
- What is the current performance level?""",
                height=200
            )
        
        with col2:
            st.markdown("#### Current Metrics")
            
            col2a, col2b = st.columns(2)
            
            with col2a:
                cycle_time = st.number_input("Cycle Time (min)", min_value=0.0, value=10.0, step=0.5)
                oee = st.number_input("OEE (%)", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
            
            with col2b:
                defect_rate = st.number_input("Defect Rate (%)", min_value=0.0, max_value=100.0, value=2.5, step=0.1)
                throughput = st.number_input("Daily Throughput", min_value=0, value=500, step=10)
            
            st.markdown("---")
            
            downtime = st.number_input("Avg Downtime (hrs/week)", min_value=0.0, value=4.0, step=0.5)
            changeover_time = st.number_input("Changeover Time (min)", min_value=0.0, value=30.0, step=5.0)
            
            labor_cost = st.number_input("Labor Cost ($/unit)", min_value=0.0, value=5.0, step=0.5)
        
        st.markdown("---")
        
        # Constraints and Goals
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Constraints")
            constraints = st.text_area(
                "List any constraints",
                placeholder="e.g., Budget limits, space constraints, equipment limitations, regulatory requirements...",
                height=100
            )
        
        with col2:
            st.markdown("#### Optimization Goals")
            goals = st.multiselect(
                "Select optimization goals",
                [
                    "Reduce Cycle Time",
                    "Improve OEE",
                    "Reduce Defect Rate",
                    "Increase Throughput",
                    "Reduce Downtime",
                    "Lower Labor Costs",
                    "Reduce Changeover Time",
                    "Improve Quality",
                    "Reduce Waste",
                    "Energy Efficiency"
                ],
                default=["Improve OEE", "Reduce Defect Rate"]
            )
        
        st.markdown("---")
        
        # Analysis Options
        st.markdown("#### Analysis Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_lean = st.checkbox("Lean Manufacturing Analysis", value=True)
            include_six_sigma = st.checkbox("Six Sigma Recommendations", value=True)
        
        with col2:
            include_automation = st.checkbox("Automation Opportunities", value=True)
            include_roi = st.checkbox("ROI Calculations", value=True)
        
        with col3:
            include_implementation = st.checkbox("Implementation Roadmap", value=True)
            include_kpis = st.checkbox("KPI Recommendations", value=True)
        
        # Analyze Button
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🔍 Analyze & Optimize", type="primary", use_container_width=True):
                if not process_description.strip():
                    st.error("Please describe the process to analyze.")
                elif not self.ai_service.is_configured():
                    st.error("Please configure your Groq API key in Settings first.")
                else:
                    metrics = {
                        "cycle_time_min": cycle_time,
                        "oee_percent": oee,
                        "defect_rate_percent": defect_rate,
                        "daily_throughput": throughput,
                        "downtime_hrs_week": downtime,
                        "changeover_time_min": changeover_time,
                        "labor_cost_per_unit": labor_cost
                    }
                    
                    self._run_optimization(
                        process_name=process_name,
                        process_type=process_type,
                        process_description=process_description,
                        metrics=metrics,
                        constraints=constraints,
                        goals=goals
                    )
        
        # Display results
        if st.session_state.current_optimization:
            self._display_optimization_results(st.session_state.current_optimization)
    
    def _run_optimization(self, **kwargs):
        """Run the AI optimization analysis"""
        with st.spinner("🤖 AI is analyzing your process and generating optimization recommendations..."):
            # Build full description with metrics
            full_description = f"""
Process Name: {kwargs.get('process_name', 'Unnamed')}
Process Type: {kwargs.get('process_type', 'General')}

Description:
{kwargs.get('process_description', '')}

Constraints:
{kwargs.get('constraints', 'None specified')}

Optimization Goals:
{', '.join(kwargs.get('goals', []))}
"""
            
            result = self.ai_service.optimize_process(
                process_description=full_description,
                metrics=kwargs.get('metrics', {})
            )
            
            if 'error' in result:
                st.error(f"❌ {result['error']}")
            else:
                # Save to session state
                optimization_record = {
                    'timestamp': datetime.now().isoformat(),
                    'process_name': kwargs.get('process_name', 'Unnamed'),
                    'process_type': kwargs.get('process_type', ''),
                    'metrics': kwargs.get('metrics', {}),
                    'optimization': result.get('optimization', ''),
                    'goals': kwargs.get('goals', [])
                }
                
                st.session_state.current_optimization = optimization_record
                st.session_state.process_history.append(optimization_record)
                st.success("✅ Optimization analysis complete!")
    
    def _display_optimization_results(self, optimization_record):
        """Display the optimization results"""
        st.markdown("---")
        st.markdown("### 📊 Optimization Recommendations")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Process:** {optimization_record.get('process_name', 'Unnamed')}")
            st.markdown(f"**Analyzed:** {optimization_record.get('timestamp', '')[:19]}")
        
        with col2:
            goals = optimization_record.get('goals', [])
            if goals:
                st.markdown(f"**Goals:** {', '.join(goals)}")
        
        # Display metrics visualization
        metrics = optimization_record.get('metrics', {})
        if metrics:
            st.markdown("#### Current Performance Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("OEE", f"{metrics.get('oee_percent', 0):.1f}%", 
                         delta=f"{85 - metrics.get('oee_percent', 0):.1f}% to target" if metrics.get('oee_percent', 0) < 85 else "On target")
            
            with col2:
                st.metric("Defect Rate", f"{metrics.get('defect_rate_percent', 0):.2f}%",
                         delta=f"-{metrics.get('defect_rate_percent', 0) - 1:.2f}% needed" if metrics.get('defect_rate_percent', 0) > 1 else "Good")
            
            with col3:
                st.metric("Cycle Time", f"{metrics.get('cycle_time_min', 0):.1f} min")
            
            with col4:
                st.metric("Throughput", f"{metrics.get('daily_throughput', 0):,}/day")
        
        # Display AI recommendations
        st.markdown("---")
        st.markdown("#### 💡 AI Optimization Recommendations")
        
        optimization = optimization_record.get('optimization', '')
        st.markdown(optimization)
        
        # Export options
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            export_data = json.dumps(optimization_record, indent=2)
            st.download_button(
                label="📥 Export as JSON",
                data=export_data,
                file_name=f"process_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            text_report = f"""Process Optimization Report
{'='*50}

Process: {optimization_record.get('process_name', '')}
Type: {optimization_record.get('process_type', '')}
Date: {optimization_record.get('timestamp', '')}

Current Metrics:
{json.dumps(metrics, indent=2)}

Goals: {', '.join(optimization_record.get('goals', []))}

Optimization Recommendations:
{optimization}
"""
            st.download_button(
                label="📄 Export as Text",
                data=text_report,
                file_name=f"process_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col3:
            if st.button("🔄 New Analysis"):
                st.session_state.current_optimization = None
                st.rerun()
    
    def _render_metrics_dashboard(self):
        """Render the metrics dashboard"""
        st.markdown("### 📊 Process Metrics Dashboard")
        
        # Sample data for demonstration
        st.info("💡 Connect to your data sources to see real-time metrics. Showing sample data for demonstration.")
        
        # OEE Trend
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### OEE Trend (Last 30 Days)")
            
            import numpy as np
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            oee_data = 75 + np.random.randn(30).cumsum() * 0.5
            oee_data = np.clip(oee_data, 60, 95)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=oee_data,
                mode='lines+markers',
                name='OEE',
                line=dict(color='#667eea', width=2),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)'
            ))
            fig.add_hline(y=85, line_dash="dash", line_color="green", annotation_text="Target: 85%")
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                yaxis_title="OEE %"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Defect Rate by Category")
            
            defect_categories = ['Assembly', 'Material', 'Machine', 'Operator', 'Design']
            defect_values = [35, 25, 20, 12, 8]
            
            fig = px.pie(
                values=defect_values,
                names=defect_categories,
                color_discrete_sequence=px.colors.sequential.Purples_r
            )
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        # Production metrics
        st.markdown("#### Production Metrics Comparison")
        
        processes = ['Assembly A', 'Assembly B', 'Machining', 'Packaging', 'QC']
        
        metrics_df = pd.DataFrame({
            'Process': processes,
            'OEE (%)': [82, 78, 85, 88, 92],
            'Defect Rate (%)': [2.1, 3.2, 1.8, 1.2, 0.5],
            'Cycle Time (min)': [12, 15, 8, 5, 10],
            'Throughput': [450, 380, 520, 680, 420]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='OEE (%)', x=processes, y=metrics_df['OEE (%)'], marker_color='#667eea'))
        fig.add_trace(go.Bar(name='Target (85%)', x=processes, y=[85]*5, marker_color='rgba(0,200,0,0.3)'))
        
        fig.update_layout(
            barmode='overlay',
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed metrics table
        st.markdown("#### Detailed Metrics")
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    
    def _render_optimization_history(self):
        """Render optimization history"""
        st.markdown("### 📈 Optimization History")
        
        if not st.session_state.process_history:
            st.info("No optimization analyses found. Run a process analysis to see history.")
            return
        
        for i, record in enumerate(reversed(st.session_state.process_history)):
            with st.expander(f"⚙️ {record.get('process_name', 'Unnamed')} - {record.get('timestamp', '')[:10]}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Type:** {record.get('process_type', 'N/A')}")
                    st.markdown(f"**Goals:** {', '.join(record.get('goals', []))}")
                
                with col2:
                    metrics = record.get('metrics', {})
                    if metrics:
                        st.markdown(f"**OEE:** {metrics.get('oee_percent', 'N/A')}%")
                        st.markdown(f"**Defect Rate:** {metrics.get('defect_rate_percent', 'N/A')}%")
                
                if st.button(f"View Full Analysis", key=f"view_opt_{i}"):
                    st.session_state.current_optimization = record
                    st.rerun()
    
    def _render_benchmarks(self):
        """Render industry benchmarks"""
        st.markdown("### 🎯 Industry Benchmarks")
        
        st.markdown("""
        Compare your manufacturing performance against industry standards and world-class benchmarks.
        """)
        
        # Benchmark data
        benchmarks = {
            'Metric': ['OEE', 'Defect Rate', 'On-Time Delivery', 'Inventory Turns', 'Changeover Time Reduction'],
            'World Class': ['85%+', '<100 PPM', '99%+', '12+', '90%+ reduction'],
            'Industry Average': ['60-70%', '1-3%', '90-95%', '4-8', '50% reduction'],
            'Your Target': ['85%', '<1%', '98%', '10', '75% reduction']
        }
        
        benchmark_df = pd.DataFrame(benchmarks)
        
        st.dataframe(benchmark_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("#### OEE Components Benchmark")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### Availability")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=88,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Current"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#667eea"},
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("**Target:** 90%+ | **World Class:** 95%+")
        
        with col2:
            st.markdown("##### Performance")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=92,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Current"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#667eea"},
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("**Target:** 95%+ | **World Class:** 98%+")
        
        with col3:
            st.markdown("##### Quality")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=97.5,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Current"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#667eea"},
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 99
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("**Target:** 99%+ | **World Class:** 99.9%+")
