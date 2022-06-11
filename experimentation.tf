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
resource "aws_instance" "deep_learning_ec2" {
    ami = "ami-00ab1614b421d5575"
    instance_type = "p2.xlarge"
    ebs_block_device {
      device_name = "/dev/xvda"
      volume_size = "100"
      volume_type = "gp3"
    }
}