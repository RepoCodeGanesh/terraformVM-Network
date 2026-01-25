output "vm_private_ip" {
  description = "The private IP address of the VM"
  value       = azurerm_network_interface.nic[0].ip_configuration[0].private_ip_address
}

output "vm_ids" {
  description = "The IDs of all created VMs"
  value       = [for vm in azurerm_virtual_machine.vm : vm.id]
}

output "vm_names" {
  description = "The names of all created VMs"
  value       = [for vm in azurerm_virtual_machine.vm : vm.name]
}

output "vm_private_ips" {
  description = "The private IP addresses of all created VMs"
  value       = [for idx in range(length(azurerm_network_interface.nic)) : azurerm_network_interface.nic[idx].ip_configuration[0].private_ip_address]
}