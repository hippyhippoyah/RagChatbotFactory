
output "lambda_function_name" {
  value = aws_lambda_function.rag_res_gen.function_name
}

output "base_url" {
  value = aws_apigatewayv2_stage.rag_res_gen.invoke_url
}