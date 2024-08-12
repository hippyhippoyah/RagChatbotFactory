terraform {

  cloud {
    workspaces {
      name = "rag-res-gen"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.38.0"
    }
  }

  required_version = "~> 1.2"
}
