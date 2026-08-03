output "function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.fastapi_app.arn
}

output "function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.fastapi_app.function_name
}

output "invoke_arn" {
  description = "Invoke ARN of the Lambda function for API Gateway integration"
  value       = aws_lambda_function.fastapi_app.invoke_arn
}
