location      = "centralindia"
resource_group_name          = "Gmail"
vnet_address_spaces = ["10.0.0.0/16", "10.1.0.0/16"]
subnet_prefixes     = ["10.0.0.0/24", "10.0.1.0/24", "10.1.0.0/24", "10.1.1.0/24"]


tags = {
  Environment = "dev"
  Dept        = "financial"
}
