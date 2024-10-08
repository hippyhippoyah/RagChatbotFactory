# RAG Chatbot Factory

A tool for generating chatbot using Retrieval Augmented Generation from pinecone. Containerized and auto-deployment to aws with terraform. 


## Overview

This project leverages the capabilities of Pinecone, LangChain, Terraform, AWS, Docker, and OpenAI to create a robust response generator. The tool utilizes large language models to produce accurate and context-aware responses.

## Architecture

* **Pinecone**: Used for vector database management and similarity search.
* **LangChain**: Employs language models for response generation and processing.
* **Terraform**: Manages infrastructure as code for scalable deployment.
* **AWS**: Provides cloud services for hosting and computation.
* **Docker**: Enables containerization for easy deployment and management.
* **OpenAI**: Powers language models for response generation.

## Prerequisites

* **Terraform**: [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) configuration files (HCL) for infrastructure setup
* **Tokens**: [link](https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-login)
* **VariableSet** [link](https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-create-variable-set)
* **AWS**: AWS account and credentials for cloud services
* **Pinecone**: Pinecone account and index creation
* **OPENAIKEY** In environment variables
* **Environment Variables**: Export the following environment variables:
	+ `TF_CLOUD_ORGANIZATION`
	+ `TF_VAR_openai_api_key`
	+ `TF_VAR_pinecone_api_key`
	+ `TF_VAR_pinecone_index_name`
	+ `TF_VAR_env_name`

## Features

* **Context-aware responses**: Generates responses based on input context.
* **Scalable infrastructure**: Handles high traffic with ease.
* **Easy deployment**: Utilizes Docker and Terraform for streamlined deployment.
* **Endpoints**: Using aws API GATEWAY, new endpoints to prompt chatbot and to update data. 

## Setup

1. Clone the repository: `git clone https://github.com/your-repo/rag-response-generator.git`
2. Create private ECR repositories rag-res-data-gen, and `rag-res-gen`
3. cd into data lambda and run `make docker/push TAG=dev`
4. cd into rag lambda and run `make docker/push TAG=dev`
5. return to root directory and run (may have to login to terraform before) `terraform apply`

## Issues
Any issues are likely do to the Prerequisites setup. 

## Contributing

Contributions are welcome! Please fork with your contribution!

## It is still a WIP (sorry this readme might not be the best)

Important items such as moving out of environment variables and putting into AWS secrets is important for actual deployment. This is just a working basic product. 

AWS does not support multithreading to Pinecone.from_documents does not work currently in lambda. 