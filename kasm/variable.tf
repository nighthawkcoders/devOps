#
# change subdomain, domain_2ld, domain_tag to meet project needs
#

variable "subdomain" {
  description = "List of Kasm EC2 instances"
  type        = list(string)
  default     = ["Kasm2", "Kasm3", "Kasm4"]
}

variable "domain_tag" {
  description = "Abbreviated domain name for tags"
  type        = string
  default     = "ncs.com"
}

# full domain name
variable "domain" {
  description = "Full domain name"
  type        = string
  default     = "nighthawkcodingsociety.com"
}

# shorter name used in AWS tags, use default = "domain_2ld" if not needed
variable "email" {
  description = "Certbot and public facing email"
  type        = string
  default     = "nighthawkcodingsociety@gmail.com"
}


#
# derived names after here, do not change
#

# derived list for EC2 instances
variable "kasm_ec2" {
  description = "List of Kasm EC2 instances"
  type        = list(string)
  default     = []
}
