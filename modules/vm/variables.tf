variable "resource_group_name" {
  type        = string
  default     = "RGDeafult"
  description = "Location of the resource group."
}

variable "resource_group_location" {
  type        = string
  default     = "eastus"
  description = "Location of the resource group."
}

variable "location" {
  description = "Location of the resources"
  type        = string
}

variable "vm_count" {
  description = "Number of VMs to create"
  type        = number
}

variable "vm_size" {
  description = "Size of the VM"
  type        = string
}

variable "vm_os" {
  description = "OS version for the VM"
  type        = string
}

variable "admin_username" {
  description = "Admin username for the VM"
  type        = string
}

variable "admin_password" {
  description = "Admin password for the VM"
  type        = string
  sensitive   = true
}

variable "tags" {
  description = "A map of tags to assign to the resource group"
  type        = map(string)
}

variable "hostname" {
  description = "name for vm"
  type = string
}

variable "subnet_ids" {
  description = "The subnet IDs for the network interfaces"
  type        = list(string)
}
variable "vm_subnet_id"{ # Changed from subnet_ids to vm_subnet_id 
  description = "The ID of the subnet for the VM NICs"
  type = string
}
