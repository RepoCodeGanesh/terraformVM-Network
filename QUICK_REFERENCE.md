# Quick Reference Card

## 🚀 Quick Start Commands

### Initialize Terraform
```bash
terraform init \
  -backend-config="resource_group_name=terraform" \
  -backend-config="storage_account_name=tfstateforterrform" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=prod.terraform.tfstate"
```

### Local Development
```bash
terraform validate      # Validate syntax
terraform fmt          # Format code
terraform plan         # Review changes
terraform apply        # Deploy
terraform destroy      # Cleanup
```

### View State
```bash
terraform state list           # List resources
terraform state show <resource> # Show resource details
terraform state pull          # Download state
```

---

## 📋 Pipeline Quick Reference

### Pipeline Stages
| Stage | Duration | Trigger | Action |
|-------|----------|---------|--------|
| Validate | 2-3 min | Automatic | Check code quality |
| Plan | 5-10 min | Automatic | Generate plan |
| Review | Manual | Manual | Approve changes |
| Apply | 10-20 min | After approval | Deploy infrastructure |
| Validate | 2-3 min | Automatic | Verify deployment |
| Cleanup | Manual | On demand | Destroy resources |

### Trigger Pipeline
1. Commit code to repository
2. Push to main branch
3. Pipeline triggers automatically
4. Review plan in logs
5. Approve manual step
6. Monitor apply stage

---

## 🔐 Variable Group Values

```
BACKEND_CONTAINER       = tfstate
BACKEND_KEY            = prod.terraform.tfstate
BACKEND_RESOURCE_GROUP = terraform
BACKEND_STORAGE_ACCOUNT= tfstateforterrform
CLIENT_ID              = 0dfa47eb-cb5f-4a19-8edc-192901b73c82
SUBSCRIPTION_ID        = f4ffefe1-d689-4059-969c-ccc73e2a11d4
TENANT_ID              = 4cef0d84-84d6-4ed0-8abe-773b015bcf99
```
(CLIENT_SECRET & BACKEND_STORAGE_KEY marked as secret)

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `azure-pipelines.yml` | CI/CD pipeline definition |
| `terraform.tfvars` | Variable values (secret) |
| `.gitignore` | Files to exclude from git |
| `README.md` | Project overview |
| `PIPELINE_SETUP.md` | Pipeline configuration |
| `DEPLOYMENT_GUIDE.md` | Deployment instructions |
| `SECURITY.md` | Security guidelines |

---

## 🔧 Common Tasks

### Deploy Infrastructure
```bash
# 1. Plan
terraform plan -out=tfplan

# 2. Review plan output

# 3. Apply
terraform apply tfplan
```

### Check Resource Status
```bash
# List all resources
terraform state list

# Show specific resource
terraform state show azurerm_resource_group.main

# View outputs
terraform output
```

### Update Infrastructure
```bash
# Edit variables
nano terraform.tfvars

# Plan changes
terraform plan

# Review changes carefully

# Apply updates
terraform apply
```

### Backup State
```bash
# Create backup
terraform state pull > backup.tfstate

# Restore from backup
terraform state push backup.tfstate
```

---

## 🚨 Troubleshooting

### State Lock Error
```bash
terraform force-unlock <lock-id>
```

### Authentication Error
```bash
az login
az account set --subscription <subscription-id>
```

### Plan Generation Error
```bash
terraform refresh
terraform plan
```

### Backend Configuration Error
```bash
# Verify storage account
az storage account show \
  --name tfstateforterrform \
  --resource-group terraform
```

---

## 📊 Monitoring

### Check Pipeline Status
1. Go to **Pipelines** → Select pipeline
2. Click on latest run
3. Review stage results
4. Check logs for errors

### Monitor Azure Resources
1. Go to **Resource Groups**
2. Select your resource group
3. View deployments
4. Check Activity Log

### Check Costs
1. Go to **Cost Management + Billing**
2. Select **Cost analysis**
3. Filter by resource group
4. Review spending trends

---

## 🔄 Git Workflow

### Create Feature Branch
```bash
git checkout -b feature/my-changes
git add .
git commit -m "Add feature"
git push origin feature/my-changes
```

### Create Pull Request
1. Push feature branch
2. Go to repository
3. Click **Create Pull Request**
4. Add description
5. Submit for review

### Merge to Main
```bash
git checkout main
git pull origin main
git merge feature/my-changes
git push origin main
# Pipeline triggers automatically
```

---

## 📚 Documentation Map

```
START HERE
    ↓
README.md ─→ Project overview & quick start
    ↓
PIPELINE_SETUP.md ─→ Configure Azure DevOps
    ↓
DEPLOYMENT_GUIDE.md ─→ Deploy infrastructure
    ├→ SECURITY.md ─→ Security guidelines
    ├→ OPERATIONS_GUIDE.md ─→ Daily operations
    └→ PIPELINE_CONFIG_REFERENCE.md ─→ Technical details
```

---

## 🎯 Success Criteria

### Pipeline Should:
✅ Run on every commit  
✅ Validate code automatically  
✅ Generate accurate plans  
✅ Require manual approval  
✅ Deploy without errors  
✅ Verify deployment success  
✅ Maintain audit trail  

### Infrastructure Should:
✅ Deploy to correct region  
✅ Create all resources  
✅ Apply correct tags  
✅ Configure networking properly  
✅ Show in Azure Portal  
✅ Be destroyable cleanly  

---

## 📞 Getting Help

### Check These First
1. Pipeline logs: `Pipelines` → Run → Stage logs
2. Error messages: Copy full error text
3. Azure Portal: Verify resource deployment
4. Documentation: Search the markdown files

### Escalation Path
1. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Check [SECURITY.md](SECURITY.md)
3. Review [PIPELINE_CONFIG_REFERENCE.md](PIPELINE_CONFIG_REFERENCE.md)
4. Contact Infrastructure Team
5. Open Azure Support ticket

---

## 🔑 Key Contacts

| Role | Contact | Responsibility |
|------|---------|-----------------|
| DevOps Lead | [Contact] | Pipeline maintenance |
| Infrastructure | [Contact] | Resource approval |
| Security | [Contact] | Security review |
| On-Call | [Contact] | Incident response |

---

## 📅 Maintenance Schedule

| Frequency | Task | Checklist |
|-----------|------|-----------|
| Daily | Monitor pipeline | [ ] No failures |
| Weekly | Review costs | [ ] Within budget |
| Monthly | Security audit | [ ] No issues |
| Quarterly | Version upgrade | [ ] Plan updated |
| Annual | DR drill | [ ] Procedures tested |

---

## 💾 Critical Values (Reference Only)

Service Connection: `azuredevops-azure`  
Variable Group: `Terraform-Secrets`  
Storage Account: `tfstateforterrform`  
State Container: `tfstate`  
State Key: `prod.terraform.tfstate`  
Resource Group: `terraform`  
Subscription: `f4ffefe1-d689-4059-969c-ccc73e2a11d4`  
Tenant: `4cef0d84-84d6-4ed0-8abe-773b015bcf99`  

---

## ✨ Pro Tips

1. **Always review the plan** before approval
2. **Never commit** `terraform.tfvars` or secrets
3. **Use variables** for all customizable values
4. **Enable state locking** to prevent conflicts
5. **Backup state regularly** for disaster recovery
6. **Tag all resources** for cost tracking
7. **Monitor costs** monthly
8. **Test in non-prod** first
9. **Document changes** in commit messages
10. **Keep team informed** of major changes

---

## ⚡ Emergency Procedures

### Pipeline Hanging
1. Check approval queue
2. Manually reject if timeout
3. Restart pipeline

### Failed Deployment
1. Check logs for error
2. Fix issue in code
3. Re-run pipeline

### Corruption in State
1. Restore from backup
2. Verify resources manually
3. `terraform refresh`

### Security Breach
1. Revoke credentials immediately
2. Rotate service principal
3. Review audit logs
4. Notify security team

---

*Last Updated: January 2026*  
*Bookmark this page for quick reference!*
