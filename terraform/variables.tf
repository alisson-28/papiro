variable "aws_region" {
    type = string
    description = "" 
}

variable "environment" {
  type        = string
  description = ""
}

variable "instance_type" {
    type = string
    description = ""
}

variable "instance_ami" {
    type = string
    description = ""
}

variable "instance_tags" {
    type = map(string)
    description = ""
    default = {
        Name = "CENTOS"
        Project = "Curso aws com terraform"
    }
}