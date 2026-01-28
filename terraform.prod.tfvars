# Production Environment Variables
# This file contains environment-specific configuration for prod
# ⚠️  Handle with care - these settings affect production infrastructure

# Azure Resource Group
resource_group_name = "prod-rg"
location            = "eastus"

# Network Configuration
vnet_name           = "prod-vnet"
vnet_address_space  = ["10.2.0.0/16"]

# Subnets
subnets = [
  {
    name             = "prod-subnet-1"
    address_prefixes = ["10.2.1.0/24"]
  },
  {
    name             = "prod-subnet-2"
    address_prefixes = ["10.2.2.0/24"]
  },
  {
    name             = "prod-subnet-3"
    address_prefixes = ["10.2.3.0/24"]
  }
]

# VM Configuration
vm_name           = "prod-vm"
vm_size           = "Standard_D2s_v3"
admin_username    = "azureuser"
os_disk_size_gb   = 100

# Environment Tags
environment = "prod"
project     = "terraform-learning"
owner       = "devteam"

# Cost Management & Compliance
enable_monitoring = true
backup_enabled    = true
enable_encryption = true
