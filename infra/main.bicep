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
var shortSuffix = substring(uniqueSuffix, 0, 8)
var appServicePlanName = '${appName}-plan-${uniqueSuffix}'
var webAppName = '${appName}-${uniqueSuffix}'
var containerRegistryName = replace('${appName}acr${uniqueSuffix}', '-', '')
var keyVaultName = 'mfg-kv-${shortSuffix}'
var logAnalyticsName = '${appName}-logs-${uniqueSuffix}'

// ---------- Log Analytics Workspace ----------

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

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

// ---------- Key Vault ----------

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
  }
}

resource groqApiKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'groq-api-key'
  properties: {
    value: groqApiKey
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
          value: '@Microsoft.KeyVault(SecretUri=${groqApiKeySecret.properties.secretUri})'
        }
        {
          name: 'STREAMLIT_SERVER_PORT'
          value: '8000'
        }
      ]
    }
  }
}

// ---------- Key Vault Access for Web App ----------

// Grant the Web App's managed identity access to Key Vault secrets
resource keyVaultRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, webApp.id, '4633458b-17de-408a-b874-0445c86b69e6')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6') // Key Vault Secrets User
    principalId: webApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// ---------- Diagnostic Settings ----------

resource webAppDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'webAppDiagnostics'
  scope: webApp
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      {
        category: 'AppServiceHTTPLogs'
        enabled: true
      }
      {
        category: 'AppServiceConsoleLogs'
        enabled: true
      }
      {
        category: 'AppServiceAppLogs'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

// ---------- Outputs ----------

output webAppName string = webApp.name
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
output containerRegistryName string = containerRegistry.name
output keyVaultName string = keyVault.name
output keyVaultUri string = keyVault.properties.vaultUri
