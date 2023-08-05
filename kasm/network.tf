# network.tf

# create Elastic IP's
resource "aws_eip" "kasm_eip" {
  count = length(aws_instance.kasm_server) # aws_eip iterator

  # assign Meta data
  tags = {
    Name   = aws_instance.kasm_server[count.index].tags["Name"]
  }

  # create reference to a EC2 instance, see ec2.tf
  instance = aws_instance.kasm_server[count.index].id
}

# create DNS A records in zone_id
resource "aws_route53_record" "kasm_dns" {
  count = length(aws_instance.kasm_server) # aws_route53_record iterator

  zone_id = var.hosted_zone  # set Hosted Zone ID, see variable.tf
  name    = aws_instance.kasm_server[count.index].tags["Domain"] # set from EC2 meta data
  type    = "A"
  ttl     = "300"
  records = [aws_eip.kasm_eip[count.index].public_ip] # set from Elastic IP public address
}
