# Staging Environment Variables
# This file contains environment-specific configuration for staging

# Azure Resource Group
resource_group_name = "staging-rg"
location            = "eastus"

# Network Configuration
vnet_name           = "staging-vnet"
vnet_address_space  = ["10.1.0.0/16"]

# Subnets
subnets = [
  {
    name             = "staging-subnet-1"
    address_prefixes = ["10.1.1.0/24"]
  },
  {
    name             = "staging-subnet-2"
    address_prefixes = ["10.1.2.0/24"]
  }
]

# VM Configuration
vm_name           = "staging-vm"
vm_size           = "Standard_B2s"
admin_username    = "azureuser"
os_disk_size_gb   = 50

# Environment Tags
environment = "staging"
project     = "terraform-learning"
owner       = "devteam"

# Cost Management
enable_monitoring = true
backup_enabled    = true
