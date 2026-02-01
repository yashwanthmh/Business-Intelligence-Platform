"""
Decision Support Module
AI-powered executive decision support and analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from modules.ai_service import AIService

class DecisionSupport:
    """Executive Decision Support Module"""
    
    def __init__(self):
        self.ai_service = AIService()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state"""
        if 'decision_history' not in st.session_state:
            st.session_state.decision_history = []
        if 'current_decision' not in st.session_state:
            st.session_state.current_decision = None
    
    def render(self):
        """Render the Decision Support interface"""
        st.markdown('<p class="main-header">🎯 Decision Support</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-powered analysis for executive decision-making</p>', unsafe_allow_html=True)
        
        if not self.ai_service.is_configured():
            st.warning("⚠️ Groq API key not configured. Please add your API key in Settings.")
        
        tab1, tab2, tab3 = st.tabs(["🔍 New Decision Analysis", "📊 Decision Matrix", "📚 Decision History"])
        
        with tab1:
            self._render_decision_analysis()
        with tab2:
            self._render_decision_matrix()
        with tab3:
            self._render_decision_history()
    
    def _render_decision_analysis(self):
        """Render decision analysis form"""
        st.markdown("### 🔍 Decision Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            decision_title = st.text_input("Decision Title", 
                placeholder="e.g., New Equipment Investment Decision")
            
            decision_type = st.selectbox("Decision Type", [
                "Investment Decision",
                "Make vs Buy Decision",
                "Strategic Direction",
                "Resource Allocation",
                "Vendor Selection",
                "Process Change",
                "Capacity Planning",
                "Risk Management",
                "Other"
            ])
            
            decision_context = st.text_area("Decision Context",
                placeholder="""Describe the decision context:
- What is the business need?
- What triggered this decision?
- What are the constraints?
- What is the timeline?
- Who are the stakeholders?""",
                height=200)
        
        with col2:
            st.markdown("#### Decision Parameters")
            
            urgency = st.select_slider("Urgency", 
                options=["Low", "Medium", "High", "Critical"])
            
            impact = st.select_slider("Business Impact",
                options=["Minor", "Moderate", "Significant", "Major"])
            
            reversibility = st.select_slider("Reversibility",
                options=["Easily Reversible", "Somewhat Reversible", "Difficult to Reverse", "Irreversible"])
            
            budget_impact = st.text_input("Budget Impact", placeholder="e.g., $500K - $1M")
        
        st.markdown("---")
        
        # Options
        st.markdown("#### Options Under Consideration")
        
        num_options = st.number_input("Number of Options", min_value=2, max_value=6, value=3)
        
        options = []
        cols = st.columns(min(num_options, 3))
        
        for i in range(num_options):
            with cols[i % 3]:
                option = st.text_area(f"Option {i+1}", 
                    placeholder=f"Describe option {i+1}...",
                    height=100,
                    key=f"option_{i}")
                if option:
                    options.append(option)
        
        st.markdown("---")
        
        # Criteria
        st.markdown("#### Evaluation Criteria")
        
        default_criteria = [
            "Financial Impact/ROI",
            "Strategic Alignment",
            "Implementation Risk",
            "Timeline Feasibility",
            "Resource Requirements",
            "Stakeholder Acceptance"
        ]
        
        criteria = st.multiselect("Select Criteria", 
            default_criteria + ["Quality Impact", "Scalability", "Flexibility", "Competitive Advantage"],
            default=default_criteria[:4])
        
        custom_criteria = st.text_input("Add Custom Criteria (comma-separated)", 
            placeholder="e.g., Environmental Impact, Regulatory Compliance")
        
        if custom_criteria:
            criteria.extend([c.strip() for c in custom_criteria.split(",") if c.strip()])
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 Analyze Decision", type="primary", use_container_width=True):
                if not decision_context.strip():
                    st.error("Please describe the decision context.")
                elif len(options) < 2:
                    st.error("Please provide at least 2 options.")
                elif not self.ai_service.is_configured():
                    st.error("Please configure your Groq API key in Settings.")
                else:
                    self._run_decision_analysis(
                        title=decision_title,
                        decision_type=decision_type,
                        context=decision_context,
                        options=options,
                        criteria=criteria,
                        urgency=urgency,
                        impact=impact,
                        reversibility=reversibility,
                        budget=budget_impact
                    )
        
        if st.session_state.current_decision:
            self._display_decision_results(st.session_state.current_decision)
    
    def _run_decision_analysis(self, **kwargs):
        """Run AI decision analysis"""
        with st.spinner("🤖 AI is analyzing your decision..."):
            full_context = f"""
Decision: {kwargs.get('title', 'Untitled')}
Type: {kwargs.get('decision_type', 'General')}
Urgency: {kwargs.get('urgency', 'Medium')}
Business Impact: {kwargs.get('impact', 'Moderate')}
Reversibility: {kwargs.get('reversibility', 'Unknown')}
Budget Impact: {kwargs.get('budget', 'Not specified')}

Context:
{kwargs.get('context', '')}
"""
            
            result = self.ai_service.decision_analysis(
                decision_context=full_context,
                options=kwargs.get('options', []),
                criteria=kwargs.get('criteria', [])
            )
            
            if 'error' in result:
                st.error(f"❌ {result['error']}")
            else:
                record = {
                    'timestamp': datetime.now().isoformat(),
                    'title': kwargs.get('title', 'Untitled Decision'),
                    'decision_type': kwargs.get('decision_type'),
                    'options': kwargs.get('options', []),
                    'criteria': kwargs.get('criteria', []),
                    'analysis': result.get('analysis', ''),
                    'urgency': kwargs.get('urgency'),
                    'impact': kwargs.get('impact')
                }
                st.session_state.current_decision = record
                st.session_state.decision_history.append(record)
                st.success("✅ Decision analysis complete!")
    
    def _display_decision_results(self, record):
        """Display decision analysis results"""
        st.markdown("---")
        st.markdown("### 📊 Decision Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Decision:** {record.get('title', 'Untitled')}")
        with col2:
            st.markdown(f"**Type:** {record.get('decision_type', 'N/A')}")
        with col3:
            st.markdown(f"**Urgency:** {record.get('urgency', 'N/A')}")
        
        st.markdown("---")
        
        # Options summary
        st.markdown("#### Options Analyzed")
        options = record.get('options', [])
        cols = st.columns(len(options))
        for i, (col, opt) in enumerate(zip(cols, options)):
            with col:
                st.markdown(f"**Option {i+1}**")
                st.markdown(opt[:100] + "..." if len(opt) > 100 else opt)
        
        st.markdown("---")
        st.markdown("#### AI Analysis & Recommendation")
        st.markdown(record.get('analysis', ''))
        
        # Export
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button("📥 Export JSON", json.dumps(record, indent=2),
                f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "application/json")
        with col2:
            text = f"Decision Analysis: {record.get('title')}\n{'='*50}\n\n{record.get('analysis', '')}"
            st.download_button("📄 Export Text", text,
                f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "text/plain")
        with col3:
            if st.button("🔄 New Analysis"):
                st.session_state.current_decision = None
                st.rerun()
    
    def _render_decision_matrix(self):
        """Render interactive decision matrix"""
        st.markdown("### 📊 Decision Matrix Tool")
        st.markdown("Use this tool to score and compare options against criteria.")
        
        col1, col2 = st.columns(2)
        with col1:
            num_options = st.number_input("Number of Options", 2, 5, 3, key="matrix_options")
        with col2:
            num_criteria = st.number_input("Number of Criteria", 2, 8, 4, key="matrix_criteria")
        
        # Input options and criteria
        st.markdown("#### Define Options and Criteria")
        
        col1, col2 = st.columns(2)
        with col1:
            options = []
            for i in range(num_options):
                opt = st.text_input(f"Option {i+1}", value=f"Option {chr(65+i)}", key=f"opt_{i}")
                options.append(opt)
        
        with col2:
            criteria = []
            weights = []
            for i in range(num_criteria):
                crit = st.text_input(f"Criterion {i+1}", value=f"Criterion {i+1}", key=f"crit_{i}")
                criteria.append(crit)
        
        # Weight input
        st.markdown("#### Criteria Weights (total should equal 100)")
        weight_cols = st.columns(num_criteria)
        for i, col in enumerate(weight_cols):
            with col:
                w = st.number_input(f"Weight {i+1}", 0, 100, 100//num_criteria, key=f"weight_{i}")
                weights.append(w)
        
        # Scoring matrix
        st.markdown("#### Score Each Option (1-10)")
        
        scores = []
        for i, opt in enumerate(options):
            st.markdown(f"**{opt}**")
            cols = st.columns(num_criteria)
            row_scores = []
            for j, col in enumerate(cols):
                with col:
                    score = st.slider(criteria[j], 1, 10, 5, key=f"score_{i}_{j}")
                    row_scores.append(score)
            scores.append(row_scores)
        
        # Calculate weighted scores
        if st.button("📊 Calculate Results", type="primary"):
            st.markdown("---")
            st.markdown("### Results")
            
            # Build results dataframe
            results_data = []
            for i, opt in enumerate(options):
                weighted_score = sum(scores[i][j] * weights[j] / 100 for j in range(num_criteria))
                results_data.append({
                    'Option': opt,
                    'Raw Total': sum(scores[i]),
                    'Weighted Score': round(weighted_score, 2)
                })
            
            results_df = pd.DataFrame(results_data).sort_values('Weighted Score', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            with col2:
                fig = px.bar(results_df, x='Option', y='Weighted Score', 
                    color='Weighted Score', color_continuous_scale='Purples')
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            winner = results_df.iloc[0]['Option']
            st.success(f"🏆 **Recommended Option: {winner}** (Weighted Score: {results_df.iloc[0]['Weighted Score']})")
    
    def _render_decision_history(self):
        """Render decision history"""
        st.markdown("### 📚 Decision History")
        
        if not st.session_state.decision_history:
            st.info("No decision analyses found. Create your first analysis to see history.")
            return
        
        for i, record in enumerate(reversed(st.session_state.decision_history)):
            with st.expander(f"🎯 {record.get('title', 'Untitled')} - {record.get('timestamp', '')[:10]}"):
                st.markdown(f"**Type:** {record.get('decision_type', 'N/A')}")
                st.markdown(f"**Urgency:** {record.get('urgency', 'N/A')}")
                st.markdown(f"**Options:** {len(record.get('options', []))}")
                
                if st.button(f"View Analysis", key=f"view_dec_{i}"):
                    st.session_state.current_decision = record
                    st.rerun()
