trigger:
  branches:
    include:
      - main
      - development
  paths:
    include:
      - '**/*.tf'
      - '**/*.tfvars'

pr:
  branches:
    include:
      - main
      - development
  paths:
    include:
      - '**/*.tf'
      - '**/*.tfvars'

variables:
- group: Terraform-Secrets

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: TerraformInstaller@0
  displayName: 'Install Terraform'
  inputs:
    terraformVersion: '1.5.0'

- task: TerraformTaskV3@3
  displayName: 'Terraform Init'
  inputs:
    provider: 'azurerm'
    command: 'init'
    workingDirectory: '$(System.DefaultWorkingDirectory)'
    backendServiceArm: '64d51c9d-f7f6-4ff2-8341-75d6cc57fe01'
    backendAzureRmResourceGroupName: 'terraform'
    backendAzureRmStorageAccountName: 'tfstateforterrform'
    backendAzureRmContainerName: 'tfstate'
    backendAzureRmKey: '$(Build.SourceBranchName).terraform.tfstate'

- task: TerraformTaskV3@3
  displayName: 'Terraform Validate'
  inputs:
    provider: 'azurerm'
    command: 'validate'
    workingDirectory: '$(System.DefaultWorkingDirectory)'

- task: TerraformTaskV3@3
  displayName: 'Terraform Plan'
  inputs:
    provider: 'azurerm'
    command: 'plan'
    workingDirectory: '$(System.DefaultWorkingDirectory)'
    environmentServiceNameAzureRM: '64d51c9d-f7f6-4ff2-8341-75d6cc57fe01'
    backendAzureRmResourceGroupName: 'terraform'
    backendAzureRmStorageAccountName: 'tfstateforterrform'
    backendAzureRmContainerName: 'tfstate'
    backendAzureRmKey: '$(Build.SourceBranchName).terraform.tfstate'
    commandOptions: '-no-color -out=tfplan'
  env:
    TF_VAR_client_secret: $(CLIENT_SECRET)

- task: PublishBuildArtifacts@1
  displayName: 'Publish Terraform Plan Artifact'
  inputs:
    PathtoPublish: '$(System.DefaultWorkingDirectory)/tfplan'
    ArtifactName: 'terraform-plan'
    publishLocation: 'Container'

- task: PublishBuildArtifacts@1
  displayName: 'Publish Terraform Plan Text'
  inputs:
    PathtoPublish: '$(System.DefaultWorkingDirectory)/plan.txt'
    ArtifactName: 'terraform-plan-text'
    publishLocation: 'Container'
