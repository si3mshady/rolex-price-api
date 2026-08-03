# ==============================================================================
# Module: IAM
# Description: Manages IAM roles, assume-role policies, and permission sets.
# ==============================================================================

# Lambda execution assume-role policy document
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# IAM Execution Role for Lambda
resource "aws_iam_role" "lambda_exec" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = var.tags
}

# Attach AWS managed policy for Lambda basic execution (CloudWatch Logs)
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 access policy statement document if S3 bucket ARN is provided
data "aws_iam_policy_document" "s3_access" {
  count = var.s3_bucket_arn != "" ? 1 : 0

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
      "s3:PutObject"
    ]
    resources = [
      var.s3_bucket_arn,
      "${var.s3_bucket_arn}/*"
    ]
  }
}

resource "aws_iam_role_policy" "s3_access" {
  count  = var.s3_bucket_arn != "" ? 1 : 0
  name   = "${var.role_name}-s3-access"
  role   = aws_iam_role.lambda_exec.id
  policy = data.aws_iam_policy_document.s3_access[0].json
}
