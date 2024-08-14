variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "us-east-1"
}

variable "openai_api_key" {
  description = "openai api key."

  type    = string
  default = "1234567890"
}

variable "pinecone_api_key" {
  description = "pinecone api key."

    type    = string
    default = "1234567890"
}

variable "google_application_credentials" {
  description = "google application credentials."

  type    = string
  default = ""
}

variable "pinecone_index_name" {
  description = "pinecone index name."

  type  =  string
  default = "rag-res-gen"
}