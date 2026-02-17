// Azure Infrastructure for Manufacturing Intelligence Platform
// Deploy with: az deployment group create -g <resource-group> -f main.bicep -p main.bicepparam

@description('Base name for all resources')
param appName string = 'mfg-intel-platform'

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('App Service Plan SKU')
@allowed(['B1', 'B2', 'S1', 'S2', 'P1v3'])
param appServicePlanSku string = 'B1'

@description('Docker image name (without registry prefix)')
param dockerImage string = 'mfg-intel-platform'

@description('Docker image tag')
param dockerImageTag string = 'latest'

@description('Groq API key for AI services')
@secure()
param groqApiKey string = ''

// ---------- Variables ----------

var uniqueSuffix = uniqueString(resourceGroup().id)
var appServicePlanName = '${appName}-plan-${uniqueSuffix}'
var webAppName = '${appName}-${uniqueSuffix}'
var containerRegistryName = replace('${appName}acr${uniqueSuffix}', '-', '')

// ---------- Azure Container Registry ----------

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: containerRegistryName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// ---------- App Service Plan ----------

resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: appServicePlanSku
  }
  properties: {
    reserved: true // Required for Linux
  }
}

// ---------- Web App ----------

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: webAppName
  location: location
  kind: 'app,linux,container'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOCKER|${containerRegistry.properties.loginServer}/${dockerImage}:${dockerImageTag}'
      alwaysOn: true
      healthCheckPath: '/_stcore/health'
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://${containerRegistry.properties.loginServer}'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_USERNAME'
          value: containerRegistry.listCredentials().username
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_PASSWORD'
          value: containerRegistry.listCredentials().passwords[0].value
        }
        {
          name: 'GROQ_API_KEY'
          value: groqApiKey
        }
        {
          name: 'STREAMLIT_SERVER_PORT'
          value: '8000'
        }
      ]
    }
  }
}


// ---------- Outputs ----------

output webAppName string = webApp.name
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
output containerRegistryName string = containerRegistry.name
