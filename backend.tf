terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.35.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "terraform"
    storage_account_name = "tfstateforterrform"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}