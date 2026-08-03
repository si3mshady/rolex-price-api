# ==============================================================================
# Module: CloudWatch
# Description: Manages log groups, metric alarms, and monitoring settings.
# ==============================================================================

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = var.log_group_name
  retention_in_days = var.retention_in_days

  tags = var.tags
}
