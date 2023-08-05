variable "instances_prefix" {
  description = "EC2 instance name prefix"
  type        = string
  default     = "Kasm"  # Used as prefix in naming
}

variable "instances_start" {
  description = "Starting EC2 instance number"
  type        = number
  default     = 0  # Adjust starting integer as needed
}

variable "instances_count" {
  description = "Number of EC2 instances"
  type        = number
  default     = 1  # Adjust number of instances as needed
}

variable "domain" {
  description = "Full domain name"
  type        = string
  default     = "nighthawkcodingsociety.com"
}

variable "domain_tag" {
  description = "Abbreviated domain name for tags"
  type        = string
  default     = "ncs.com"  # Used for resource names
}

# shorter name used in AWS tags, use default = "domain_2ld" if not needed
variable "email" {
  description = "Certbot and public facing email"
  type        = string
  default     = "nighthawkcodingsociety@gmail.com" # Used in System install
}

variable "hosted_zone" {
  description = "AWS Route 53 Hosted Zone that maps to Registered Domain"
  type        = string
  default     = "Z06240873BALIBO9T07NB"
}

variable "key_pair" {
  description = "Name of of Key pair for login"
  type        = string
  default     = "kasm" 
}
