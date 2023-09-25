terraform {
  required_version = "1.3.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.17.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
#testandooooo
resource "aws_instance" "web" {
  ami           = var.instance_ami
  instance_type = var.instance_type

  tags = {
    Name = "HelloWorld"
  }
}
