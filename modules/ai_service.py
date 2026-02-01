"""
AI Service Module - Google Gemini Integration
Handles all LLM interactions for the platform
"""

import os
import time
import google.generativeai as genai
from typing import Optional, List, Dict, Any
import json
import streamlit as st

class AIService:
    """Service class for AI-powered analysis and generation using Google Gemini"""
    
    def __init__(self):
        """Initialize the AI service with Gemini client"""
        self.model = None
        self.configured = False
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Gemini client with API key"""
        api_key = os.getenv("GOOGLE_API_KEY") or st.session_state.get("google_api_key")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                # Use gemini-pro - widely available model with free tier
                self.model = genai.GenerativeModel('gemini-pro')
                self.configured = True
            except Exception as e:
                self.configured = False
                print(f"Failed to initialize Gemini: {e}")
    
    def is_configured(self) -> bool:
        """Check if the AI service is properly configured"""
        return self.configured
    
    def _create_system_prompt(self, context: str) -> str:
        """Create a system prompt based on context"""
        base_prompt = """You are an expert AI Business Analyst and Decision Intelligence Assistant 
specialized in advanced manufacturing and innovation organizations. You provide:

1. Detailed, actionable business analysis
2. Data-driven recommendations
3. Strategic insights for manufacturing operations
4. Process optimization suggestions
5. Executive-level decision support

Always structure your responses clearly with sections, bullet points, and priorities.
Be specific, quantitative where possible, and focused on actionable outcomes."""
        
        return f"{base_prompt}\n\nContext: {context}"
    
    def _generate_response(self, prompt: str, system_context: str = "") -> str:
        """Generate a response using Gemini with retry logic for rate limits"""
        if not self.is_configured():
            raise Exception("AI service not configured. Please add your Google API key in Settings.")

        full_prompt = f"{system_context}\n\n{prompt}" if system_context else prompt

        max_retries = 5
        base_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                error_str = str(e)

                # Check for rate limit / quota errors (be specific to avoid false positives)
                error_lower = error_str.lower()
                is_quota_error = (
                    "429" in error_str or
                    "quota" in error_lower or
                    "rate limit" in error_lower or
                    "resource exhausted" in error_lower or
                    "too many requests" in error_lower
                )

                if is_quota_error:
                    if attempt < max_retries - 1:
                        # Exponential backoff: 5s, 10s, 20s, 40s
                        delay = base_delay * (2 ** attempt)
                        time.sleep(delay)
                        continue
                    else:
                        # Final attempt failed - show actual error for debugging
                        raise Exception(
                            f"API quota exceeded after {max_retries} retries. "
                            f"Original error: {error_str}. "
                            "Please wait a few minutes before trying again, or upgrade to a paid plan at "
                            "https://ai.google.dev/gemini-api/docs/billing"
                        )
                else:
                    # Non-rate-limit error, raise immediately with actual error
                    raise Exception(f"Generation failed: {error_str}")

        raise Exception("Generation failed after multiple retries")
    
    def analyze_requirements(self, requirements_text: str, project_context: str = "") -> Dict[str, Any]:
        """Analyze business requirements and generate structured insights"""
        if not self.is_configured():
            return {"error": "AI service not configured. Please add your Google API key in Settings."}
        
        system_prompt = self._create_system_prompt("Requirements Analysis for Manufacturing Projects")
        
        user_prompt = f"""Analyze the following business requirements for a manufacturing innovation project:

PROJECT CONTEXT:
{project_context}

REQUIREMENTS:
{requirements_text}

Provide a comprehensive analysis including:
1. **Executive Summary** - Brief overview of the requirements
2. **Functional Requirements** - List of key functional needs
3. **Non-Functional Requirements** - Performance, security, scalability needs
4. **Technical Considerations** - Technology and integration aspects
5. **Risk Assessment** - Potential risks and mitigation strategies
6. **Dependencies** - External and internal dependencies
7. **Priority Matrix** - Categorize requirements by priority (High/Medium/Low)
8. **Estimated Complexity** - Simple/Moderate/Complex for each major requirement
9. **Recommendations** - Suggested approach and next steps

Please provide a detailed, well-structured analysis."""

        try:
            response = self._generate_response(user_prompt, system_prompt)
            return {"success": True, "analysis": response}
        except Exception as e:
            return {"error": str(e)}
    
    def optimize_process(self, process_description: str, metrics: Dict = None) -> Dict[str, Any]:
        """Analyze and optimize manufacturing processes"""
        if not self.is_configured():
            return {"error": "AI service not configured. Please add your Google API key in Settings."}
        
        system_prompt = self._create_system_prompt("Process Optimization for Advanced Manufacturing")
        
        metrics_text = ""
        if metrics:
            metrics_text = f"\nCurrent Metrics:\n{json.dumps(metrics, indent=2)}"
        
        user_prompt = f"""Analyze the following manufacturing process and provide optimization recommendations:

PROCESS DESCRIPTION:
{process_description}
{metrics_text}

Provide comprehensive optimization analysis including:
1. **Current State Assessment** - Analysis of existing process
2. **Bottleneck Identification** - Key constraints and limitations
3. **Optimization Opportunities** - Specific areas for improvement
4. **Lean Manufacturing Recommendations** - Waste reduction strategies
5. **Automation Potential** - Areas suitable for automation
6. **Quality Improvement** - Suggestions for quality enhancement
7. **Cost-Benefit Analysis** - Expected ROI for recommendations
8. **Implementation Roadmap** - Phased approach for changes
9. **KPI Recommendations** - Metrics to track improvement
10. **Risk Mitigation** - Potential issues and solutions

Provide specific, actionable recommendations with estimated impact percentages where possible."""

        try:
            response = self._generate_response(user_prompt, system_prompt)
            return {"success": True, "optimization": response}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_strategic_plan(self, objectives: str, constraints: str, timeline: str) -> Dict[str, Any]:
        """Generate strategic plans based on objectives and constraints"""
        if not self.is_configured():
            return {"error": "AI service not configured. Please add your Google API key in Settings."}
        
        system_prompt = self._create_system_prompt("Strategic Planning for Manufacturing Innovation")
        
        user_prompt = f"""Create a comprehensive strategic plan for a manufacturing innovation organization:

STRATEGIC OBJECTIVES:
{objectives}

CONSTRAINTS & LIMITATIONS:
{constraints}

TIMELINE:
{timeline}

Generate a detailed strategic plan including:
1. **Vision & Mission Alignment** - How this plan aligns with organizational goals
2. **Strategic Pillars** - Key focus areas for the plan
3. **Initiative Portfolio** - Specific projects and initiatives
4. **Resource Requirements** - People, technology, and budget needs
5. **Milestone Roadmap** - Key deliverables and dates
6. **Success Metrics** - KPIs and targets
7. **Risk Management Plan** - Identified risks and mitigation
8. **Stakeholder Map** - Key stakeholders and engagement strategy
9. **Change Management** - Approach for organizational change
10. **Governance Structure** - Decision-making and oversight

Include specific timelines, resource estimates, and measurable targets."""

        try:
            response = self._generate_response(user_prompt, system_prompt)
            return {"success": True, "plan": response}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_report(self, report_type: str, data: Dict, parameters: Dict = None) -> Dict[str, Any]:
        """Generate various types of business reports"""
        if not self.is_configured():
            return {"error": "AI service not configured. Please add your Google API key in Settings."}
        
        system_prompt = self._create_system_prompt(f"Executive Report Generation - {report_type}")
        
        params_text = ""
        if parameters:
            params_text = f"\nReport Parameters:\n{json.dumps(parameters, indent=2)}"
        
        user_prompt = f"""Generate a comprehensive {report_type} report for manufacturing executive leadership:

DATA & CONTEXT:
{json.dumps(data, indent=2)}
{params_text}

Create an executive-level report including:
1. **Executive Summary** - Key findings and recommendations (2-3 paragraphs)
2. **Performance Highlights** - Top achievements and metrics
3. **Areas of Concern** - Issues requiring attention
4. **Trend Analysis** - Patterns and trajectories
5. **Comparative Analysis** - Benchmarking against targets/industry
6. **Root Cause Analysis** - For any underperformance
7. **Action Items** - Prioritized list of recommended actions
8. **Forward Outlook** - Predictions and expectations
9. **Resource Implications** - Budget and staffing considerations
10. **Appendix** - Supporting data and methodology

Use clear, executive-friendly language with specific numbers and actionable insights."""

        try:
            response = self._generate_response(user_prompt, system_prompt)
            return {"success": True, "report": response}
        except Exception as e:
            return {"error": str(e)}
    
    def decision_analysis(self, decision_context: str, options: List[str], criteria: List[str]) -> Dict[str, Any]:
        """Provide decision support analysis for executive decisions"""
        if not self.is_configured():
            return {"error": "AI service not configured. Please add your Google API key in Settings."}
        
        system_prompt = self._create_system_prompt("Executive Decision Support Analysis")
        
        options_text = "\n".join([f"- Option {i+1}: {opt}" for i, opt in enumerate(options)])
        criteria_text = "\n".join([f"- {crit}" for crit in criteria])
        
        user_prompt = f"""Provide comprehensive decision support analysis for the following executive decision:

DECISION CONTEXT:
{decision_context}

OPTIONS UNDER CONSIDERATION:
{options_text}

EVALUATION CRITERIA:
{criteria_text}

Provide detailed decision analysis including:
1. **Decision Framework** - Structured approach for this decision
2. **Options Analysis** - Detailed pros/cons for each option
3. **Criteria Scoring Matrix** - Score each option against criteria (1-10)
4. **Risk Assessment** - Risks associated with each option
5. **Financial Impact** - Cost-benefit analysis for each option
6. **Stakeholder Impact** - Effects on different stakeholder groups
7. **Implementation Complexity** - Effort required for each option
8. **Scenario Analysis** - Best/worst/likely case for each option
9. **Sensitivity Analysis** - Key factors that could change the recommendation
10. **Recommendation** - Recommended option with rationale
11. **Decision Triggers** - Conditions that would change the recommendation
12. **Next Steps** - Immediate actions if recommendation is accepted

Be objective, data-driven, and provide clear justification for scores and recommendations."""

        try:
            response = self._generate_response(user_prompt, system_prompt)
            return {"success": True, "analysis": response}
        except Exception as e:
            return {"error": str(e)}
    
    def chat(self, message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """General chat interface for the AI assistant"""
        if not self.is_configured():
            return {"error": "AI service not configured. Please add your Google API key in Settings."}
        
        system_prompt = """You are an expert AI Business Analyst Assistant for a manufacturing innovation organization.
You help with:
- Business requirements analysis
- Process optimization
- Strategic planning
- Report generation
- Executive decision support
- Manufacturing best practices
- Innovation management

Be helpful, specific, and action-oriented. Use examples from manufacturing and innovation contexts."""

        # Build conversation context
        context = ""
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                context += f"\n{role.upper()}: {content}"
        
        full_prompt = f"{context}\n\nUSER: {message}\n\nASSISTANT:"
        
        try:
            response = self._generate_response(full_prompt, system_prompt)
            return {
                "success": True, 
                "response": response,
                "usage": {
                    "model": "gemini-pro"
                }
            }
        except Exception as e:
            return {"error": str(e)}
