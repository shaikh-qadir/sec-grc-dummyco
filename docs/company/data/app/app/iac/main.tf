terraform { required_version = ">= 1.5.0" }
provider "aws" { region = "us-east-1" }

# ❌ Public S3 without encryption (Checkov/tfsec will flag)
resource "aws_s3_bucket" "public_bucket" {
  bucket = "dummyco-public-demo-bucket"
  acl    = "public-read"
  tags = { Name = "public-demo" } # missing owner/env
}

# ❌ Open SSH to the world
resource "aws_security_group" "open_ssh" {
  name        = "dc-open-ssh"
  description = "demo"
  ingress { from_port = 22 to_port = 22 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0  to_port = 0  protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
}

# ❌ Wildcard IAM policy
resource "aws_iam_user" "legacy_user" { name = "legacy.user" }
resource "aws_iam_user_policy" "legacy_user_policy" {
  name = "legacy-user-policy"
  user = aws_iam_user.legacy_user.name
  policy = <<EOF
{ "Version":"2012-10-17", "Statement":[{ "Effect":"Allow", "Action":"*", "Resource":"*" }] }
EOF
}
