# ==============================================================================
# Module: Lambda
# Description: Manages AWS Lambda functions for container or zip deployments.
# ==============================================================================

resource "aws_lambda_function" "fastapi_app" {
  function_name = var.function_name
  role          = var.role_arn
  package_type  = var.package_type

  # Container image deployment
  image_uri = var.package_type == "Image" ? var.image_uri : null

  # Zip archive deployment (if package_type is Zip)
  filename         = var.package_type == "Zip" ? var.filename : null
  handler          = var.package_type == "Zip" ? var.handler : null
  runtime          = var.package_type == "Zip" ? var.runtime : null
  source_code_hash = var.package_type == "Zip" && var.filename != null ? filebase64sha256(var.filename) : null

  timeout     = var.timeout
  memory_size = var.memory_size

  dynamic "environment" {
    for_each = length(keys(var.environment_variables)) > 0 ? [1] : []
    content {
      variables = var.environment_variables
    }
  }

  tags = var.tags
}
