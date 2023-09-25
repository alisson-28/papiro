resource "aws_s3_bucket" "this" {

  bucket = "${random_pet.bucket.id}-${var.environment}"

  tags = {
    Service     = "Curso terraform"
    ManagedBy   = "Terraform"
    Environment = var.environment
    Owner       = "Alisson"
  }
}

resource "aws_s3_bucket" "manual" {

    bucket = "meubuckets3docursoterraform12"
      tags = {
        Criado    = "14/01/2021"
        Importado = "23/01/2021"
        ManagedBy = "Terraform"
  }
}

data "aws_caller_identity" "current" {} #acessar o meu ID de conta AWS

resource "aws_s3_bucket" "remote-state" {
    bucket = "tfstate-${data.aws_caller_identity.current.account_id}"


      tags = {
    Description = "Stores terraform remote state files"
    ManagedBy   = "Terraform"
    Owner       = "Cleber Gasparoto"
    CreatedAt   = "2023-09-25"
  }

}

resource "aws_s3_bucket_versioning" "versioning_example" { #habilitando o versionamento do backup remote-state
  bucket = aws_s3_bucket.remote-state.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "remote_state_bucket" {
  value = aws_s3_bucket.remote-state.bucket
}

output "remote_state_bucket_arn" {
  value = aws_s3_bucket.remote-state.arn
}