resource "azurerm_virtual_network" "vnet" {
  count               = 2
  name                = "vnet${count.index + 1}"
  address_space       = [var.vnet_address_spaces[count.index]]
  location            = var.location
  resource_group_name = var.resource_group_name
  tags = var.tags
}

resource "azurerm_subnet" "subnet" {
  count                = 4
  name                 = "${element(["VM", "DB"], count.index % 2)}-subnet${floor(count.index / 2) + 1}"
  resource_group_name  = var.resource_group_name
  virtual_network_name = element(azurerm_virtual_network.vnet.*.name, floor(count.index / 2))
  address_prefixes     = [var.subnet_prefixes[count.index]]
  depends_on = [azurerm_virtual_network.vnet]
}
