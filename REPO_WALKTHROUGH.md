# Business-Intelligence-Platform: Complete Repository Walkthrough

A line-by-line explanation of every file in the **Manufacturing Intelligence Platform (MIP)** codebase.

---

## Table of Contents

1. [Overview & Architecture](#1-overview--architecture)
2. [app.py — Main Entry Point](#2-apppy--main-entry-point)
3. [modules/\_\_init\_\_.py — Package Init](#3-modules__init__py--package-init)
4. [modules/rate_limiter.py — Rate Limiting](#4-modulesrate_limiterpy--rate-limiting)
5. [modules/ai_service.py — AI Integration](#5-modulesai_servicepy--ai-integration)
6. [modules/requirements_analysis.py](#6-modulesrequirements_analysispy)
7. [modules/process_optimization.py](#7-modulesprocess_optimizationpy)
8. [modules/strategic_planning.py](#8-modulesstrategic_planningpy)
9. [modules/reports_analytics.py](#9-modulesreports_analyticspy)
10. [modules/decision_support.py](#10-modulesdecision_supportpy)
11. [modules/ai_assistant.py](#11-modulesai_assistantpy)
12. [modules/settings.py](#12-modulessettingspy)
13. [requirements.txt](#13-requirementstxt)
14. [Dockerfile & startup.sh](#14-dockerfile--startupsh)
15. [infra/main.bicep & main.bicepparam](#15-inframainbicep--mainbicepparam)
16. [.github/workflows/ — CI/CD](#16-githubworkflows--cicd)
17. [Key Architectural Observations](#17-key-architectural-observations)

---

## 1. Overview & Architecture

### What is this project?

MIP is a **Streamlit web application** that provides AI-powered business analysis tools for manufacturing organizations. It connects to the **Groq** API (running **Llama 3.1 8B Instant**) to generate analysis, reports, and recommendations.

### High-Level Architecture

```
User's Browser
     |
     v
+-------------------+
|     Streamlit      |  <-- app.py (router + dashboard)
|  (Python / Web UI) |
+-------------------+
     |
     v
+-------------------+     +------------------+
|  Feature Modules   | --> |   AIService      |
|  (7 modules in     |     | (modules/        |
|   modules/)        |     |  ai_service.py)  |
+-------------------+     +------------------+
                                  |
                                  v
                          +------------------+
                          |   RateLimiter    |
                          | (Singleton)      |
                          +------------------+
                                  |
                                  v
                          +------------------+
                          |  Groq Cloud API  |
                          | (Llama 3.1 8B)   |
                          +------------------+
```

### Deployment Stack

```
GitHub Actions (CI/CD)
     |
     v
Azure Container Registry  <-- Docker image built on push to main
     |
     v
Azure App Service (Linux)  <-- Runs the Streamlit container on port 8000
     |
Azure Bicep (IaC)          <-- Defines all Azure resources
```

### File Tree

```
Business-Intelligence-Platform/
|-- app.py                              # Main entry point & router
|-- requirements.txt                    # Python dependencies
|-- Dockerfile                          # Container build instructions
|-- startup.sh                          # Container entrypoint script
|-- modules/
|   |-- __init__.py                     # Package exports
|   |-- ai_service.py                   # Groq LLM integration (core)
|   |-- rate_limiter.py                 # Token-bucket rate limiter (singleton)
|   |-- requirements_analysis.py        # Requirements analysis UI
|   |-- process_optimization.py         # Process optimization UI
|   |-- strategic_planning.py           # Strategic planning UI
|   |-- reports_analytics.py            # Report generation UI
|   |-- decision_support.py             # Decision support UI
|   |-- ai_assistant.py                 # Chat interface UI
|   |-- settings.py                     # App settings UI
|-- infra/
|   |-- main.bicep                      # Azure infrastructure as code
|   |-- main.bicepparam                 # Bicep parameter file
|-- .github/workflows/
|   |-- azure-deploy.yml                # Build & deploy on push to main
|   |-- infra-deploy.yml                # Manually deploy Azure infrastructure
```

---

## 2. app.py — Main Entry Point

**Purpose:** The single-page Streamlit application. It configures the page, renders the sidebar navigation, defines the dashboard, and routes to feature modules.

### Lines 1-6: Module Docstring

```python
"""
AI-Powered Business Analysis and Decision Intelligence Platform
For Advanced Manufacturing Innovation Organizations
Main Application Entry Point
"""
```

A standard Python docstring describing the project.

### Lines 7-9: Imports

```python
import streamlit as st
from datetime import datetime
```

- `streamlit` — The web framework. Every `st.*` call renders a UI widget.
- `datetime` — Used to display the current date in the sidebar.

### Lines 11-17: Page Configuration

```python
st.set_page_config(
    page_title="Manufacturing Intelligence Platform",
    page_icon="...",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

This **must be the first Streamlit command** in the script. It sets the browser tab title, favicon, uses the full-width layout, and opens the sidebar by default.

### Lines 19-69: Custom CSS

```python
st.markdown("""<style>...</style>""", unsafe_allow_html=True)
```

Injects custom CSS into the page for:
- `.main-header` — Large navy-blue page titles (font-size 2.5rem)
- `.sub-header` — Gray subtitle text
- `.metric-card` — Purple gradient cards with box shadow
- `.module-card` — White bordered cards with hover animation
- `.status-active` / `.status-pending` — Green/amber status badges
- `.stButton>button` — Purple gradient buttons with rounded corners

`unsafe_allow_html=True` is required for Streamlit to render raw HTML/CSS.

### Lines 71-75: Session State Initialization

```python
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True  # Set to True for demo
if 'current_module' not in st.session_state:
    st.session_state.current_module = 'dashboard'
```

`st.session_state` is Streamlit's per-session key-value store that persists across reruns. Here:
- `authenticated` is hardcoded to `True` (no real auth implemented).
- `current_module` tracks which page the user is viewing (defaults to `'dashboard'`).

### Lines 77-106: Sidebar Navigation

The sidebar contains:
1. A factory icon loaded from an external URL
2. The app name "MIP" with subtitle
3. Navigation buttons — each button sets `st.session_state.current_module` to route to the corresponding page
4. System status indicators (hardcoded "Online" — no real health checks)
5. Current date

### Lines 108-190: Dashboard Renderer

`render_dashboard()` renders the executive dashboard with:
- **4 metric cards** (Active Projects, Process Efficiency, Requirements Analyzed, AI Recommendations) — all hardcoded sample data
- **Recent Activity table** — 5 hardcoded activity records in a 4-column layout
- **Quick Actions** — Buttons that navigate to other modules via `st.session_state.current_module` then `st.rerun()`
- **Weekly Goals** progress bar at 75%

### Lines 192-232: Module Renderers

Seven thin wrapper functions that:
1. **Lazy-import** the module class (imports happen only when the page is visited)
2. Instantiate the class
3. Call `.render()` to draw the UI

This pattern keeps startup fast by deferring imports until needed.

### Lines 234-248: Module Router

```python
module_renderers = {
    'dashboard': render_dashboard,
    'requirements': render_requirements,
    ...
}
current_renderer = module_renderers.get(st.session_state.current_module, render_dashboard)
current_renderer()
```

A dictionary maps module keys to render functions. Falls back to dashboard if the key is not found.

### Lines 250-259: Footer

A centered footer with copyright text rendered as raw HTML.

---

## 3. modules/\_\_init\_\_.py — Package Init

**Purpose:** Makes `modules/` a Python package and re-exports all public classes.

- Relative imports (`.ai_service`, etc.) import from sibling files.
- `__all__` defines the public API for `from modules import *`.
- Note: `app.py` does not use these re-exports; it imports directly from each module file.

---

## 4. modules/rate_limiter.py — Rate Limiting

**Purpose:** A thread-safe, singleton token-bucket rate limiter that prevents the app from exceeding the Groq free-tier limit of 30 requests per minute.

### Imports

- `time` — For `time.time()` timestamps and `time.sleep()` delays.
- `threading` — For `Lock` to ensure thread safety.
- `deque` — A double-ended queue used as a sliding window of request timestamps.

### Singleton Pattern (Double-Checked Locking)

```python
class RateLimiter:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
```

**Why a singleton?** Streamlit may create multiple instances of module classes on each rerun, but there must be only ONE rate limiter tracking requests globally.

The double-checked locking pattern:
1. **Outer check** — Fast path, avoids locking when instance already exists.
2. **Lock** — Only one thread can enter the critical section.
3. **Inner check** — Guards against a race where two threads both passed the outer check.
4. `_initialized = False` flag ensures `__init__` only runs setup once.

### Initialization

- Sets the limit to **25 RPM** (5 below the actual 30 RPM limit for safety buffer).
- `request_times` is a deque storing Unix timestamps of recent requests.
- A separate `self.lock` protects the deque from concurrent access.

### Sliding Window Cleanup (`_clean_old_requests`)

Removes all timestamps older than 60 seconds from the left side of the deque. Since timestamps are appended in order, `popleft()` is O(1).

### Wait Time Calculation (`get_wait_time`)

Under the lock:
1. Clean expired entries.
2. If fewer than 25 requests in the window, return 0 (proceed immediately).
3. Otherwise, calculate how long until the oldest request expires.

### Acquire a Slot (`acquire`)

The main method called before every API request:
1. Check if a slot is available.
2. If yes, **double-check under the lock** and record the request timestamp. Return `True`.
3. If no slot, check timeout. Return `False` if exceeded.
4. Sleep for up to 1 second, then retry. Small sleep chunks keep the loop responsive.

### Usage Stats & Global Instance

- `get_current_usage()` returns a snapshot of current rate limit state (used by Settings page).
- `rate_limiter = RateLimiter()` is a module-level singleton. Importing it always gives the same object.

---

## 5. modules/ai_service.py — AI Integration

**Purpose:** The central AI service layer. Every feature module delegates LLM calls through this class. It wraps the Groq Python SDK, manages prompt construction, and handles retries with exponential backoff.

### Initialization

```python
class AIService:
    def __init__(self):
        self.client = None
        self.configured = False
        self.model = "llama-3.1-8b-instant"
        self._initialize_client()
```

- The API key can come from either an **environment variable** (`GROQ_API_KEY` for production/Docker) or **session state** (set by the user in the Settings UI).
- The model is hardcoded to `llama-3.1-8b-instant` — Groq's fastest free-tier model.
- If no key is found, `self.configured` stays `False` and all methods return error messages.

### System Prompt Builder (`_create_system_prompt`)

Every API call gets a system prompt instructing the LLM to act as a manufacturing business analyst. A `context` parameter specializes each call.

### Core Generation Method with Retry Logic (`_generate_response`)

The flow for every LLM call:
1. **Check configuration** — Fail fast if no API key.
2. **Build messages** — OpenAI-compatible format with optional system message.
3. **Rate limiter gate** — `rate_limiter.acquire(timeout=120)` blocks up to 2 minutes.
4. **API call** — `max_tokens=4096`, `temperature=0.7`.
5. **Error handling** — Rate limit errors (HTTP 429) retry with exponential backoff: `delay = 2 * 2^attempt + 5` seconds (7s, 9s, 13s, 21s, 37s). Non-rate errors raised immediately.

### Domain-Specific Methods

Each method follows the same pattern: check config, build specialized prompt, call `_generate_response()`, return result dict.

| Method | Purpose | Prompt Asks For |
|--------|---------|-----------------|
| `analyze_requirements()` | Requirements analysis | Executive summary, functional/non-functional reqs, risks, priority matrix |
| `optimize_process()` | Process optimization | Current state, bottlenecks, lean recommendations, automation potential, ROI |
| `generate_strategic_plan()` | Strategic planning | Vision alignment, strategic pillars, milestones, governance |
| `generate_report()` | Executive reports | Executive summary, performance highlights, trend analysis, action items |
| `decision_analysis()` | Decision support | Options analysis, criteria scoring, scenario analysis, recommendation |
| `chat()` | General chat | Free-form conversation with last 10 messages as context |

### Chat Method

Unique because it:
- Keeps a rolling window of the last 10 messages for context
- Formats conversation as `ROLE: message` pairs
- Returns rate limit stats alongside the response

---

## 6. modules/requirements_analysis.py

**Purpose:** AI-powered business requirements analysis UI with form input, file upload, templates, analysis history, and export.

### Class: RequirementsAnalyzer

**Structure:** 3 tabs — New Analysis, History, Templates.

### New Analysis Form

Collects:
- **Project Information** — Name, type (8 categories), context
- **Project Details** — Priority (Low to Critical), timeline, budget range, stakeholders
- **Requirements Input** — Three methods:
  - **Text Input** — Free-form text area
  - **Upload Document** — `.txt`, `.md`, `.csv` files decoded as UTF-8
  - **Use Template** — 5 pre-built manufacturing templates
- **Analysis Options** — 6 checkboxes (risks, dependencies, estimates, priorities, recommendations, user stories)

### Analysis Execution

1. Shows spinner, builds context from form fields.
2. Calls `self.ai_service.analyze_requirements()`.
3. Saves to session state on success.

### Results Display

- Renders AI output as markdown (plain text) or expandable sections (structured JSON).
- Export buttons: JSON download, text download, "New Analysis" reset.

### Templates

Five manufacturing-specific templates with placeholder fields:
1. Manufacturing Process Requirements
2. Equipment Specification Requirements
3. Software System Requirements
4. Quality Management Requirements
5. Safety & Compliance Requirements

---

## 7. modules/process_optimization.py

**Purpose:** Manufacturing process analysis with metrics input, interactive charts, benchmarks, and AI optimization recommendations.

### Class: ProcessOptimizer

**Structure:** 4 tabs — Process Analysis, Metrics Dashboard, Optimization History, Benchmarks.

### Process Analysis Form

Collects:
- **Process info** — Name, type (Assembly, Machining, Fabrication, etc.), description
- **Current metrics** — Cycle time, OEE %, defect rate %, daily throughput, downtime hrs/week, changeover time, labor cost/unit
- **Constraints** — Free text
- **Optimization goals** — Multiselect from 10 options
- **Analysis options** — 6 checkboxes (Lean, Six Sigma, Automation, ROI, Implementation, KPIs)

Calls `self.ai_service.optimize_process()`.

### Results Display

- 4 metric cards (OEE, Defect Rate, Cycle Time, Throughput) with delta indicators.
- AI recommendations rendered as markdown.
- Export buttons for JSON and text.

### Metrics Dashboard

Uses **sample data** (not connected to real sources):
- **OEE Trend** — 30-day Plotly line chart with 85% target line
- **Defect Rate Pie Chart** — By category (Assembly, Material, Machine, Operator, Design)
- **Production Comparison** — Bar chart comparing 5 processes
- **Detailed Metrics Table** — `st.dataframe()` with per-process stats

Uses `numpy` for random data generation.

### Benchmarks

- Reference table: "World Class" vs "Industry Average" vs "Your Target"
- Three Plotly gauge charts for OEE components: Availability (88%), Performance (92%), Quality (97.5%)

---

## 8. modules/strategic_planning.py

**Purpose:** AI-assisted strategic planning with roadmap visualization, initiative tracking, and plan generation.

### Class: StrategicPlanner

**Structure:** 4 tabs — Create Plan, Roadmap View, Initiative Tracker, Plan History.

### Plan Creation Form

Collects: plan name, type (9 categories), objectives, timeline, budget, priority areas, stakeholders, constraints, resources, and 6 option checkboxes.

Calls `self.ai_service.generate_strategic_plan()`.

### Roadmap View

A **Gantt chart** via `plotly.express.timeline()` showing 8 sample initiatives across 2026, color-coded by strategic phase. Below: quarterly milestone checklists.

### Initiative Tracker

Interactive management tool:
- **Add Initiative** form (name, phase, owner, dates, status)
- **Status Filter** multiselect
- **Initiative Cards** with progress bars and status icons
- **Portfolio Summary** — 4 metrics (Total, In Progress, Completed, At Risk)
- Pre-populated with 3 sample initiatives

### Plan History

Expandable list of generated plans with "View Full Plan" buttons.

---

## 9. modules/reports_analytics.py

**Purpose:** Executive report generation with analytics dashboards, report library, and templates.

### Class: ReportsAnalytics

**Structure:** 4 tabs — Generate Report, Analytics Dashboard, Report Library, Templates.

### Report Generation

Collects report name, type (8 categories), data (manual entry or sample), period, audience, section checkboxes, context.

Calls `self.ai_service.generate_report()`.

### Analytics Dashboard

Sample-data visualizations:
- **4 KPI metrics** — Revenue ($5.25M), Production (26,500), OEE (84.2%), Quality (98.1%)
- **Revenue Trend** — 6-month line chart
- **Production by Line** — Bar chart for 4 lines
- **Quality by Category** — Pie chart
- **OEE Components** — Bar chart with target line

### Report Library & Templates

- Library: expandable list of generated reports
- Templates: 5 report templates (Executive Summary, Operational, Financial, Quality, Project Status)

---

## 10. modules/decision_support.py

**Purpose:** AI-powered executive decision analysis with a decision matrix tool and history tracking.

### Class: DecisionSupport

**Structure:** 3 tabs — New Decision Analysis, Decision Matrix, Decision History.

### Decision Analysis Form

Collects:
- Title, type (9 categories), context
- **Parameters** — Urgency, Business Impact, Reversibility (sliders), budget impact
- **Options** — 2 to 6 text areas
- **Criteria** — Multiselect from 10 defaults + custom input

Calls `self.ai_service.decision_analysis()`.

### Decision Matrix Tool

A fully interactive weighted scoring matrix:
1. Define 2-5 options and 2-8 criteria
2. Assign weights (should total 100)
3. Score each option per criterion (1-10 sliders)
4. Calculate weighted scores: `sum(score * weight / 100)`
5. Display sorted dataframe + bar chart + winner

This is the **only module that works without AI** — pure local computation.

---

## 11. modules/ai_assistant.py

**Purpose:** Conversational chat interface for free-form AI interaction.

### Class: AIAssistant

**Session State:** `chat_history` (display) and `conversation_context` (AI context).

### Render Flow

1. **Sidebar** — "Clear Chat" button + 6 quick prompt buttons
2. **Welcome banner** — Purple gradient listing capabilities (shown when empty)
3. **Message display** — User/assistant bubbles via `st.chat_message()`
4. **Input** — `st.chat_input()` for free-form text

### Message Processing

1. Append user message to both histories
2. Call `self.ai_service.chat()` with last 10 messages
3. Append response, call `st.rerun()` to refresh

---

## 12. modules/settings.py

**Purpose:** Application configuration UI for API keys, organization details, appearance, and data management.

### Class: Settings

**Structure:** 4 tabs — API Configuration, Organization, Appearance, Data.

### API Configuration

- Instructions for getting a free Groq API key
- Masked key display (last 8 chars visible)
- Password input field, Save/Clear buttons
- **Test Connection** — Sends test message to Groq
- **Rate Limit Status** — 3 metrics from `rate_limiter.get_current_usage()`
- Model info (Llama 3.1 8B Instant)

### Organization Settings

Form for org name, industry, company size, contact info. Session-state only (not persisted).

### Appearance Settings

Theme selector and checkboxes — **non-functional placeholders** (stored but not applied).

### Data Settings

- Retention/export format selectors
- **Clear All History** — Resets all session state (requires confirmation)
- System info: version 1.0.0, Python 3.11+, Streamlit 1.30+

---

## 13. requirements.txt

```
streamlit>=1.30.0        # Web framework
groq>=0.4.0              # Groq API client (for Llama 3.1)
pandas>=2.0.0            # Data manipulation & DataFrames
plotly>=5.18.0           # Interactive charts & visualizations
numpy>=1.24.0            # Numerical computing (used for sample data)
python-dotenv>=1.0.0     # Load .env files (for local dev API keys)
cffi>=2.0.0              # C Foreign Function Interface (dependency)
cryptography>=42.0.0     # Cryptographic operations (dependency)
```

- **Core:** `streamlit`, `groq`, `pandas`, `plotly`, `numpy`
- **Support:** `python-dotenv` for `.env` loading (though `load_dotenv()` is never called in code)
- **System:** `cffi` and `cryptography` are likely transitive dependencies pinned explicitly

---

## 14. Dockerfile & startup.sh

### Dockerfile

```dockerfile
FROM python:3.11-slim-bookworm
```

Slim Debian Bookworm with Python 3.11 for a small image.

**Environment variables:**
- `PYTHONDONTWRITEBYTECODE=1` — No `.pyc` files (smaller image)
- `PYTHONUNBUFFERED=1` — Flush logs immediately
- `STREAMLIT_SERVER_PORT=8000` / `STREAMLIT_SERVER_ADDRESS=0.0.0.0`

**Build steps:**
1. Install `curl` (needed by HEALTHCHECK)
2. Copy and install Python deps first (Docker layer caching)
3. Copy application code

**Health check:** Hits `/_stcore/health` every 30s. Unhealthy after 3 failures.

**Entry point:** `startup.sh`

### startup.sh

```bash
#!/bin/bash
set -e
streamlit run app.py \
    --server.port=${STREAMLIT_SERVER_PORT:-8000} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false
```

- `--server.headless=true` — No browser prompt in container
- `--server.enableCORS=false` — CORS handled by Azure/proxy
- `--server.enableXsrfProtection=false` — Simplifies proxy deployment
- `--browser.gatherUsageStats=false` — Opt out of telemetry

---

## 15. infra/main.bicep & main.bicepparam

### main.bicep — Azure Infrastructure as Code

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `appName` | `mfg-intel-platform` | Base name for resources |
| `location` | Resource group location | Azure region |
| `appServicePlanSku` | `B1` | Compute tier |
| `dockerImage` | `mfg-intel-platform` | Docker image name |
| `dockerImageTag` | `latest` | Image tag |
| `groqApiKey` | `''` | API key (`@secure()`) |

**Variables:** `uniqueString(resourceGroup().id)` generates a deterministic 13-char hash for globally unique names.

**Resources:**
1. **Azure Container Registry (ACR)** — Basic SKU, admin enabled
2. **App Service Plan** — Linux, selected SKU, `reserved: true`
3. **Web App** — Linux container with managed identity, HTTPS only, Always On, health check at `/_stcore/health`, Docker registry creds, `GROQ_API_KEY` env var

**Outputs:** Web app URL, ACR login server, ACR name.

### main.bicepparam

References `main.bicep` with default parameter values. `groqApiKey` left empty — set via CLI or Azure Portal.

---

## 16. .github/workflows/ — CI/CD

### azure-deploy.yml — Build & Deploy

**Trigger:** Push to `main` or manual dispatch.

**Steps:**
1. Checkout code
2. Azure login via OIDC
3. ACR login
4. Build Docker image with two tags: `<sha>` (immutable) and `latest` (rolling)
5. Push both tags
6. Deploy to Azure Web App with SHA-tagged image
7. Azure logout

**Secrets:** `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `ACR_NAME`, `AZURE_WEBAPP_NAME`

### infra-deploy.yml — Infrastructure Deployment

**Trigger:** Manual dispatch only.

**Inputs:** Resource group, region, SKU.

**Steps:**
1. Checkout, Azure login
2. Deploy Bicep: `az deployment group create --template-file infra/main.bicep`
3. Show outputs
4. Azure logout

Run **once** to provision infrastructure. `azure-deploy.yml` runs on every push for app updates.

---

## 17. Key Architectural Observations

### Design Patterns

| Pattern | Where | Why |
|---------|-------|-----|
| **Singleton** | `RateLimiter` | One tracker across all Streamlit reruns |
| **Service Layer** | `AIService` | Consistent error handling for all LLM calls |
| **Lazy Loading** | `app.py` renders | Imports deferred until module is visited |
| **Session State as DB** | Every module | All data in `st.session_state` (lost on restart) |
| **Strategy Pattern** | Module router | Dict maps keys to render functions |

### Strengths

1. **Clean module separation** — Each domain is its own file/class
2. **Robust rate limiting** — Thread-safe singleton with token bucket
3. **Exponential backoff** — Retries from 7s to 37s for transient failures
4. **Complete IaC** — Azure infra fully codified in Bicep with CI/CD
5. **Docker health checks** — Container health via Streamlit endpoint
6. **Dual image tagging** — SHA (immutable, rollback) + latest (convenience)

### Limitations & Areas for Improvement

1. **No persistent storage** — Session state only; lost on restart. Needs a database for production.
2. **No authentication** — `authenticated = True` hardcoded. Needs Azure AD or similar.
3. **No real data integration** — Dashboards use hardcoded sample data.
4. **Settings don't persist** — Theme, org settings are session-only.
5. **`python-dotenv` unused** — `load_dotenv()` never called.
6. **CORS/XSRF disabled** — Security concern if exposed directly.
7. **Single LLM model** — Hardcoded; no model selector.
8. **No input sanitization** — User text passed directly to prompts.
9. **Appearance settings non-functional** — Theme selector stored but not applied.
10. **New AIService per rerun** — Could use `@st.cache_resource` for efficiency.

---

*Document generated from a complete read of every file in the repository.*
