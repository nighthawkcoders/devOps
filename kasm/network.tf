# network.tf

# define route 53 zone
resource "aws_route53_zone" "nighthawkcodingsociety" {
  name = "${var.domain}"
}

# create route 53 A records
resource "aws_route53_record" "kasm_dns" {
  # repeat for each subdomain and relate  kasm_eip 
  for_each = aws_instance.kasm_server

  # set zone
  zone_id = aws_route53_zone.nighthawkcodingsociety.id
  # set subdomain using index
  name    = each.value.tags["Domain"] # Use the "Domain" tag as the subdomain
  type    = "A"
  ttl     = "300"
  # sets IP, uses index of kasm.eip (elastic ip)
  records = [aws_eip.kasm_eip[each.key].public_ip] # Use each.key to index the EIPs
}
