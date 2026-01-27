# Azure DevOps Pipeline Configuration

This file provides the configuration reference for the production-grade Terraform deployment pipeline.

## Service Connection Requirements

### Name: Azure-Service-Connection
**Type:** Azure Resource Manager  
**Authentication:** Service Principal  

Ensure this service connection has:
- Contributor role on target subscription
- Access to storage account for state backend
- Permissions to create/modify all Azure resources

## Variable Group: Terraform-Secrets

### Location
**Path:** Pipelines → Library → Variable groups → Terraform-Secrets

### Required Variables

| Name | Value | Type | Secret |
|------|-------|------|--------|
| BACKEND_CONTAINER | tfstate | String | ❌ |
| BACKEND_KEY | prod.terraform.tfstate | String | ❌ |
| BACKEND_RESOURCE_GROUP | terraform | String | ❌ |
| BACKEND_STORAGE_ACCOUNT | tfstateforterrform | String | ❌ |
| BACKEND_STORAGE_KEY | [Storage Account Key] | String | ✅ |
| CLIENT_ID | 0dfa47eb-cb5f-4a19-8edc-192901b73c82 | String | ❌ |
| CLIENT_SECRET | [Service Principal Secret] | String | ✅ |
| SUBSCRIPTION_ID | f4ffefe1-d689-4059-969c-ccc73e2a11d4 | String | ❌ |
| TENANT_ID | 4cef0d84-84d6-4ed0-8abe-773b015bcf99 | String | ❌ |

### How to Create in Azure DevOps

1. Navigate to **Pipelines** → **Library**
2. Click **+ Variable group**
3. Name: `Terraform-Secrets`
4. Add each variable from table above
5. For secret variables (marked with ✅):
   - Click lock icon to mark as secret
   - Value will be encrypted in Azure DevOps
6. Click **Save**

### Getting Variable Values

```bash
# Get storage account key
az storage account keys list \
  --account-name tfstateforterrform \
  --resource-group terraform \
  --query '[0].value' -o tsv

# Get service principal details
az ad app list --display-name TerraformSP

# Get current subscription
az account show --query id -o tsv

# Get tenant ID
az account show --query tenantId -o tsv
```

## Pipeline Stages Detailed Configuration

### Stage 1: Validate

**Runs:** On every commit to main branch or PR  
**Agents:** ubuntu-latest  
**Duration:** ~2-3 minutes  

**Jobs:**
- ValidateAndScan

**Steps:**
1. Checkout code
2. Install Terraform
3. Initialize backend
4. Format validation
5. Syntax validation
6. Security scan (tfsec)

**Success Criteria:**
- All format checks pass
- Terraform validates successfully
- No critical security issues

### Stage 2: Plan

**Depends On:** Validate stage  
**Duration:** ~5-10 minutes  
**Artifacts:** Publishes terraform-plan  

**Jobs:**
- PlanJob

**Steps:**
1. Checkout code
2. Install Terraform
3. Initialize backend
4. Generate plan
5. Export plan summary
6. Publish artifacts

**Artifacts Generated:**
- `tfplan` - Binary Terraform plan
- `tfplan.json` - JSON format plan
- `outputs.json` - Infrastructure outputs

### Stage 3: ReviewApproval

**Depends On:** Plan stage  
**Duration:** Manual (30 min timeout)  

**Jobs:**
- HoldForReview (server job - no agent)

**Steps:**
1. Manual validation required
2. Notifies Infrastructure-Team
3. Waits for approval (timeout: 30 min)
4. Rejects on timeout

**Approval Checklist:**
- [ ] Plan output reviewed
- [ ] Resource changes understood
- [ ] No unexpected deletions
- [ ] Security implications reviewed
- [ ] Cost impact acceptable

### Stage 4: Apply

**Depends On:** ReviewApproval  
**Duration:** ~10-20 minutes  

**Jobs:**
- ApplyJob

**Steps:**
1. Checkout code
2. Install Terraform
3. Download plan artifact
4. Initialize backend
5. Apply plan
6. Export outputs
7. Publish outputs artifact

**Lock Settings:**
- State file locked during apply
- Prevents concurrent modifications
- Auto-unlocked on completion

### Stage 5: PostDeploymentValidation

**Depends On:** Apply stage  
**Duration:** ~2-3 minutes  

**Jobs:**
- ValidationJob

**Steps:**
1. Validate Azure resources deployed
2. Check resource groups
3. Verify configurations

### Stage 6: Cleanup (Optional)

**Trigger:** Only on 'cleanup' branch  
**Requires:** Manual confirmation  

**Jobs:**
1. ConfirmDestroy (approval gate)
2. DestroyResources (if approved)

**Destroys:**
- All managed Terraform resources
- State file preserved

## Environment Variables

### Passed to Terraform

```bash
ARM_SUBSCRIPTION_ID    = SUBSCRIPTION_ID
ARM_TENANT_ID          = TENANT_ID
ARM_CLIENT_ID          = CLIENT_ID
ARM_CLIENT_SECRET      = CLIENT_SECRET
ARM_ACCESS_KEY         = BACKEND_STORAGE_KEY
```

### Pipeline-Specific

```bash
terraformVersion       = 1.9.0
azureCliVersion        = latest
tfPlanArtifact        = terraform-plan
System.PreferGitFromPath = true
```

## Branch Policies Recommended

### For main branch:

1. **Require pull request reviews**
   - Minimum reviewers: 1
   - Requestors cannot approve

2. **Check for linked work items**
   - Required for traceability

3. **Enforce status checks**
   - Validate stage must succeed

4. **Limit merge types**
   - Squash or no fast-forward

## Notification Setup

### Pipeline Notifications

1. Go to **Project Settings** → **Notifications**
2. Create subscriptions:
   - **Build failed** - Notify on failure
   - **Build completed** - Track all runs
   - **Pull request policy override** - Security

### Email Templates Recommended

```
Subject: Terraform Pipeline [#{build.buildNumber}] - {status}

Build: {project} / {pipeline}
Status: {status}
Branch: {sourceBranch}
Commit: {sourceVersion} - {sourceVersionMessage}

Plan Summary: [Link to artifacts]
Logs: [Link to pipeline run]
```

## Troubleshooting Pipeline Issues

### Service Connection Not Found
**Error:** "The specified service connection does not exist."

**Solution:**
```
1. Go to Project Settings → Service connections
2. Verify connection name matches: Azure-Service-Connection
3. Check service connection has access to subscription
4. Grant Pipeline permissions to connection
```

### Variable Group Not Found
**Error:** "Variable group 'Terraform-Secrets' not found."

**Solution:**
```
1. Verify variable group exists: Pipelines → Library
2. Check group name: Terraform-Secrets
3. Verify user has access to group
4. If new group, may need to re-save pipeline
```

### Terraform State Lock
**Error:** "Error acquiring the state lock"

**Solution:**
```bash
# List locks
terraform state list

# Force unlock (use carefully)
terraform force-unlock <lock-id>

# Or via Azure CLI
az storage blob metadata show \
  --account-name tfstateforterrform \
  --container-name tfstate \
  --name prod.terraform.tfstate.lock
```

### Authentication Failures
**Error:** "Unauthorized to access Azure subscription"

**Solution:**
```
1. Verify service principal exists in Azure AD
2. Check role assignment on subscription
3. Verify credentials in variable group
4. Ensure client secret is valid
```

## Monitoring Pipeline Performance

### Key Metrics

| Metric | Target | Action |
|--------|--------|--------|
| Validate Duration | < 5 min | Optimize code if exceeds |
| Plan Duration | < 15 min | Check resource count |
| Apply Duration | < 30 min | Review logs if exceeds |
| Approval Time | < 1 hour | Set SLA for team |

### Pipeline Analytics

1. Go to **Pipelines** → **Pipelines**
2. Select pipeline
3. Click **Analytics**
4. Review:
   - Pass rate
   - Average duration
   - Stage performance
   - Failure trends

## Best Practices

✅ **Always review plans before approval**  
✅ **Keep variable group secrets encrypted**  
✅ **Use specific branch names for cleanup**  
✅ **Monitor pipeline logs regularly**  
✅ **Update Terraform versions quarterly**  
✅ **Test in non-prod first**  
✅ **Maintain audit trail**  
✅ **Document all customizations**  

## Reference

- [Azure DevOps Pipelines Docs](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
- [Pipeline YAML Schema](https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema)
