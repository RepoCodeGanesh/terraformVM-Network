# Terraform VM & Network Infrastructure

Production-grade Terraform configuration for deploying Azure Virtual Machines and Network infrastructure with CI/CD automation via Azure DevOps.

## 📋 Overview

This repository contains:
- **Terraform Configuration** for Azure VMs and networking
- **Azure DevOps Pipeline** with production-grade stages
- **Security Best Practices** implementation
- **Modular Architecture** for scalability

### Pipeline Stages
1. **Validate** - Format, syntax, and security checks
2. **Plan** - Generate infrastructure plan
3. **Review** - Manual approval gate
4. **Apply** - Deploy infrastructure
5. **Validate** - Post-deployment verification
6. **Cleanup** - Optional resource destruction

## 🚀 Quick Start

### Prerequisites
- Azure Subscription
- Terraform 1.9.0+
- Azure CLI
- Azure DevOps Account
- Service Principal with Contributor role

### Local Development

```bash
# Initialize backend
terraform init \
  -backend-config="resource_group_name=terraform" \
  -backend-config="storage_account_name=tfstateforterrform" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=prod.terraform.tfstate"

# Validate
terraform validate

# Plan
terraform plan -out=tfplan

# Apply
terraform apply tfplan
```

### Azure DevOps Pipeline Setup

See [PIPELINE_SETUP.md](PIPELINE_SETUP.md) for detailed instructions.

## 📁 Directory Structure

```
.
├── main.tf              # Main resource definitions
├── variables.tf         # Variable declarations
├── outputs.tf           # Output definitions
├── providers.tf         # Provider configuration
├── backend.tf           # State backend configuration
├── terraform.tfvars     # Variable values (not in git)
├── terraform.tfvars.example  # Example variables (for reference)
├── azure-pipelines.yml  # Azure DevOps pipeline
├── modules/
│   ├── network/         # Network module (VNets, NSGs)
│   └── vm/              # VM module (instances, disks)
├── PIPELINE_SETUP.md    # Pipeline configuration guide
├── DEPLOYMENT_GUIDE.md  # Step-by-step deployment
└── SECURITY.md          # Security best practices
```

## 🔐 Security Features

✅ **Service Principal Authentication** - No hardcoded credentials  
✅ **State File Encryption** - Remote backend with locking  
✅ **Secrets Management** - Encrypted variable groups  
✅ **Plan Approval Gates** - Manual review required  
✅ **Security Scanning** - tfsec compliance checks  
✅ **Audit Logging** - All changes tracked  
✅ **RBAC** - Least privilege access  

See [SECURITY.md](SECURITY.md) for comprehensive security guidelines.

## 📋 Configuration

### Required Variables
```hcl
BACKEND_RESOURCE_GROUP      = "terraform"
BACKEND_STORAGE_ACCOUNT     = "tfstateforterrform"
BACKEND_CONTAINER          = "tfstate"
BACKEND_KEY                = "prod.terraform.tfstate"
CLIENT_ID                  = "service-principal-id"
CLIENT_SECRET              = "service-principal-secret"
SUBSCRIPTION_ID            = "subscription-id"
TENANT_ID                  = "tenant-id"
```

### Terraform Variables
```hcl
resource_group_name        = "RGDefault"
vm_count                   = 2
vm_size                    = "Standard_B2s"
admin_username             = "azureuser"
admin_password             = "secure-password"
tags = {
  Environment = "Production"
  ManagedBy   = "Terraform"
}
```

Copy `terraform.tfvars.example` to `terraform.tfvars` and update values.

## 🔄 Workflow

### Development
```bash
# Make changes
git checkout -b feature/enhancement
# Edit .tf files
terraform plan
# Review plan output
git commit -am "Add feature"
git push
```

### CI/CD
1. **Commit** → Pipeline triggers
2. **Validate** → Code checks
3. **Plan** → Infrastructure plan
4. **Review** → Team approval
5. **Apply** → Deploy infrastructure
6. **Verify** → Post-deployment checks

## 📊 Monitoring & Logging

### Azure Portal
- Resource Groups → Monitor resources
- Cost Management → Track spending
- Activity Log → View operations

### Pipeline Logs
- Pipelines → Select build → View stage logs
- Download artifacts for detailed analysis

### Diagnostics
```bash
# Check state file
terraform state list
terraform state show <resource>

# Validate resources
az resource list --resource-group <rg>
```

## 🛠️ Troubleshooting

### Common Issues

**State Lock Error**
```bash
terraform force-unlock <lock-id>
```

**Authentication Failed**
```bash
az login
az account set --subscription <subscription-id>
```

**Plan Conflicts**
```bash
terraform refresh
terraform plan
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#troubleshooting) for more solutions.

## 📝 Best Practices Implemented

✅ Modular design (network, vm modules)  
✅ Variable validation and defaults  
✅ Sensitive data protection  
✅ Remote state management  
✅ State file locking  
✅ Plan review before apply  
✅ Comprehensive error handling  
✅ Audit logging and monitoring  
✅ Disaster recovery procedures  
✅ Cost estimation  

## 🔄 Maintenance

### Regular Tasks
- [ ] Monthly: Review pipeline logs and performance
- [ ] Monthly: Update Terraform provider versions
- [ ] Quarterly: Audit access and permissions
- [ ] Quarterly: Review and optimize costs
- [ ] Semi-annual: Disaster recovery drill

### Version Management
Update `terraformVersion` in `azure-pipelines.yml`:
```yaml
variables:
  - name: terraformVersion
    value: '1.9.0'
```

## 📚 Documentation

- [Pipeline Setup Guide](PIPELINE_SETUP.md) - Configure Azure DevOps
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Deploy infrastructure
- [Security Guidelines](SECURITY.md) - Security best practices
- [Terraform Docs](https://www.terraform.io/docs)
- [Azure Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest)

## 🚨 Important Notes

### Never Commit
- ❌ `terraform.tfvars` - Contains secrets
- ❌ `client_secret.txt` - Service principal secret
- ❌ `*.tfstate` files - Infrastructure state
- ❌ Any hardcoded credentials

### Always Use
- ✅ Azure DevOps Variable Groups for secrets
- ✅ Remote state backend
- ✅ Service principal authentication
- ✅ Plan review before apply
- ✅ Proper tagging for cost tracking

## 📞 Support

For issues or questions:
1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review [SECURITY.md](SECURITY.md)
3. Check pipeline execution logs
4. Consult [Terraform documentation](https://www.terraform.io/docs)

## 📄 License

[Your License Here]

## 🤝 Contributing

1. Create feature branch
2. Make changes with tests
3. Submit pull request
4. Get approval from team
5. Merge and deploy

## 📞 Contact

Infrastructure Team: infrastructure@company.com

---

**Last Updated:** January 2026  
**Terraform Version:** 1.9.0  
**Azure Provider:** 4.35.0+
