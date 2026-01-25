/* variable "resource_group_location" {
  type        = string
  default     = "eastus"
 description = "Location of the resource group."
} */

variable "resource_group_name" {
  type        = string
  default     = "RGDefault"
  description = "Location of the resource group."
}

variable "vm_count" {
  description = "Number of VMs to create"
  type        = number
  default     = 2
}

variable "resource_group_name_prefix" {
  type        = string
  default     = "rg2"
  description = "Prefix of the resource group name that's combined with a random ID so the name is unique in your Azure subscription."
}

variable "client_secret" { 
  description = "The client secret for the service principal"
  type        = string
  sensitive   = true 
}

variable "tags" {
  description = "A map of tags to assign to the resource group"
  type        = map(string) 
  default = {
    Environment = "tag1"
    Dept        = "tag2"
  } 
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
variable "vm_size" {
  description = "Size of the VM"
  type        = string
}

variable "vm_os" {
  description = "OS version for the VM"
  type        = string
}

variable "hostname" {
  description = "name for vm"
  type = string
}

variable "location" {
  type        = string
  default     = "eastus"
  description = "Location of the resources."
} 

variable "vnet_address_spaces" {
  description = "List of VNet address spaces"
  type        = list(string)
 }

variable "subnet_prefixes" {
   description = "List of subnet prefixes"
   type        = list(string)
 }

#variable "subnet_ids" {
  #description = "The subnet IDs for the network interfaces"
  #type        = list(string)
#}

#variable "vm_subnet_id" {
  #description = "The subnet IDs for the network interfaces"
  #type        = string
#}
