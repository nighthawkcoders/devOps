#
# change subdomain, domain_2ld, domain_tag to meet project needs
#

# instance or system identifier
variable "subdomain" {
  description = "List of Kasm EC2 instances"
  type        = list(string)
  default     = ["Kasm2", "Kasm3", "Kasm4"]
}

# domain marketing name 
variable "domain_2ld" {
  description = "Domain second level description"
  type        = string
  default     = "nighthawkcodingsociety"
}

# shorter name used in AWS tags, use default = "domain_2ld" if not needed
variable "domain_tag" {
  description = "Domain name for tags"
  type        = string
  default     = "ncs.com"
}

#
# derived names after here, do not change
#

# full domain name
variable "domain" {
  description = "Full domain name"
  type        = string
  default     = "${domain_2ld}.com"
}

# derived list for EC2 instances
variable "kasm_ec2" {
  description = "List of Kasm EC2 instances"
  type        = list(string)
  # list comprehension
  default     = [for sub in var.subdomain : "${sub}.${var.domain_tag}"]
}

# derived list for URLs
variable "kasm_domain" {
  description = "List of Kasm URLs"
  type        = list(string)
  default     = [for sub in var.subdomain : "${sub}.${var.domain}"]
}
