# network.tf

# define route 53 zone
resource "aws_route53_zone" "nighthawkcodingsociety" {
  name = "nighthawkcodingsociety.com."
}

# create route 53 A records
resource "aws_route53_record" "kasm_dns" {
  # repeat for each kasm ec2
  count = length(var.kasm_ec2)

  # set zone
  zone_id = aws_route53_zone.nighthawkcodingsociety.id
  # extracts subdomain from each kasm_ec2, the part before the first dot
  name    = replace(var.kasm_ec2[count.index], "\\..*$", "")
  type    = "A"
  ttl     = "300"
  # sets IP to EC2 instance's Elastic IP
  records = [aws_eip.kasm_eip[count.index].public_ip]
}
