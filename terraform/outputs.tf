output "bucket_name" {
  value = aws_s3_bucket.bucket.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}
