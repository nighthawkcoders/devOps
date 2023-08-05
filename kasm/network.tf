# network.tf

resource "aws_route53_record" "kasm_dns" {
  count = length(aws_instance.kasm_server)

  zone_id = "Z06240873BALIBO9T07NB"  # Use the existing Hosted Zone ID here
  name    = aws_instance.kasm_server[count.index].tags["Domain"]
  type    = "A"
  ttl     = "300"
  records = [aws_eip.kasm_eip[count.index].public_ip]
}
