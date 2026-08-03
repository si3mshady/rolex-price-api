output "api_id" {
  description = "ID of the HTTP API Gateway"
  value       = aws_apigatewayv2_api.http_api.id
}

output "api_endpoint" {
  description = "HTTP API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}

output "api_arn" {
  description = "ARN of the HTTP API Gateway"
  value       = aws_apigatewayv2_api.http_api.arn
}

output "stage_invoke_url" {
  description = "Stage invocation URL"
  value       = aws_apigatewayv2_stage.default.invoke_url
}
