# ==============================================================================
# Terraform Declarative Import Blocks
# ==============================================================================
# Automatically imports pre-existing remote backend infrastructure (S3 Bucket
# and DynamoDB Lock Table) into Terraform state if they already exist in AWS.
# ==============================================================================

import {
  to = aws_s3_bucket.state
  id = var.state_bucket_name
}

import {
  to = aws_s3_bucket_versioning.state
  id = var.state_bucket_name
}

import {
  to = aws_s3_bucket_server_side_encryption_configuration.state
  id = var.state_bucket_name
}

import {
  to = aws_s3_bucket_public_access_block.state
  id = var.state_bucket_name
}

import {
  to = aws_dynamodb_table.locks
  id = var.lock_table_name
}
