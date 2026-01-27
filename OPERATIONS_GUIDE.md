# Operations & Monitoring Guide

Comprehensive guide for operating and monitoring your Terraform infrastructure after deployment.

## 🚨 Health Monitoring

### Azure Portal Monitoring

#### Resource Health
```
1. Go to Resource Groups → Your Resource Group
2. Select "Resource Health"
3. View availability status
4. Check for any warnings or issues
```

#### Cost Management
```
1. Navigate to Cost Management + Billing
2. Review costs by:
   - Resource
   - Resource group
   - Service
3. Set budgets and alerts
4. Analyze spending trends
```

#### Activity Log
```
1. Resource Group → Activity Log
2. Filter by:
   - Time range
   - Resource type
   - Operation
3. Review all infrastructure changes
4. Audit who made changes and when
```

### Metrics & Alerts

#### Create VM CPU Alert
```bash
az monitor metrics alert create \
  --name cpu-alert \
  --resource-group terraform \
  --scopes <vm-resource-id> \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action email-action
```

#### Create Storage Alert
```bash
az monitor metrics alert create \
  --name storage-alert \
  --resource-group terraform \
  --scopes <storage-resource-id> \
  --condition "total UsedCapacity > 10737418240" \
  --action email-action
```

### Logging Configuration

#### Enable Diagnostic Logs
```bash
# For Virtual Machines
az monitor diagnostic-settings create \
  --resource <vm-resource-id> \
  --name vm-diagnostics \
  --logs '[{"category":"VMGuestOperatingSystemEvent","enabled":true}]'

# For Storage Account
az monitor diagnostic-settings create \
  --resource <storage-resource-id> \
  --name storage-diagnostics \
  --logs '[{"category":"StorageRead","enabled":true},{"category":"StorageWrite","enabled":true}]'
```

## 📊 Performance Monitoring

### VM Performance

#### Check CPU and Memory
```bash
# Real-time metrics
az monitor metrics list-definitions \
  --resource-group terraform \
  --resource <vm-name> \
  --resource-type "Microsoft.Compute/virtualMachines"

# Get specific metric
az monitor metrics list \
  --resource <vm-resource-id> \
  --metric "Percentage CPU" \
  --start-time 2024-01-20T00:00:00Z \
  --interval PT1M
```

#### Network Performance
```bash
# Inbound traffic
az monitor metrics list \
  --resource <vm-resource-id> \
  --metric "Network In Total"

# Outbound traffic
az monitor metrics list \
  --resource <vm-resource-id> \
  --metric "Network Out Total"
```

### Storage Performance

#### Monitor Storage Account
```bash
az monitor metrics list \
  --resource <storage-resource-id> \
  --metric "UsedCapacity" \
  --start-time 2024-01-20T00:00:00Z
```

## 🔄 State Management

### Check Current State
```bash
# List all resources in state
terraform state list

# Show specific resource
terraform state show azurerm_resource_group.main

# Export state as JSON
terraform state pull > state.json
```

### State Refresh
```bash
# Update state with current Azure resources
terraform refresh

# Verify changes
terraform state list
```

### State Recovery

#### Backup State
```bash
# Manual backup
terraform state pull > backup.tfstate.$(date +%Y%m%d-%H%M%S)

# Automated backup (script)
#!/bin/bash
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR
terraform state pull > $BACKUP_DIR/state.tfstate.$(date +%Y%m%d-%H%M%S)
```

#### Restore State
```bash
# Restore from backup
terraform state push backup.tfstate.20240120-120000
```

## 🔧 Infrastructure Updates

### Update VM Size
```hcl
# 1. Update variables.tf
variable "vm_size" {
  default = "Standard_D2s_v3"  # Changed from Standard_B2s
}

# 2. Plan and review
terraform plan

# 3. Apply
terraform apply

# Note: Requires VM restart
```

### Add New VMs
```hcl
# 1. Update variables
variable "vm_count" {
  default = 3  # Increased from 2
}

# 2. Plan changes
terraform plan

# 3. Apply
terraform apply
```

### Update Network Configuration
```hcl
# 1. Modify network module
module "network" {
  # Update configuration
}

# 2. Plan network changes only
terraform plan -target=module.network

# 3. Apply
terraform apply -target=module.network
```

## 🔒 Security Updates

### Rotate Service Principal Credentials
```bash
# Create new client secret
az ad app credential reset \
  --id <app-id> \
  --append

# Update in Variable Group:
# 1. Go to Pipelines → Library → Terraform-Secrets
# 2. Update CLIENT_SECRET with new value
# 3. Mark as secret
# 4. Save
```

### Update VM Credentials
```bash
# Reset VM password
az vm user update \
  --resource-group terraform \
  --name <vm-name> \
  --username azureuser \
  --password <new-password>

# Or use SSH key (recommended)
az vm user update \
  --resource-group terraform \
  --name <vm-name> \
  --username azureuser \
  --ssh-key-values "@ssh-keys.pub"
```

### Update Network Security Groups
```bash
# View current rules
az network nsg rule list \
  --resource-group terraform \
  --nsg-name <nsg-name>

# Add new rule
az network nsg rule create \
  --resource-group terraform \
  --nsg-name <nsg-name> \
  --name AllowHTTPS \
  --protocol tcp \
  --source-address-prefix "*" \
  --source-port-range "*" \
  --destination-address-prefix "*" \
  --destination-port-range 443 \
  --access Allow \
  --priority 102
```

## 📈 Scaling Operations

### Scale Up VMs
```bash
# 1. Update vm_size variable
variable "vm_size" {
  default = "Standard_D4s_v3"  # Larger instance
}

# 2. Plan and apply
terraform plan
terraform apply

# Note: Requires deallocate → resize → deallocate cycle
```

### Add More VMs
```bash
# Update count
variable "vm_count" {
  default = 5
}

# Preview new resources
terraform plan -target=azurerm_virtual_machine.main

# Apply
terraform apply -target=azurerm_virtual_machine.main
```

### Auto-Scaling (if applicable)
```bash
# Configure auto-scale (not in current Terraform)
az monitor autoscale create \
  --resource-group terraform \
  --resource <resource-id> \
  --resource-type "Microsoft.Compute/virtualMachines" \
  --min-count 2 \
  --max-count 10 \
  --count 3
```

## 🗑️ Resource Cleanup

### Remove Specific Resources
```bash
# Remove from state (keep in Azure)
terraform state rm azurerm_resource_group.old

# Destroy specific resource
terraform destroy -target=azurerm_virtual_machine.old
```

### Full Cleanup
```bash
# Review what will be destroyed
terraform plan -destroy

# Confirm destruction
terraform destroy
```

## 📋 Regular Maintenance Tasks

### Daily Checks (15 min)
- [ ] Monitor pipeline executions
- [ ] Check for failed deployments
- [ ] Review critical alerts

### Weekly Checks (1 hour)
- [ ] Review cost trends
- [ ] Check resource health
- [ ] Audit access logs
- [ ] Verify backups completed

### Monthly Tasks (2 hours)
- [ ] Full security audit
- [ ] Review and update documentation
- [ ] Performance analysis
- [ ] Capacity planning review
- [ ] Cost optimization review

### Quarterly Tasks (4 hours)
- [ ] Disaster recovery drill
- [ ] Security penetration test
- [ ] Compliance audit
- [ ] Architecture review
- [ ] Update Terraform versions

### Annual Tasks (1 day)
- [ ] Complete infrastructure audit
- [ ] Security assessment
- [ ] Cost optimization analysis
- [ ] Capacity planning for next year
- [ ] Update disaster recovery plan

## 📞 Incident Response

### VM Not Responding
```bash
# 1. Check boot status
az vm get-instance-view \
  --resource-group terraform \
  --name <vm-name> \
  --query "instanceView.statuses"

# 2. Check serial console
az serial-console connect \
  --resource-group terraform \
  --name <vm-name>

# 3. Restart if needed
az vm restart \
  --resource-group terraform \
  --name <vm-name>
```

### Storage Account Not Responding
```bash
# Check account status
az storage account show \
  --name tfstateforterrform \
  --resource-group terraform

# Check network rules
az storage account network-rule list \
  --account-name tfstateforterrform \
  --resource-group terraform
```

### Pipeline Failure
```bash
# 1. Check pipeline logs
# Pipelines → Run → Click failed stage

# 2. Check state locks
terraform state list

# 3. View diagnostics
az monitor activity-log list \
  --resource-group terraform \
  --max-events 50

# 4. Force unlock if needed (carefully!)
terraform force-unlock <lock-id>
```

## 📊 Reporting

### Monthly Status Report Template
```
## Infrastructure Status Report - January 2024

### Summary
- Infrastructure Status: [Green/Yellow/Red]
- Uptime: 99.9%
- Cost: $X,XXX

### Key Metrics
- VM CPU Average: X%
- VM Memory Average: X%
- Storage Used: XGB
- Network Traffic: XGB

### Changes Made
- [List of Terraform applies]
- [Security updates applied]
- [Configuration changes]

### Issues & Resolution
- [Issue 1]: [Resolution]
- [Issue 2]: [Resolution]

### Next Steps
- [Planned improvements]
- [Security updates needed]
- [Cost optimization opportunities]

### Approval
- Reviewed by: _______________
- Approved by: _______________
- Date: _______________
```

### Cost Optimization Report
```bash
# Analyze costs
az consumption usage list \
  --subscription <id> \
  --format table

# Group by service
az consumption usage list \
  --subscription <id> \
  --query "value[].{Service: meterDetails.meterName, Cost: cost}" \
  --format table

# Find idle resources
az resource list \
  --resource-group terraform \
  --query "[?tags.AutoShutdown=='true']"
```

## 🔔 Notification Setup

### Alert Rules

```bash
# Create alert for high CPU
az monitor metrics alert create \
  --resource-group terraform \
  --name HighCPUAlert \
  --scopes <vm-id> \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --action webhook-action

# Create alert for deployment failure
# Set up in Azure DevOps Notifications
```

### Email Notifications
1. Go to **Project Settings** → **Notifications**
2. Create rules for:
   - Pipeline failures
   - Release approvals
   - Build completions
3. Configure recipients
4. Set frequency

## 📚 Documentation Maintenance

### Update Documentation When:
- [ ] Infrastructure design changes
- [ ] Adding new resources
- [ ] Modifying deployment process
- [ ] Security procedures updated
- [ ] Runbooks created/modified

### Keep Updated:
- [ ] [README.md](README.md)
- [ ] [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [ ] [SECURITY.md](SECURITY.md)
- [ ] [PIPELINE_CONFIG_REFERENCE.md](PIPELINE_CONFIG_REFERENCE.md)
- [ ] Runbooks for common tasks

## 🎓 Team Training

### Monthly Training Topics
- Terraform basics (Month 1)
- Azure DevOps pipelines (Month 2)
- Security best practices (Month 3)
- Disaster recovery (Month 4)
- Cost optimization (Month 5)
- Performance tuning (Month 6)

### Documentation for Team
- [ ] Create runbooks for common tasks
- [ ] Document troubleshooting procedures
- [ ] Maintain escalation contacts
- [ ] Update team wiki/knowledge base

## References

- [Azure Monitoring Documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/)
- [Terraform State Management](https://www.terraform.io/language/state)
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/)
- [Azure Best Practices](https://docs.microsoft.com/en-us/azure/architecture/framework/)
