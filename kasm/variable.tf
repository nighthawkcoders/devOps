variable "kasm_ec2" {

  type = list(string)


  default = [
    "Kasm1.ncs.com",
    "Kasm2.ncs.com",
    "Kasm3.ncs.com"
  ]
}
