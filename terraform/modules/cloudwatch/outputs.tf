output "log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda_logs.arn
}

output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

output "dashboard_name" {
  description = "Name of the CloudWatch dashboard"
  value       = length(aws_cloudwatch_dashboard.operational) > 0 ? aws_cloudwatch_dashboard.operational[0].dashboard_name : ""
}

output "lambda_errors_alarm_arn" {
  description = "ARN of the Lambda errors metric alarm"
  value       = length(aws_cloudwatch_metric_alarm.lambda_errors) > 0 ? aws_cloudwatch_metric_alarm.lambda_errors[0].arn : ""
}
