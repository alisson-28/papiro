variable "aws_region" {
    type = string
    description = ""
    default = "us-east-1"  
}

variable "instance_type" {
    type = string
    description = ""
    default = "t2.micro"
}

variable "instance_ami" {
    type = string
    description = ""
    default = "ami-03a6eaae9938c858c"
}

variable "instance_tags" {
    type = map(string)
    description = ""
    default = {
        Name = "CENTOS"
        Project = "Curso aws com terraform"
    }
}