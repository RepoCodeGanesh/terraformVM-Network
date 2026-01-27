# Deployment Guide

## Quick Start

### Prerequisites
- Azure subscription with appropriate permissions
- Azure CLI installed
- Terraform 1.9.0 or higher
- Azure DevOps account and project

### Local Development Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd terraformVM-Network

# 2. Copy example variables
cp terraform.tfvars.example terraform.tfvars

# 3. Edit variables with your values
nano terraform.tfvars

# 4. Initialize Terraform
terraform init \
  -backend-config="resource_group_name=terraform" \
  -backend-config="storage_account_name=tfstateforterrform" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=prod.terraform.tfstate"

# 5. Validate configuration
terraform validate

# 6. Format check
terraform fmt -recursive -check

# 7. Generate plan
terraform plan -out=tfplan

# 8. Review plan
terraform show tfplan

# 9. Apply (after review)
terraform apply tfplan
```

## Azure DevOps Pipeline Deployment

### Step 1: Initial Setup
1. Navigate to **Azure DevOps Project**
2. Go to **Pipelines** → **Create Pipeline**
3. Select **Azure Repos Git**
4. Choose your repository
5. Select **Existing Azure Pipelines YAML file**
6. Point to `azure-pipelines.yml`
7. Click **Save**

### Step 2: Variable Group Configuration
1. Go to **Pipelines** → **Library** → **Variable groups**
2. Click **+ Variable group**
3. Name: `Terraform-Secrets`
4. Add variables (see below)
5. Mark sensitive fields as Secret
6. Click **Save**

#### Required Variables:
```
BACKEND_CONTAINER         = tfstate
BACKEND_KEY              = prod.terraform.tfstate
BACKEND_RESOURCE_GROUP   = terraform
BACKEND_STORAGE_ACCOUNT  = tfstateforterrform
BACKEND_STORAGE_KEY      = [from az storage account keys list]
CLIENT_ID                = [service principal ID]
CLIENT_SECRET            = [service principal secret] ✓ MARK AS SECRET
SUBSCRIPTION_ID          = [your subscription ID]
TENANT_ID                = [your tenant ID]
```

### Step 3: Service Connection Setup
1. Go to **Project Settings** → **Service connections**
2. Create **Azure Resource Manager** connection
3. Name: `Azure-Service-Connection`
4. Use Service Principal authentication
5. Grant permissions to required subscriptions

### Step 4: Branch Policy Configuration (Optional but Recommended)
1. Go to **Repos** → **Branches**
2. Select your main branch
3. Click **Branch policies**
4. Enable:
   - Require a minimum number of reviewers: 1
   - Check for linked work items
   - Check for comment resolution

### Step 5: Run Pipeline
1. Commit changes to your branch
2. Pipeline triggers automatically
3. Monitor execution in **Pipelines** section
4. Review plan output
5. Approve manual validation step
6. Monitor apply stage completion

## Deployment Stages Details

### Stage 1: Validation (2-3 min)
```
✓ Format check - Ensures consistent code style
✓ Syntax validation - Validates Terraform syntax
✓ Security scan - Runs tfsec compliance checks
```

### Stage 2: Plan (5-10 min)
```
✓ Backend initialization
✓ Plan generation with locking
✓ Artifact publishing
✓ Output summary
```

**Review output for:**
- Unexpected resource creation
- Resource deletions
- Configuration changes

### Stage 3: Approval (Manual)
```
! Manual validation required
! Notifies Infrastructure Team
! 30-minute approval window
```

**Approval checklist:**
- [ ] Plan output reviewed
- [ ] Resource changes understood
- [ ] No production impact concerns
- [ ] Security review completed

### Stage 4: Apply (10-20 min)
```
✓ Plan artifact downloaded
✓ Infrastructure deployed
✓ Outputs exported
✓ State updated
```

**Verify:**
- Resources created in Azure Portal
- Correct region and resource group
- Expected tags applied

### Stage 5: Post-Deployment (2-3 min)
```
✓ Azure resources validated
✓ Health checks performed
✓ Outputs published
```

## Monitoring Deployment

### Azure Portal
1. Navigate to resource group
2. Verify all resources are deployed
3. Check configuration matches plan
4. Review tags for proper categorization

### Pipeline Logs
1. Go to **Pipelines** → Your pipeline
2. Click on the build run
3. Review stage logs for issues
4. Download artifacts if needed

### Azure Activity Log
```bash
az monitor activity-log list \
  --resource-group <resource-group> \
  --status "Succeeded" \
  --offset 5h
```

## Common Issues & Troubleshooting

### Issue: "Error acquiring the state lock"
**Cause:** Another deployment in progress
**Solution:**
```bash
terraform force-unlock <lock-id>
```

### Issue: "Service Principal not authorized"
**Cause:** Missing role assignment
**Solution:**
```bash
az role assignment create \
  --assignee <client-id> \
  --role "Contributor" \
  --scope /subscriptions/<subscription-id>
```

### Issue: "Validation failed - missing variable"
**Cause:** terraform.tfvars missing required variable
**Solution:**
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit and fill all required values
```

### Issue: "Backend configuration error"
**Cause:** Storage account not accessible
**Solution:**
```bash
# Verify storage account exists
az storage account show \
  --name tfstateforterrform \
  --resource-group terraform

# Check access keys
az storage account keys list \
  --name tfstateforterrform \
  --resource-group terraform
```

### Issue: "Plan approval timeout"
**Cause:** No approval before 30 minutes
**Solution:**
- Re-run pipeline
- Update approval timeout in yaml
- Notify approval team earlier

## Rollback Procedures

### Manual Rollback
```bash
# Get previous state version
az storage blob list \
  --container-name tfstate \
  --account-name tfstateforterrform

# Download previous state
az storage blob download \
  --container-name tfstate \
  --name prod.terraform.tfstate \
  --account-name tfstateforterrform \
  --file prod.terraform.tfstate.backup

# Restore state
terraform state pull > current.state
# Manually restore from backup if needed
```

### Automated Rollback
```bash
# Revert to previous commit
git revert <commit-hash>
git push

# Pipeline triggers automatically
# Apply previous configuration
```

## Cost Estimation

### Before Deployment
```bash
# Generate cost estimate from plan
terraform show -json tfplan | \
  jq '.resource_changes[] | select(.change.actions[] != "no-op")'
```

### After Deployment
1. Navigate to **Cost Management** in Azure Portal
2. Set up cost alerts
3. Review monthly costs
4. Optimize as needed

## Performance Tuning

### Parallel Operations
```bash
terraform apply -parallelism=10
```

### Selective Deployment
```bash
terraform apply -target=module.network
terraform apply -target=azurerm_virtual_machine.main
```

## Backup & Disaster Recovery

### State File Backup
```bash
# Manual backup
az storage blob download \
  --container-name tfstate \
  --name prod.terraform.tfstate \
  --account-name tfstateforterrform \
  --file backup/prod.terraform.tfstate.$(date +%Y%m%d)

# Enable versioning
az storage account blob-service-properties update \
  --account-name tfstateforterrform \
  --resource-group terraform \
  --enable-restore-policy true
```

### Disaster Recovery Testing
```bash
# Monthly: Test plan generation
terraform plan -out=test.tfplan

# Quarterly: Test in non-prod environment
terraform init -backend-config="key=test.terraform.tfstate"
terraform plan
terraform destroy
```

## Next Steps

1. **Configure Monitoring**
   - Set up Azure Monitor alerts
   - Configure Application Insights
   - Enable diagnostic logs

2. **Implement Security**
   - Enable Azure Defender
   - Configure Network Security Groups
   - Set up Key Vault integration

3. **Optimize Costs**
   - Review resource sizing
   - Implement auto-shutdown policies
   - Set up cost alerts

4. **Document Architecture**
   - Create architecture diagram
   - Document naming conventions
   - Maintain runbooks

## Support & Escalation

For issues, follow this escalation path:
1. Check pipeline logs and error messages
2. Review Terraform documentation
3. Consult Azure DevOps documentation
4. Contact Infrastructure Team
5. Open support ticket with Microsoft

## Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [Azure Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Azure Best Practices](https://docs.microsoft.com/en-us/azure/architecture/framework/)
