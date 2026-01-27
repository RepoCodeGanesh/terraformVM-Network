# Security Guidelines for Terraform Infrastructure

## Overview
This document outlines security best practices and measures implemented in this Terraform configuration and CI/CD pipeline.

## 1. Authentication & Authorization

### Service Principal Setup
```bash
# Create service principal
az ad sp create-for-rbac \
  --name TerraformSP \
  --role Contributor \
  --scopes /subscriptions/{subscription-id}
```

### RBAC Best Practices
- [ ] Use least privilege principle (Contributor minimum)
- [ ] Consider using custom roles for production
- [ ] Regularly audit access permissions
- [ ] Remove unused service principals

## 2. Secrets Management

### Current Implementation
- Client Secret stored in Azure DevOps Variable Group (encrypted)
- Backend storage key encrypted in variable group
- Subscription/Tenant IDs (non-sensitive) in variables

### Recommended Improvements
```
Option 1: Azure Key Vault Integration
- Store secrets in Azure Key Vault
- Reference from pipeline using AzureKeyVault task

Option 2: Managed Identity
- Use managed identity instead of service principal
- Eliminate need to manage client secrets

Implementation:
az keyvault create \
  --name tfSecrets \
  --resource-group terraform \
  --enable-soft-delete true \
  --purge-protection-enabled

az keyvault secret set \
  --vault-name tfSecrets \
  --name ClientSecret \
  --value <client-secret>
```

### Never Commit
```
❌ terraform.tfvars
❌ client_secret.txt
❌ *.tfstate files
❌ Variable values with secrets
```

## 3. State Management

### Backend Configuration
```terraform
backend "azurerm" {
  resource_group_name  = "terraform"
  storage_account_name = "tfstateforterrform"
  container_name       = "tfstate"
  key                  = "prod.terraform.tfstate"
}
```

### Security Measures
- [ ] Enable Storage Account encryption (at rest)
- [ ] Enable HTTPS only
- [ ] Restrict network access (firewall rules)
- [ ] Enable versioning for recovery
- [ ] Enable soft delete for accidental deletions
- [ ] Use managed identities instead of keys

### Storage Account Configuration
```bash
# Enable encryption
az storage account update \
  --name tfstateforterrform \
  --resource-group terraform \
  --https-only true

# Enable versioning
az storage account blob-service-properties update \
  --account-name tfstateforterrform \
  --resource-group terraform \
  --enable-restore-policy true

# Configure firewall
az storage account update \
  --name tfstateforterrform \
  --resource-group terraform \
  --default-action Deny \
  --bypass AzureServices

# Add IP whitelist for pipeline agents
az storage account network-rule add \
  --account-name tfstateforterrform \
  --resource-group terraform \
  --ip-address <azure-devops-agent-ip>/32
```

## 4. Code Security

### Terraform Best Practices
- [ ] Use `.tfvars.example` for documentation
- [ ] Keep sensitive data out of code
- [ ] Use `sensitive = true` for outputs
- [ ] Validate all inputs
- [ ] Use variables for all customizable values

### Example - Sensitive Variables
```terraform
variable "client_secret" {
  type        = string
  sensitive   = true
  description = "Service principal client secret"
}

variable "admin_password" {
  type        = string
  sensitive   = true
  description = "VM admin password - store in Key Vault"
}

output "resource_ids" {
  value     = azurerm_virtual_machine.vm[*].id
  sensitive = true
}
```

## 5. Pipeline Security

### Implemented Safeguards
✅ **Plan Review Gate** - Manual approval required before apply
✅ **Service Principal Auth** - No stored credentials in code
✅ **Variable Group Encryption** - Secrets encrypted in transit/rest
✅ **Format Validation** - Code style enforcement
✅ **Security Scanning** - tfsec for compliance checks
✅ **State Locking** - Prevents concurrent modifications
✅ **Audit Logging** - All changes logged in Azure

### Additional Recommendations
- [ ] Enable branch policies (PR reviews required)
- [ ] Implement required reviewers
- [ ] Use status checks for validation
- [ ] Enable commit signing
- [ ] Audit all pipeline executions
- [ ] Set up alerts for failed deployments

```yaml
# Pipeline branch policy example
pr:
  branches:
    include:
      - main
  paths:
    include:
      - '**/*.tf'
```

## 6. Azure Resource Security

### Default Implementations
- [ ] Network security groups configured
- [ ] Managed identities for VMs
- [ ] Encryption at rest enabled
- [ ] HTTPS/TLS for communications
- [ ] Diagnostic logs to Log Analytics

### VM Security
```terraform
# SSH key-based authentication (recommended)
variable "ssh_key" {
  type        = string
  description = "SSH public key for VM access"
  sensitive   = true
}

# Multi-factor authentication for management
# Implement using Azure AD Conditional Access

# Disk encryption
variable "disk_encryption_enabled" {
  type    = bool
  default = true
}
```

## 7. Network Security

### Recommended Network Configuration
```terraform
# Network Security Groups
- Deny all inbound by default
- Allow only necessary ports
- Restrict to specific IPs/ranges
- Use service tags for Azure services

# Virtual Network
- Use private subnets for workloads
- Implement VPN/Bastion for management
- Enable flow logs
- Monitor with Network Watcher
```

## 8. Compliance & Auditing

### Audit Logging
```bash
# Enable audit logging for storage account
az monitor diagnostic-settings create \
  --resource /subscriptions/{id}/resourceGroups/terraform/providers/Microsoft.Storage/storageAccounts/tfstateforterrform \
  --name StorageAudit \
  --logs '[{"category":"StorageRead","enabled":true},{"category":"StorageWrite","enabled":true}]' \
  --workspace /subscriptions/{id}/resourcegroups/terraform/providers/microsoft.operationalinsights/workspaces/tfaudit
```

### Compliance Checks
- [ ] Ensure tagging standards
- [ ] Validate resource locations
- [ ] Check encryption requirements
- [ ] Monitor for non-compliant resources

## 9. Incident Response

### In Case of Compromise
1. **Immediate Actions**
   - Revoke service principal access
   - Rotate credentials
   - Enable audit logging

2. **Investigation**
   - Review pipeline execution logs
   - Check Azure activity logs
   - Audit all recent changes

3. **Remediation**
   ```bash
   # Revoke service principal
   az ad app delete --id <app-id>
   
   # Force state unlock if needed
   terraform force-unlock <lock-id>
   ```

## 10. Regular Security Tasks

### Daily
- [ ] Monitor pipeline executions
- [ ] Check for failed deployments

### Weekly
- [ ] Review access logs
- [ ] Check for unnecessary resources

### Monthly
- [ ] Audit permissions
- [ ] Review secrets rotation
- [ ] Validate backups

### Quarterly
- [ ] Security assessment
- [ ] Penetration testing
- [ ] Compliance audit
- [ ] Disaster recovery drill

## References
- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/fundamentals/)
- [Terraform Security Best Practices](https://www.terraform.io/language/state/sensitive-data)
- [Azure DevOps Security](https://docs.microsoft.com/en-us/azure/devops/organizations/security/)
