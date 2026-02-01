"""
Strategic Planning Module
AI-powered strategic planning for manufacturing organizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from modules.ai_service import AIService

class StrategicPlanner:
    """Strategic Planning Module"""
    
    def __init__(self):
        self.ai_service = AIService()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for planning module"""
        if 'planning_history' not in st.session_state:
            st.session_state.planning_history = []
        if 'current_plan' not in st.session_state:
            st.session_state.current_plan = None
        if 'initiatives' not in st.session_state:
            st.session_state.initiatives = []
    
    def render(self):
        """Render the Strategic Planning interface"""
        st.markdown('<p class="main-header">📅 Strategic Planning</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-assisted strategic planning and roadmap development</p>', unsafe_allow_html=True)
        
        # Check if AI is configured
        if not self.ai_service.is_configured():
            st.warning("⚠️ Groq API key not configured. Please add your API key in Settings to enable AI planning.")
        
        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Create Plan", "🗺️ Roadmap View", "📊 Initiative Tracker", "📚 Plan History"])
        
        with tab1:
            self._render_create_plan()
        
        with tab2:
            self._render_roadmap()
        
        with tab3:
            self._render_initiative_tracker()
        
        with tab4:
            self._render_plan_history()
    
    def _render_create_plan(self):
        """Render the plan creation form"""
        st.markdown("### 📝 Create Strategic Plan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Plan Information
            st.markdown("#### Plan Information")
            
            plan_name = st.text_input("Plan Name", placeholder="e.g., Manufacturing Excellence 2026")
            
            plan_type = st.selectbox(
                "Plan Type",
                [
                    "Annual Strategic Plan",
                    "Digital Transformation Roadmap",
                    "Operational Excellence Initiative",
                    "Innovation Strategy",
                    "Cost Reduction Program",
                    "Quality Improvement Plan",
                    "Capacity Expansion Plan",
                    "Sustainability Initiative",
                    "Other"
                ]
            )
            
            st.markdown("#### Strategic Objectives")
            objectives = st.text_area(
                "Define your strategic objectives",
                placeholder="""List your key strategic objectives:
1. Increase manufacturing efficiency by 20%
2. Reduce production costs by 15%
3. Achieve zero defect manufacturing
4. Implement Industry 4.0 technologies
5. Improve customer delivery performance to 99%

Be specific about what you want to achieve...""",
                height=200
            )
        
        with col2:
            st.markdown("#### Plan Parameters")
            
            timeline = st.selectbox(
                "Planning Horizon",
                ["Q1 2026", "H1 2026", "Full Year 2026", "2026-2027", "3-Year Plan", "5-Year Plan"]
            )
            
            budget = st.text_input("Total Budget", placeholder="e.g., $5M")
            
            priority_areas = st.multiselect(
                "Priority Areas",
                [
                    "Operational Excellence",
                    "Digital Transformation",
                    "Quality Improvement",
                    "Cost Reduction",
                    "Capacity Expansion",
                    "Workforce Development",
                    "Sustainability",
                    "Innovation",
                    "Customer Experience",
                    "Supply Chain"
                ],
                default=["Operational Excellence", "Digital Transformation"]
            )
            
            st.markdown("---")
            
            st.markdown("#### Key Stakeholders")
            stakeholders = st.multiselect(
                "Select stakeholders",
                [
                    "Executive Leadership",
                    "Operations Management",
                    "Engineering",
                    "IT Department",
                    "Quality Assurance",
                    "Finance",
                    "HR",
                    "Supply Chain",
                    "Sales & Marketing",
                    "External Partners"
                ],
                default=["Executive Leadership", "Operations Management"]
            )
        
        st.markdown("---")
        
        # Constraints and Resources
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Constraints & Limitations")
            constraints = st.text_area(
                "List constraints",
                placeholder="""Describe any constraints:
- Budget limitations
- Resource availability
- Regulatory requirements
- Technical limitations
- Market conditions
- Timeline pressures...""",
                height=150
            )
        
        with col2:
            st.markdown("#### Available Resources")
            resources = st.text_area(
                "List available resources",
                placeholder="""Describe available resources:
- Current team capabilities
- Technology infrastructure
- Partner relationships
- Existing initiatives
- Available budget...""",
                height=150
            )
        
        st.markdown("---")
        
        # Planning Options
        st.markdown("#### Planning Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_milestones = st.checkbox("Generate Milestones", value=True)
            include_risks = st.checkbox("Risk Assessment", value=True)
        
        with col2:
            include_metrics = st.checkbox("Success Metrics", value=True)
            include_governance = st.checkbox("Governance Structure", value=True)
        
        with col3:
            include_change_mgmt = st.checkbox("Change Management", value=True)
            include_dependencies = st.checkbox("Dependency Analysis", value=True)
        
        # Generate Plan Button
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🚀 Generate Strategic Plan", type="primary", use_container_width=True):
                if not objectives.strip():
                    st.error("Please define strategic objectives.")
                elif not self.ai_service.is_configured():
                    st.error("Please configure your Groq API key in Settings first.")
                else:
                    self._generate_plan(
                        plan_name=plan_name,
                        plan_type=plan_type,
                        objectives=objectives,
                        timeline=timeline,
                        budget=budget,
                        priority_areas=priority_areas,
                        stakeholders=stakeholders,
                        constraints=constraints,
                        resources=resources
                    )
        
        # Display current plan
        if st.session_state.current_plan:
            self._display_plan_results(st.session_state.current_plan)
    
    def _generate_plan(self, **kwargs):
        """Generate strategic plan using AI"""
        with st.spinner("🤖 AI is generating your strategic plan..."):
            constraints_full = f"""
Constraints: {kwargs.get('constraints', 'None specified')}

Available Resources: {kwargs.get('resources', 'Not specified')}

Budget: {kwargs.get('budget', 'Not specified')}

Priority Areas: {', '.join(kwargs.get('priority_areas', []))}

Stakeholders: {', '.join(kwargs.get('stakeholders', []))}
"""
            
            result = self.ai_service.generate_strategic_plan(
                objectives=kwargs.get('objectives', ''),
                constraints=constraints_full,
                timeline=kwargs.get('timeline', '')
            )
            
            if 'error' in result:
                st.error(f"❌ {result['error']}")
            else:
                # Save to session state
                plan_record = {
                    'timestamp': datetime.now().isoformat(),
                    'plan_name': kwargs.get('plan_name', 'Unnamed Plan'),
                    'plan_type': kwargs.get('plan_type', ''),
                    'timeline': kwargs.get('timeline', ''),
                    'plan': result.get('plan', ''),
                    'objectives': kwargs.get('objectives', ''),
                    'priority_areas': kwargs.get('priority_areas', []),
                    'budget': kwargs.get('budget', '')
                }
                
                st.session_state.current_plan = plan_record
                st.session_state.planning_history.append(plan_record)
                st.success("✅ Strategic plan generated!")
    
    def _display_plan_results(self, plan_record):
        """Display the generated plan"""
        st.markdown("---")
        st.markdown("### 📋 Strategic Plan")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Plan:** {plan_record.get('plan_name', 'Unnamed')}")
        
        with col2:
            st.markdown(f"**Type:** {plan_record.get('plan_type', 'N/A')}")
        
        with col3:
            st.markdown(f"**Timeline:** {plan_record.get('timeline', 'N/A')}")
        
        st.markdown("---")
        
        # Display the plan content
        plan_content = plan_record.get('plan', '')
        st.markdown(plan_content)
        
        # Export options
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            export_data = json.dumps(plan_record, indent=2)
            st.download_button(
                label="📥 Export as JSON",
                data=export_data,
                file_name=f"strategic_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            text_report = f"""Strategic Plan: {plan_record.get('plan_name', '')}
{'='*60}

Type: {plan_record.get('plan_type', '')}
Timeline: {plan_record.get('timeline', '')}
Budget: {plan_record.get('budget', '')}
Generated: {plan_record.get('timestamp', '')}

Objectives:
{plan_record.get('objectives', '')}

Priority Areas: {', '.join(plan_record.get('priority_areas', []))}

{'='*60}

{plan_content}
"""
            st.download_button(
                label="📄 Export as Text",
                data=text_report,
                file_name=f"strategic_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col3:
            if st.button("🔄 Create New Plan"):
                st.session_state.current_plan = None
                st.rerun()
    
    def _render_roadmap(self):
        """Render the roadmap view"""
        st.markdown("### 🗺️ Strategic Roadmap")
        
        st.info("💡 This roadmap shows sample data. Connect your initiatives to see your actual roadmap.")
        
        # Sample roadmap data
        initiatives = [
            {"name": "ERP Upgrade", "start": "2026-01-01", "end": "2026-03-31", "phase": "Digital Transformation", "status": "In Progress"},
            {"name": "Assembly Line Automation", "start": "2026-02-01", "end": "2026-06-30", "phase": "Operational Excellence", "status": "Planning"},
            {"name": "Quality System Enhancement", "start": "2026-01-15", "end": "2026-04-30", "phase": "Quality Improvement", "status": "In Progress"},
            {"name": "IoT Sensor Deployment", "start": "2026-04-01", "end": "2026-07-31", "phase": "Digital Transformation", "status": "Not Started"},
            {"name": "Lean Training Program", "start": "2026-01-01", "end": "2026-12-31", "phase": "Workforce Development", "status": "In Progress"},
            {"name": "Predictive Maintenance", "start": "2026-05-01", "end": "2026-09-30", "phase": "Operational Excellence", "status": "Not Started"},
            {"name": "Supply Chain Optimization", "start": "2026-03-01", "end": "2026-08-31", "phase": "Supply Chain", "status": "Planning"},
            {"name": "Energy Efficiency Program", "start": "2026-06-01", "end": "2026-12-31", "phase": "Sustainability", "status": "Not Started"},
        ]
        
        df = pd.DataFrame(initiatives)
        df['start'] = pd.to_datetime(df['start'])
        df['end'] = pd.to_datetime(df['end'])
        
        # Color map for phases
        color_map = {
            "Digital Transformation": "#667eea",
            "Operational Excellence": "#10B981",
            "Quality Improvement": "#F59E0B",
            "Workforce Development": "#EC4899",
            "Supply Chain": "#8B5CF6",
            "Sustainability": "#06B6D4"
        }
        
        # Create Gantt chart
        fig = px.timeline(
            df,
            x_start="start",
            x_end="end",
            y="name",
            color="phase",
            color_discrete_map=color_map,
            hover_data=["status"]
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Timeline",
            yaxis_title="",
            legend_title="Strategic Phase",
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        fig.update_yaxes(categoryorder="total ascending")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Quarterly milestones
        st.markdown("#### Quarterly Milestones")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("##### Q1 2026")
            st.markdown("""
            - ✅ ERP Phase 1 Go-Live
            - 🔄 Quality System Audit
            - 📋 Automation RFP Complete
            """)
        
        with col2:
            st.markdown("##### Q2 2026")
            st.markdown("""
            - 📋 IoT Pilot Launch
            - 📋 Automation Installation
            - 📋 Supply Chain Assessment
            """)
        
        with col3:
            st.markdown("##### Q3 2026")
            st.markdown("""
            - 📋 ERP Full Deployment
            - 📋 Predictive Maint. Launch
            - 📋 Energy Audit Complete
            """)
        
        with col4:
            st.markdown("##### Q4 2026")
            st.markdown("""
            - 📋 Annual Targets Review
            - 📋 2027 Planning Start
            - 📋 Sustainability Report
            """)
    
    def _render_initiative_tracker(self):
        """Render initiative tracking"""
        st.markdown("### 📊 Initiative Tracker")
        
        # Add new initiative
        with st.expander("➕ Add New Initiative", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Initiative Name", key="new_init_name")
                new_phase = st.selectbox("Strategic Phase", [
                    "Digital Transformation",
                    "Operational Excellence",
                    "Quality Improvement",
                    "Workforce Development",
                    "Supply Chain",
                    "Sustainability"
                ], key="new_init_phase")
                new_owner = st.text_input("Owner", key="new_init_owner")
            
            with col2:
                new_start = st.date_input("Start Date", key="new_init_start")
                new_end = st.date_input("End Date", key="new_init_end")
                new_status = st.selectbox("Status", ["Not Started", "Planning", "In Progress", "On Hold", "Completed"], key="new_init_status")
            
            if st.button("Add Initiative"):
                if new_name:
                    st.session_state.initiatives.append({
                        "name": new_name,
                        "phase": new_phase,
                        "owner": new_owner,
                        "start": str(new_start),
                        "end": str(new_end),
                        "status": new_status,
                        "progress": 0
                    })
                    st.success(f"Added initiative: {new_name}")
                    st.rerun()
        
        # Display initiatives
        st.markdown("#### Current Initiatives")
        
        # Sample initiatives if none exist
        if not st.session_state.initiatives:
            sample_initiatives = [
                {"name": "ERP Upgrade", "phase": "Digital Transformation", "owner": "IT Director", "start": "2026-01-01", "end": "2026-03-31", "status": "In Progress", "progress": 45},
                {"name": "Assembly Automation", "phase": "Operational Excellence", "owner": "Ops Manager", "start": "2026-02-01", "end": "2026-06-30", "status": "Planning", "progress": 15},
                {"name": "Quality Enhancement", "phase": "Quality Improvement", "owner": "QA Manager", "start": "2026-01-15", "end": "2026-04-30", "status": "In Progress", "progress": 30},
            ]
            st.session_state.initiatives = sample_initiatives
        
        # Status filter
        status_filter = st.multiselect(
            "Filter by Status",
            ["Not Started", "Planning", "In Progress", "On Hold", "Completed"],
            default=["Planning", "In Progress"]
        )
        
        # Display initiatives
        filtered_initiatives = [i for i in st.session_state.initiatives if i.get('status') in status_filter]
        
        for i, initiative in enumerate(filtered_initiatives):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.markdown(f"**{initiative['name']}**")
                    st.markdown(f"*{initiative.get('phase', 'N/A')}* | Owner: {initiative.get('owner', 'TBD')}")
                
                with col2:
                    st.markdown(f"📅 {initiative.get('start', 'TBD')} → {initiative.get('end', 'TBD')}")
                
                with col3:
                    progress = initiative.get('progress', 0)
                    st.progress(progress / 100, text=f"{progress}% complete")
                
                with col4:
                    status = initiative.get('status', 'Unknown')
                    if status == "Completed":
                        st.markdown("✅ Done")
                    elif status == "In Progress":
                        st.markdown("🔄 Active")
                    elif status == "Planning":
                        st.markdown("📋 Plan")
                    elif status == "On Hold":
                        st.markdown("⏸️ Hold")
                    else:
                        st.markdown("⬜ New")
                
                st.markdown("---")
        
        # Summary metrics
        st.markdown("#### Portfolio Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(st.session_state.initiatives)
        in_progress = len([i for i in st.session_state.initiatives if i.get('status') == 'In Progress'])
        completed = len([i for i in st.session_state.initiatives if i.get('status') == 'Completed'])
        at_risk = len([i for i in st.session_state.initiatives if i.get('status') == 'On Hold'])
        
        with col1:
            st.metric("Total Initiatives", total)
        
        with col2:
            st.metric("In Progress", in_progress)
        
        with col3:
            st.metric("Completed", completed)
        
        with col4:
            st.metric("At Risk", at_risk)
    
    def _render_plan_history(self):
        """Render planning history"""
        st.markdown("### 📚 Planning History")
        
        if not st.session_state.planning_history:
            st.info("No strategic plans found. Create a new plan to get started.")
            return
        
        for i, record in enumerate(reversed(st.session_state.planning_history)):
            with st.expander(f"📋 {record.get('plan_name', 'Unnamed')} - {record.get('timestamp', '')[:10]}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Type:** {record.get('plan_type', 'N/A')}")
                    st.markdown(f"**Timeline:** {record.get('timeline', 'N/A')}")
                    st.markdown(f"**Budget:** {record.get('budget', 'N/A')}")
                
                with col2:
                    areas = record.get('priority_areas', [])
                    if areas:
                        st.markdown("**Priority Areas:**")
                        for area in areas[:3]:
                            st.markdown(f"- {area}")
                
                if st.button(f"View Full Plan", key=f"view_plan_{i}"):
                    st.session_state.current_plan = record
                    st.rerun()
