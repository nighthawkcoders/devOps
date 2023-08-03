# network.tf

# define route 53 zone
resource "aws_route53_zone" "${var.domain_2ld}" {
  name = "${var.domain}"
}

# create route 53 A records
resource "aws_route53_record" "kasm_dns" {
  # repeat for each kasm ec2
  count = length(var.subdomain)

  # set zone
  zone_id = aws_route53_zone.nighthawkcodingsociety.id
  # extracts subdomain from each kasm_ec2, the part before the first dot
  name    = "${var.subdomain[count.index]}"
  type    = "A"
  ttl     = "300"
  # sets IP, count.index obtains kasm.eip resource (elastic ip)
  records = [aws_eip.kasm_eip[count.index].public_ip]
}
