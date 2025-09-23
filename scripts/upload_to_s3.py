import boto3

bucket_name = 'my-data-engineering-bucket-aj'  # Your S3 bucket name
file_path = 'output/orders.csv'                 # Your fixed CSV path
object_name = 'orders/orders.csv'                # S3 object key (folder + filename)

s3 = boto3.client('s3')

try:
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"✅ Successfully uploaded {file_path} to s3://{bucket_name}/{object_name}")
except Exception as e:
    print(f"❌ Upload failed: {e}")

