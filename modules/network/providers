terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>4.0"
    }
  }
}

provider "azurerm" {
  features {
 virtual_machine {
      detach_implicit_data_disk_on_deletion = false
      delete_os_disk_on_deletion            = true
   }   
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }

  subscription_id = "e94bdd49-97a8-440d-bf40-10569cc9409e"
  tenant_id       = "9a998602-7371-4737-98c5-cd71dd4a9e9b"
  client_id       = "1ce6cbf4-1110-4ec8-b98d-80088bde1942"
  client_secret   = var.client_secret
}
