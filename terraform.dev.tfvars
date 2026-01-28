# Development Environment Variables
# This file contains environment-specific configuration for dev

# Azure Resource Group
resource_group_name = "dev-rg"
location            = "eastus"

# Network Configuration
vnet_name           = "dev-vnet"
vnet_address_space  = ["10.0.0.0/16"]

# Subnets
subnets = [
  {
    name             = "dev-subnet-1"
    address_prefixes = ["10.0.1.0/24"]
  },
  {
    name             = "dev-subnet-2"
    address_prefixes = ["10.0.2.0/24"]
  }
]

# VM Configuration
vm_name           = "dev-vm"
vm_size           = "Standard_B2s"
admin_username    = "azureuser"
os_disk_size_gb   = 30

# Environment Tags
environment = "dev"
project     = "terraform-learning"
owner       = "devteam"

# Cost Management
enable_monitoring = true
backup_enabled    = false
