terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

#open ec2 instance
resource "aws_instance" "deep_learning" {
    ami = "ami-00ab1614b421d5575"
    instance_type = "p2.xlarge"
    volume_size = "100"
    volume_type = "gp3"
}