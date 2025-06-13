import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def upload_file_to_s3(file_name, bucket, object_name=None):
    # If S3 object_name not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Initialize S3 client
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Upload Successful: {file_name} to s3://{bucket}/{object_name}")
    except FileNotFoundError:
        print(f"❌ The file {file_name} was not found")
    except NoCredentialsError:
        print("❌ AWS credentials not available")
    except ClientError as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    file_path = "output/orders.csv"
    bucket_name = "my-data-engineering-bucket-aj"
    s3_object_name = "orders/orders.csv"

    upload_file_to_s3(file_path, bucket_name, s3_object_name)
