using './main.bicep'

// Customize these parameters for your deployment
param appName = 'mfg-intel-platform'
param appServicePlanSku = 'B1'
param dockerImage = 'mfg-intel-platform'
param dockerImageTag = 'latest'

// Set via command line: --parameters groqApiKey=<your-key>
// Or set the GROQ_API_KEY in Azure Portal after deployment
param groqApiKey = ''
