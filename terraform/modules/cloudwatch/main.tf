# ==============================================================================
# Module: CloudWatch
# Description: Manages log groups, CloudWatch Dashboard, and Metric Alarms.
# ==============================================================================

# 1. Lambda Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = var.log_group_name
  retention_in_days = var.retention_in_days

  tags = var.tags
}

# 2. CloudWatch Metric Alarms (Lambda Errors & Throttles)
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  count               = var.function_name != "" ? 1 : 0
  alarm_name          = "${var.function_name}-errors-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alarm triggered when Lambda function encounters 1 or more errors."
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = var.function_name
  }

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  count               = var.function_name != "" ? 1 : 0
  alarm_name          = "${var.function_name}-throttles-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alarm triggered when Lambda function execution is throttled."
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = var.function_name
  }

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  count               = var.function_name != "" ? 1 : 0
  alarm_name          = "${var.function_name}-high-latency-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 300
  extended_statistic  = "p95"
  threshold           = 1000
  alarm_description   = "Alarm triggered when Lambda p95 duration exceeds 1000ms."
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = var.function_name
  }

  tags = var.tags
}

# 3. Operational CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "operational" {
  count          = var.function_name != "" ? 1 : 0
  dashboard_name = var.dashboard_name

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", var.function_name, { stat = "Sum", period = 60 }],
            [".", "Errors", ".", ".", { stat = "Sum", period = 60, color = "#d62728" }],
            [".", "Throttles", ".", ".", { stat = "Sum", period = 60, color = "#ff7f0e" }]
          ]
          view    = "timeSeries"
          stacked = false
          title   = "Lambda Invocations, Errors & Throttles"
          region  = "us-east-1"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/Lambda", "Duration", "FunctionName", var.function_name, { stat = "Average", period = 60 }],
            ["...", { stat = "p95", period = 60 }],
            ["...", { stat = "p99", period = 60 }]
          ]
          view    = "timeSeries"
          stacked = false
          title   = "Lambda Execution Latency (Avg, p95, p99)"
          region  = "us-east-1"
        }
      }
    ]
  })
}
