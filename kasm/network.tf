# network.tf

# Define route 53 zone
resource "aws_route53_zone" "nighthawkcodingsociety" {
  name = var.domain
}

# Create route 53 A records
resource "aws_route53_record" "kasm_dns" {
  count = length(aws_instance.kasm_server)

  zone_id = aws_route53_zone.nighthawkcodingsociety.id
  name    = aws_instance.kasm_server[count.index].tags["Domain"]
  type    = "A"
  ttl     = "300"
  records = [aws_eip.kasm_eip[count.index].public_ip]
}
