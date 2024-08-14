provider "aws" {
  region = var.aws_region
}

variable "env_name" {
  description = "Environment name"
}

data "aws_ecr_repository" "rag_ecr" {
  name = "lambda-rag-ecr"
}

data "aws_ecr_repository" "rag_ecr_data_repo" {
  name = "rag-lambda-data-repo"
}

//lambda function data response generator
resource "aws_lambda_function" "rag_res_data_gen" {
  function_name = "rag-res-data-gen"
  memory_size = 500
  role          = aws_iam_role.rag_res_gen.arn
  timeout       = 5
  image_uri = "${data.aws_ecr_repository.rag_ecr_data_repo.repository_url}:${var.env_name}"
  package_type = "Image"

    environment {
        variables = {
        OPENAI_API_KEY = var.openai_api_key
        PINECONE_API_KEY = var.pinecone_api_key
        PINECONE_INDEX_NAME = var.pinecone_index_name
        GOOGLE_APPLICATION_CREDENTIALS = var.google_application_credentials
        }
    }
}

//lambda function data response
resource "aws_lambda_function" "rag_res_gen" {
  function_name = "rag-res-gen"
  memory_size = 500
  role          = aws_iam_role.rag_res_gen.arn
  timeout       = 5
  image_uri = "${data.aws_ecr_repository.rag_ecr.repository_url}:${var.env_name}"
  package_type = "Image"

    environment {
        variables = {
        OPENAI_API_KEY = var.openai_api_key
        PINECONE_API_KEY = var.pinecone_api_key
        PINECONE_INDEX_NAME = var.pinecone_index_name
        }
    }
}

//iam role
resource "aws_iam_role" "rag_res_gen" {
  name = "rag-res-gen"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rag_res_gen" {
  role       = aws_iam_role.rag_res_gen.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

//api gateway
resource "aws_apigatewayv2_api" "rag_res_gen" {
  name          = "rag-res-gen"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "rag_res_gen" {
  api_id = aws_apigatewayv2_api.rag_res_gen.id
  name   = "$default"
    auto_deploy = true
}

resource "aws_apigatewayv2_integration" "rag_res_gen" {
  api_id = aws_apigatewayv2_api.rag_res_gen.id
  integration_type = "AWS_PROXY"
  integration_method = "POST"
  integration_uri = aws_lambda_function.rag_res_gen.invoke_arn
}

resource "aws_apigatewayv2_route" "rag_res_gen" {
  api_id = aws_apigatewayv2_api.rag_res_gen.id
  route_key = "POST /prompt"
    target = "integrations/${aws_apigatewayv2_integration.rag_res_gen.id}"
}

resource "aws_apigatewayv2_integration" "rag_data_res_gen" {
  api_id = aws_apigatewayv2_api.rag_res_gen.id
  integration_type = "AWS_PROXY"
  integration_method = "POST"
  integration_uri = aws_lambda_function.rag_res_data_gen.invoke_arn
}

resource "aws_apigatewayv2_route" "rag_data_res_gen" {
  api_id = aws_apigatewayv2_api.rag_res_gen.id
  route_key = "POST /data"
    target = "integrations/${aws_apigatewayv2_integration.rag_data_res_gen.id}"
}

resource "aws_lambda_permission" "rag_res_gen" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rag_res_gen.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.rag_res_gen.execution_arn}/*/*"
}
