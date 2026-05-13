output "vnet_ids" {
  description = "The IDs of the VNets"
  value       = azurerm_virtual_network.vnet.*.id
}

output "subnet_ids" {
  description = "The IDs of the subnets"
  value       = azurerm_subnet.subnet.*.id
}

output "vm_subnet1_id" {
  description = "The ID of the subnet VM-subnet1"
  value       = element(azurerm_subnet.subnet.*.id, 3)  # Assuming VM-subnet1 is the first subnet
}

