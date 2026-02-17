# 🏭 Manufacturing Intelligence Platform (MIP)

An AI-powered Business Analysis and Decision Intelligence platform that uses Large Language Models to automate requirements analysis, process optimization, planning, reporting, and executive decision support for advanced manufacturing innovation organizations.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 📋 Requirements Analysis
- AI-powered analysis of business requirements
- Automatic identification of functional and non-functional requirements
- Risk assessment and dependency analysis
- Priority matrix generation
- Complexity estimation
- Multiple input methods (text, upload, templates)

### ⚙️ Process Optimization
- Manufacturing process analysis
- Bottleneck identification
- Lean manufacturing recommendations
- Six Sigma integration
- Automation opportunity detection
- ROI calculations
- KPI recommendations

### 📅 Strategic Planning
- AI-assisted strategic plan generation
- Initiative portfolio management
- Roadmap visualization (Gantt charts)
- Milestone tracking
- Resource planning
- Risk management

### 📈 Reports & Analytics
- Executive report generation
- Interactive analytics dashboard
- Performance metrics visualization
- Trend analysis
- Custom report templates
- Export to multiple formats

### 🎯 Decision Support
- Multi-criteria decision analysis
- Option scoring and comparison
- Interactive decision matrix
- Risk-benefit analysis
- AI-powered recommendations
- Scenario analysis

### 💬 AI Assistant
- Conversational AI interface
- Context-aware responses
- Quick prompts for common tasks
- Chat history management
- Manufacturing domain expertise

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yashwanthmh/business-intelligence-platform.git
cd business-intelligence-platform
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables (optional)**
```bash
# Create a .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Open in browser**
Navigate to `http://localhost:8501`

## 📁 Project Structure

```
business-intelligence-platform/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
└── modules/
    ├── __init__.py            # Module exports
    ├── ai_service.py          # OpenAI integration service
    ├── requirements_analysis.py    # Requirements module
    ├── process_optimization.py     # Process optimization module
    ├── strategic_planning.py       # Strategic planning module
    ├── reports_analytics.py        # Reports & analytics module
    ├── decision_support.py         # Decision support module
    ├── ai_assistant.py            # AI chat assistant module
    └── settings.py                # Settings & configuration module
```

## ⚙️ Configuration

### OpenAI API Key
You can configure your API key in two ways:

1. **Environment Variable**
```bash
export OPENAI_API_KEY=your-api-key-here
```

2. **In-App Settings**
Navigate to Settings → API Configuration and enter your API key.

### Supported Models
- GPT-4 Turbo (recommended)
- GPT-4
- GPT-3.5 Turbo

## 🎯 Use Cases

### For Business Analysts
- Automate requirements documentation
- Generate structured analysis reports
- Track project requirements

### For Operations Managers
- Analyze manufacturing processes
- Identify optimization opportunities
- Track OEE and quality metrics

### For Executives
- Generate executive summaries
- Support strategic decision-making
- Access real-time dashboards

### For Project Managers
- Create strategic plans
- Track initiatives and milestones
- Manage project portfolios

## ☁️ Deploy to Azure

This project includes full Azure deployment support via Azure App Service (Linux containers), Azure Container Registry, Key Vault, and Bicep infrastructure-as-code.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Azure Resource Group               │
│                                                     │
│  ┌──────────────┐   ┌────────────────────────────┐  │
│  │  Container    │   │  App Service (Linux)       │  │
│  │  Registry     │──▶│  Docker container          │  │
│  │  (ACR)        │   │  Streamlit on port 8000    │  │
│  └──────────────┘   └──────────┬─────────────────┘  │
│                                │                     │
│  ┌──────────────┐   ┌─────────▼──────────────────┐  │
│  │  Key Vault    │   │  Log Analytics Workspace   │  │
│  │  (secrets)    │   │  (monitoring & logs)        │  │
│  └──────────────┘   └────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed
- An Azure subscription
- A Groq API key

### Option A: Deploy via CLI (Manual)

**1. Log in to Azure and create a resource group:**

```bash
az login
az group create --name mfg-intel-platform-rg --location eastus
```

**2. Deploy the infrastructure:**

```bash
az deployment group create \
  --resource-group mfg-intel-platform-rg \
  --template-file infra/main.bicep \
  --parameters groqApiKey=<YOUR_GROQ_API_KEY>
```

**3. Get the deployment outputs:**

```bash
az deployment group show \
  --resource-group mfg-intel-platform-rg \
  --name main \
  --query properties.outputs
```

**4. Build and push the Docker image:**

```bash
# Get your ACR name from the outputs above
ACR_NAME=<acr-name-from-outputs>

az acr login --name $ACR_NAME
docker build -t $ACR_NAME.azurecr.io/mfg-intel-platform:latest .
docker push $ACR_NAME.azurecr.io/mfg-intel-platform:latest
```

**5. Restart the Web App to pick up the new image:**

```bash
WEBAPP_NAME=<webapp-name-from-outputs>
az webapp restart --name $WEBAPP_NAME --resource-group mfg-intel-platform-rg
```

### Option B: Deploy via GitHub Actions (CI/CD)

**1. Deploy infrastructure first** using the "Deploy Azure Infrastructure" workflow (manual trigger from the Actions tab).

**2. Set up GitHub repository secrets:**

| Secret | Description |
|--------|-------------|
| `AZURE_CLIENT_ID` | Service principal / federated credential client ID |
| `AZURE_TENANT_ID` | Azure AD tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID |
| `ACR_NAME` | Container Registry name (from infra deployment output) |
| `AZURE_WEBAPP_NAME` | Web App name (from infra deployment output) |
| `GROQ_API_KEY` | Your Groq API key (used by infra workflow) |

**3. Push to `main`** — the "Build and Deploy to Azure" workflow will automatically build the Docker image and deploy it.

### Local Docker Testing

```bash
docker build -t mfg-intel-platform .
docker run -p 8000:8000 -e GROQ_API_KEY=your-key mfg-intel-platform
# Open http://localhost:8000
```

## 🔧 Development

### Running in Development Mode
```bash
streamlit run app.py --server.runOnSave true
```

### Adding New Modules
1. Create a new module in `modules/`
2. Implement the `render()` method
3. Add to `modules/__init__.py`
4. Update navigation in `app.py`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI GPT-4](https://openai.com/)
- Charts by [Plotly](https://plotly.com/)


---
