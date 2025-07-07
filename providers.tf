terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.35.0"
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

  subscription_id = "f4ffefe1-d689-4059-969c-ccc73e2a11d4"
  tenant_id       = "4cef0d84-84d6-4ed0-8abe-773b015bcf99"
  client_id       = "0dfa47eb-cb5f-4a19-8edc-192901b73c82"
  client_secret   = var.client_secret
}

