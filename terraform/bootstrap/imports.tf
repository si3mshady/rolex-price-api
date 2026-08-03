# ==============================================================================
# Terraform Declarative Import Blocks
# ==============================================================================
# Automatically imports pre-existing remote backend infrastructure (S3 Bucket
# and DynamoDB Lock Table) into Terraform state if they already exist in AWS.
# ==============================================================================

import {
  to = aws_s3_bucket.state
  id = "rolex-price-api-tf-state-dev"
}

import {
  to = aws_s3_bucket_versioning.state
  id = "rolex-price-api-tf-state-dev"
}

import {
  to = aws_s3_bucket_server_side_encryption_configuration.state
  id = "rolex-price-api-tf-state-dev"
}

import {
  to = aws_s3_bucket_public_access_block.state
  id = "rolex-price-api-tf-state-dev"
}

import {
  to = aws_dynamodb_table.locks
  id = "rolex-price-api-tf-locks-dev"
}
