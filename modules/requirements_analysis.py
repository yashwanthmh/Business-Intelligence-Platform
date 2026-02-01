"""
Requirements Analysis Module
AI-powered business requirements analysis for manufacturing projects
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
from modules.ai_service import AIService

class RequirementsAnalyzer:
    """Business Requirements Analysis Module"""
    
    def __init__(self):
        self.ai_service = AIService()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for requirements module"""
        if 'requirements_history' not in st.session_state:
            st.session_state.requirements_history = []
        if 'current_analysis' not in st.session_state:
            st.session_state.current_analysis = None
    
    def render(self):
        """Render the Requirements Analysis interface"""
        st.markdown('<p class="main-header">📋 Requirements Analysis</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-powered analysis of business requirements for manufacturing projects</p>', unsafe_allow_html=True)
        
        # Check if AI is configured
        if not self.ai_service.is_configured():
            st.warning("Groq API key not configured. Please add your API key in Settings to enable AI analysis.")
        
        # Main tabs
        tab1, tab2, tab3 = st.tabs(["📝 New Analysis", "📚 Analysis History", "📊 Templates"])
        
        with tab1:
            self._render_new_analysis()
        
        with tab2:
            self._render_history()
        
        with tab3:
            self._render_templates()
    
    def _render_new_analysis(self):
        """Render the new analysis form"""
        st.markdown("### Create New Requirements Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Project Information
            st.markdown("#### 📁 Project Information")
            project_name = st.text_input("Project Name", placeholder="e.g., Smart Factory Phase 2")
            
            project_type = st.selectbox(
                "Project Type",
                [
                    "New Product Development",
                    "Process Improvement",
                    "Digital Transformation",
                    "Equipment Upgrade",
                    "Facility Expansion",
                    "Quality Enhancement",
                    "Automation Initiative",
                    "Other"
                ]
            )
            
            project_context = st.text_area(
                "Project Context",
                placeholder="Describe the background, objectives, and scope of the project...",
                height=100
            )
        
        with col2:
            st.markdown("#### 📊 Project Details")
            
            priority = st.select_slider(
                "Priority Level",
                options=["Low", "Medium", "High", "Critical"]
            )
            
            timeline = st.selectbox(
                "Expected Timeline",
                ["1-3 months", "3-6 months", "6-12 months", "12+ months"]
            )
            
            budget_range = st.selectbox(
                "Budget Range",
                ["< $100K", "$100K - $500K", "$500K - $1M", "$1M - $5M", "> $5M"]
            )
            
            stakeholders = st.multiselect(
                "Key Stakeholders",
                ["Executive Team", "Operations", "Engineering", "IT", "Quality", "Finance", "HR", "External Partners"]
            )
        
        st.markdown("---")
        
        # Requirements Input
        st.markdown("#### 📝 Requirements Input")
        
        input_method = st.radio(
            "Input Method",
            ["Text Input", "Upload Document", "Use Template"],
            horizontal=True
        )
        
        requirements_text = ""
        
        if input_method == "Text Input":
            requirements_text = st.text_area(
                "Enter Requirements",
                placeholder="""Enter your business requirements here. You can include:
- Functional requirements (what the system should do)
- Non-functional requirements (performance, security, etc.)
- Business rules and constraints
- Integration needs
- User stories or use cases

Be as detailed as possible for better AI analysis...""",
                height=300
            )
        
        elif input_method == "Upload Document":
            uploaded_file = st.file_uploader(
                "Upload Requirements Document",
                type=["txt", "md", "csv"],
                help="Upload a text file containing your requirements"
            )
            
            if uploaded_file:
                requirements_text = uploaded_file.read().decode("utf-8")
                st.text_area("Uploaded Content", requirements_text, height=200, disabled=True)
        
        elif input_method == "Use Template":
            template = st.selectbox(
                "Select Template",
                [
                    "Manufacturing Process Requirements",
                    "Equipment Specification Requirements",
                    "Software System Requirements",
                    "Quality Management Requirements",
                    "Safety & Compliance Requirements"
                ]
            )
            requirements_text = self._get_template(template)
            requirements_text = st.text_area("Edit Template", requirements_text, height=300)
        
        st.markdown("---")
        
        # Analysis Options
        st.markdown("#### ⚙️ Analysis Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_risks = st.checkbox("Include Risk Assessment", value=True)
            include_dependencies = st.checkbox("Include Dependency Analysis", value=True)
        
        with col2:
            include_estimates = st.checkbox("Include Complexity Estimates", value=True)
            include_priorities = st.checkbox("Generate Priority Matrix", value=True)
        
        with col3:
            include_recommendations = st.checkbox("Include Recommendations", value=True)
            generate_user_stories = st.checkbox("Generate User Stories", value=False)
        
        # Analyze Button
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🔍 Analyze Requirements", type="primary", use_container_width=True):
                if not requirements_text.strip():
                    st.error("Please enter requirements to analyze.")
                elif not self.ai_service.is_configured():
                    st.error("Please configure your Groq API key in Settings first.")
                else:
                    self._run_analysis(
                        project_name=project_name,
                        project_type=project_type,
                        project_context=project_context,
                        requirements_text=requirements_text,
                        priority=priority,
                        timeline=timeline,
                        budget_range=budget_range,
                        stakeholders=stakeholders
                    )
        
        # Display current analysis results
        if st.session_state.current_analysis:
            self._display_analysis_results(st.session_state.current_analysis)
    
    def _run_analysis(self, **kwargs):
        """Run the AI analysis on requirements"""
        with st.spinner("🤖 AI is analyzing your requirements..."):
            # Build context
            context = f"""
Project: {kwargs.get('project_name', 'Unnamed Project')}
Type: {kwargs.get('project_type', 'Not specified')}
Context: {kwargs.get('project_context', 'Not provided')}
Priority: {kwargs.get('priority', 'Medium')}
Timeline: {kwargs.get('timeline', 'Not specified')}
Budget: {kwargs.get('budget_range', 'Not specified')}
Stakeholders: {', '.join(kwargs.get('stakeholders', []))}
"""
            
            result = self.ai_service.analyze_requirements(
                requirements_text=kwargs.get('requirements_text', ''),
                project_context=context
            )
            
            if 'error' in result:
                st.error(f"❌ {result['error']}")
            else:
                # Save to session state
                analysis_record = {
                    'timestamp': datetime.now().isoformat(),
                    'project_name': kwargs.get('project_name', 'Unnamed'),
                    'project_type': kwargs.get('project_type', ''),
                    'analysis': result.get('analysis', ''),
                    'input': kwargs
                }
                
                st.session_state.current_analysis = analysis_record
                st.session_state.requirements_history.append(analysis_record)
                st.success("✅ Analysis complete!")
    
    def _display_analysis_results(self, analysis_record):
        """Display the analysis results"""
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        st.markdown(f"**Project:** {analysis_record.get('project_name', 'Unnamed')}")
        st.markdown(f"**Analyzed:** {analysis_record.get('timestamp', '')[:19]}")
        
        analysis = analysis_record.get('analysis', '')
        
        if isinstance(analysis, dict):
            # Structured JSON response
            for key, value in analysis.items():
                with st.expander(f"📌 {key.replace('_', ' ').title()}", expanded=True):
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                st.json(item)
                            else:
                                st.markdown(f"- {item}")
                    elif isinstance(value, dict):
                        st.json(value)
                    else:
                        st.markdown(value)
        else:
            # Plain text response
            st.markdown(analysis)
        
        # Export options
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Export as JSON"):
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(analysis_record, indent=2),
                    file_name=f"requirements_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📄 Export as Text"):
                text_content = f"Requirements Analysis Report\n{'='*50}\n\n"
                text_content += f"Project: {analysis_record.get('project_name', '')}\n"
                text_content += f"Date: {analysis_record.get('timestamp', '')}\n\n"
                text_content += str(analysis)
                
                st.download_button(
                    label="Download Text",
                    data=text_content,
                    file_name=f"requirements_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col3:
            if st.button("🔄 New Analysis"):
                st.session_state.current_analysis = None
                st.rerun()
    
    def _render_history(self):
        """Render the analysis history"""
        st.markdown("### 📚 Previous Analyses")
        
        if not st.session_state.requirements_history:
            st.info("No previous analyses found. Create a new analysis to get started.")
            return
        
        for i, record in enumerate(reversed(st.session_state.requirements_history)):
            with st.expander(f"📋 {record.get('project_name', 'Unnamed')} - {record.get('timestamp', '')[:10]}"):
                st.markdown(f"**Type:** {record.get('project_type', 'N/A')}")
                
                if st.button(f"View Full Analysis", key=f"view_{i}"):
                    st.session_state.current_analysis = record
                    st.rerun()
    
    def _render_templates(self):
        """Render requirements templates"""
        st.markdown("### 📊 Requirements Templates")
        
        templates = {
            "Manufacturing Process Requirements": {
                "description": "Template for documenting manufacturing process requirements",
                "sections": ["Process Overview", "Input/Output Specs", "Quality Standards", "Cycle Time", "Equipment Needs"]
            },
            "Equipment Specification Requirements": {
                "description": "Template for equipment purchase or upgrade requirements",
                "sections": ["Technical Specs", "Performance Criteria", "Safety Requirements", "Integration Needs", "Maintenance"]
            },
            "Software System Requirements": {
                "description": "Template for manufacturing software/MES requirements",
                "sections": ["Functional Requirements", "User Roles", "Data Requirements", "Integration", "Security"]
            },
            "Quality Management Requirements": {
                "description": "Template for quality system requirements",
                "sections": ["Quality Standards", "Inspection Points", "Documentation", "Traceability", "Compliance"]
            },
            "Safety & Compliance Requirements": {
                "description": "Template for safety and regulatory requirements",
                "sections": ["Regulatory Standards", "Safety Protocols", "Training Needs", "Documentation", "Audit Requirements"]
            }
        }
        
        for name, info in templates.items():
            with st.expander(f"📄 {name}"):
                st.markdown(f"*{info['description']}*")
                st.markdown("**Sections:**")
                for section in info['sections']:
                    st.markdown(f"- {section}")
                
                if st.button(f"Use This Template", key=f"template_{name}"):
                    st.session_state.selected_template = name
                    st.info(f"Template '{name}' selected. Go to 'New Analysis' tab and select 'Use Template'.")
    
    def _get_template(self, template_name: str) -> str:
        """Get template content by name"""
        templates = {
            "Manufacturing Process Requirements": """# Manufacturing Process Requirements

## 1. Process Overview
- Process Name: [Enter process name]
- Process Purpose: [Describe the main purpose]
- Current State: [Describe current process if applicable]

## 2. Input/Output Specifications
### Inputs
- Raw Materials: [List materials]
- Components: [List components]
- Data/Information: [List data inputs]

### Outputs
- Products: [List products]
- Quality Metrics: [List expected quality metrics]
- Documentation: [List required documentation]

## 3. Quality Standards
- Quality Level Required: [Specify quality requirements]
- Acceptable Defect Rate: [Specify tolerance]
- Inspection Points: [List inspection requirements]

## 4. Cycle Time Requirements
- Target Cycle Time: [Specify time]
- Throughput Requirements: [Specify volume]
- Efficiency Targets: [Specify OEE or similar]

## 5. Equipment & Resource Needs
- Equipment Required: [List equipment]
- Tooling Requirements: [List tools]
- Personnel/Skills Needed: [List skills]

## 6. Additional Requirements
[Add any additional requirements]
""",
            "Equipment Specification Requirements": """# Equipment Specification Requirements

## 1. General Information
- Equipment Type: [Enter type]
- Intended Use: [Describe use case]
- Location: [Specify installation location]

## 2. Technical Specifications
- Capacity: [Specify capacity]
- Dimensions: [Specify size requirements]
- Power Requirements: [Specify electrical needs]
- Environmental Conditions: [Specify operating environment]

## 3. Performance Criteria
- Speed/Throughput: [Specify performance]
- Accuracy/Precision: [Specify tolerances]
- Reliability: [Specify uptime requirements]

## 4. Safety Requirements
- Safety Standards: [List applicable standards]
- Guards/Interlocks: [Specify safety features]
- Emergency Stop: [Specify E-stop requirements]

## 5. Integration Requirements
- Connectivity: [Specify communication protocols]
- Data Output: [Specify data requirements]
- Existing System Integration: [List integration needs]

## 6. Maintenance & Support
- Maintenance Schedule: [Specify requirements]
- Spare Parts: [List critical spares]
- Training: [Specify training needs]
- Warranty: [Specify warranty requirements]
""",
            "Software System Requirements": """# Software System Requirements

## 1. System Overview
- System Name: [Enter name]
- Purpose: [Describe purpose]
- Users: [Describe user base]

## 2. Functional Requirements
### Core Functions
- [Function 1]: [Description]
- [Function 2]: [Description]
- [Function 3]: [Description]

### User Management
- Authentication: [Specify requirements]
- Authorization/Roles: [Specify roles]

## 3. Data Requirements
- Data Inputs: [List inputs]
- Data Outputs: [List outputs]
- Storage Requirements: [Specify storage]
- Retention: [Specify retention policy]

## 4. Integration Requirements
- ERP Integration: [Specify needs]
- Equipment Integration: [Specify needs]
- External Systems: [List systems]

## 5. Performance Requirements
- Response Time: [Specify requirements]
- Concurrent Users: [Specify capacity]
- Availability: [Specify uptime]

## 6. Security Requirements
- Data Protection: [Specify requirements]
- Access Control: [Specify requirements]
- Audit Trail: [Specify requirements]
""",
            "Quality Management Requirements": """# Quality Management Requirements

## 1. Quality Standards
- Applicable Standards: [List ISO, industry standards]
- Customer Requirements: [List customer specs]
- Internal Standards: [List internal specs]

## 2. Inspection Requirements
### Incoming Inspection
- [Material/Component]: [Inspection criteria]

### In-Process Inspection
- [Process Point]: [Inspection criteria]

### Final Inspection
- [Product]: [Inspection criteria]

## 3. Documentation Requirements
- Quality Records: [List required records]
- Certificates: [List required certificates]
- Traceability: [Specify traceability needs]

## 4. Non-Conformance Management
- Detection: [Specify detection methods]
- Containment: [Specify containment procedures]
- Corrective Action: [Specify CA requirements]

## 5. Continuous Improvement
- Metrics: [List quality metrics]
- Review Frequency: [Specify review schedule]
- Improvement Targets: [Specify targets]
""",
            "Safety & Compliance Requirements": """# Safety & Compliance Requirements

## 1. Regulatory Standards
- Applicable Regulations: [List regulations]
- Industry Standards: [List standards]
- Certification Requirements: [List certifications]

## 2. Safety Protocols
- PPE Requirements: [List PPE needs]
- Safety Procedures: [List procedures]
- Emergency Procedures: [List emergency protocols]

## 3. Training Requirements
- Initial Training: [Specify requirements]
- Refresher Training: [Specify frequency]
- Certification: [Specify certifications needed]

## 4. Documentation
- Safety Records: [List required records]
- Incident Reports: [Specify reporting requirements]
- Audit Documentation: [Specify audit needs]

## 5. Compliance Monitoring
- Inspection Schedule: [Specify schedule]
- Audit Frequency: [Specify frequency]
- Reporting Requirements: [Specify reports]
"""
        }
        
        return templates.get(template_name, "# Custom Requirements\n\n[Enter your requirements here]")
