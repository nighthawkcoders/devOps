# variable.tf

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

variable "kasm_instances" {
  description = "List of Kasm EC2 instances along with their corresponding domains"
  type = list(map(string))
  default = [
    {
      ec2_Name   = "Kasm2.ncs.com"
      ec2_Domain = "kasm2.nighthawkcodingsociety.com"
    },
    {
      ec2_Name   = "Kasm3.ncs.com"
      ec2_Domain = "kasm3.nighthawkcodingsociety.com"
    },
    {
      ec2_Name   = "Kasm4.ncs.com"
      ec2_Domain = "kasm4.nighthawkcodingsociety.com"
    },
    # Add more instances as needed
  ]
}