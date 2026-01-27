# Azure DevOps Pipeline Setup Guide

## Overview
This guide provides step-by-step instructions for setting up a production-grade Terraform pipeline in Azure DevOps.

## Prerequisites - IMPORTANT: Install Terraform Extension

### ⚠️ Required Extension
Before proceeding with pipeline setup, you **MUST** install the **Terraform** extension from the Azure DevOps Marketplace:

**Extension Details:**
- **Name:** Terraform
- **Publisher:** Microsoft DevLabs
- **Installs:** 133,376+
- **Link:** https://marketplace.visualstudio.com/items?itemName=ms-devlabs.custom-terraform-tasks

### Installation Steps (Required Before Setup)
1. Go to **Azure DevOps Organization** → **Organization Settings**
2. Click **Extensions** 
3. Click **Browse marketplace**
4. Search for: `Terraform`
5. Find **"Terraform"** published by **Microsoft DevLabs**
6. Click **Get it free**
7. Select your organization from dropdown
8. Click **Install**
9. **Wait 1-2 minutes** for installation to complete
10. You'll receive a confirmation email

### Verify Installation
1. In Azure DevOps: **Organization Settings** → **Extensions**
2. Look for **"Terraform"** in the installed extensions list
3. Should show: ✅ Green checkmark + "Microsoft DevLabs" as publisher
4. **Pipeline is now ready to use!**

### Troubleshooting Extension Installation
**If you don't see the extension:**
- Clear browser cache (Ctrl+Shift+Delete)
- Wait 5 minutes and refresh
- Try different browser
- Contact Azure DevOps support

---

### Other Prerequisites
✅ Azure DevOps organization and project created
✅ Azure Service Principal with appropriate permissions
✅ Azure Storage Account for Terraform state backend
✅ Azure DevOps Service Connection configured

## Setup Steps

### 1. Verify Service Connection
- **Name:** azuredevops-azure
- **Type:** Azure Resource Manager
- **Authentication:** Service Principal
- **Scope:** Your Azure Subscription

### 2. Create Variable Group
Follow these steps in Azure DevOps:

1. Go to **Pipelines** → **Library** → **Variable groups**
2. Create new group: **Terraform-Secrets**
3. Add the following variables (mark sensitive variables as Secret):

| Variable Name | Value | Secret |
|---|---|---|
| BACKEND_CONTAINER | tfstate | No |
| BACKEND_KEY | prod.terraform.tfstate | No |
| BACKEND_RESOURCE_GROUP | terraform | No |
| BACKEND_STORAGE_ACCOUNT | tfstateforterrform | No |
| BACKEND_STORAGE_KEY | [your-key] | ✅ Yes |
| CLIENT_ID | [your-client-id] | No |
| CLIENT_SECRET | [your-secret] | ✅ Yes |
| SUBSCRIPTION_ID | [your-subscription-id] | No |
| TENANT_ID | [your-tenant-id] | No |

4. Click **Save**

### 3. Configure Backend Storage
Ensure your Azure Storage Account is set up:

```bash
# Create resource group
az group create \
  --name terraform \
  --location eastus

# Create storage account
az storage account create \
  --name tfstateforterrform \
  --resource-group terraform \
  --location eastus \
  --sku Standard_LRS

# Create container
az storage container create \
  --name tfstate \
  --account-name tfstateforterrform

# Get storage key
az storage account keys list \
  --account-name tfstateforterrform \
  --resource-group terraform
```

### 4. Create Pipeline
1. Go to **Pipelines** → **New pipeline**
2. Select **Azure Repos Git**
3. Select your repository
4. Choose **Existing Azure Pipelines YAML file**
5. Select `azure-pipelines.yml`
6. Save and run

### 5. Update Service Connection References
In `azure-pipelines.yml`, ensure all tasks reference:
- **Service Connection Name:** `Azure-Service-Connection`
- **Variable Group:** `Terraform-Secrets`

## Pipeline Stages

### Stage 1: Validate
- Terraform format check
- Terraform validation
- Security scanning (tfsec)
- **Duration:** ~2-3 minutes

### Stage 2: Plan
- Terraform initialization
- Plan generation
- Cost estimation
- Artifact publishing
- **Duration:** ~5-10 minutes

### Stage 3: Review & Approval
- Manual approval gate
- Notifies Infrastructure Team
- **Duration:** Manual (30 min timeout default)

### Stage 4: Apply
- Downloads plan artifact
- Applies infrastructure changes
- Exports outputs
- **Duration:** ~10-20 minutes

### Stage 5: Post-Deployment Validation
- Validates Azure resources
- Checks resource health
- **Duration:** ~2-3 minutes

### Stage 6: Cleanup (Optional)
- Manual destruction gate
- Destroys all managed resources
- **Trigger:** Only on 'cleanup' branch

## Security Best Practices

### Implemented
✅ Service Principal authentication
✅ Secret variable encryption
✅ State file remote backend with locking
✅ Plan review and approval gate
✅ Security scanning (tfsec)
✅ RBAC for pipeline access

### Additional Recommendations
- [ ] Enable branch policies requiring PR reviews
- [ ] Implement approval gates for production
- [ ] Use Azure Key Vault for sensitive values
- [ ] Enable audit logging for all deployments
- [ ] Implement state file encryption
- [ ] Use dynamic secrets rotation
- [ ] Configure cost alerts and budgets

## Troubleshooting

### Pipeline fails at "Terraform Init"
- **Issue:** Backend configuration not found
- **Solution:** Verify Variable Group values and Service Connection permissions

### "Unauthorized" Error
- **Issue:** Service Principal lacks permissions
- **Solution:** 
  ```bash
  az role assignment create \
    --assignee <client-id> \
    --role "Contributor" \
    --scope /subscriptions/<subscription-id>
  ```

### Plan approval timeout
- **Issue:** Manual approval not completed in time
- **Solution:** Adjust timeout in `ManualValidation@0` task (onTimeout parameter)

### State file lock
- **Issue:** "Error acquiring the state lock"
- **Solution:** 
  ```bash
  terraform force-unlock <lock-id>
  ```

## Monitoring and Notifications

### Setting Up Notifications
1. Go to **Project Settings** → **Notifications**
2. Create subscriptions for:
   - Build completion
   - Pipeline approval pending
   - Pipeline failures

### Key Metrics to Monitor
- Pipeline duration
- Approval time
- Deployment frequency
- Infrastructure changes
- Cost trends

## Maintenance

### Regular Tasks
- [ ] Review pipeline logs monthly
- [ ] Update Terraform provider versions
- [ ] Audit IAM permissions quarterly
- [ ] Review state file for sensitive data
- [ ] Test disaster recovery procedures

### Version Updates
Update the `terraformVersion` variable in `azure-pipelines.yml`:
```yaml
variables:
  - name: terraformVersion
    value: '1.9.0'  # Update as needed
```

## Reference Documentation
- [Azure DevOps Terraform Tasks](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/deploy/terraform)
- [Terraform Backend Configuration](https://www.terraform.io/language/settings/backends/azurerm)
- [Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
