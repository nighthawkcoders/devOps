# network.tf

# define route 53 zone
resource "aws_route53_zone" "nighthawkcodingsociety" {
  name = "${var.domain}"
}

# create route 53 A records
resource "aws_route53_record" "kasm_dns" {
  # repeat for each subdomain and relate  kasm_eip 
  count = length(var.subdomain)

  # set zone
  zone_id = aws_route53_zone.nighthawkcodingsociety.id
  # set subdomain using index
  name    = "${var.subdomain[count.index]}"
  type    = "A"
  ttl     = "300"
  # sets IP, uses index of kasm.eip (elastic ip)
  records = [aws_eip.kasm_eip[count.index].public_ip]
}
