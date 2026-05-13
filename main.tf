resource "azurerm_resource_group" "rg" {
  location = var.location
  name     = var.resource_group_name
  tags     = var.tags
}

module "network" {
  source              = "./modules/network"
  resource_group_name = var.resource_group_name
  location            = var.location
  vnet_address_spaces = var.vnet_address_spaces
  subnet_prefixes     = var.subnet_prefixes
  tags                = var.tags
  depends_on          = [azurerm_resource_group.rg]
}

module "vm" {
  source              = "./modules/vm"
  resource_group_name = azurerm_resource_group.rg.name
  # resource_group_location = var.resource_group_location
  location       = var.location
  vm_os          = var.vm_os
  hostname       = var.hostname
  vm_count       = var.vm_count
  vm_size        = var.vm_size
  admin_username = var.admin_username
  admin_password = var.admin_password
  vm_subnet_id   = module.network.vm_subnet1_id # Pass the output from the network module
  subnet_ids     = module.network.subnet_ids    # Pass the output from the network module
  tags           = var.tags
}
