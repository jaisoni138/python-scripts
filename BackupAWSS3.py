import os
import tarfile
import boto3
from datetime import datetime

def backup_directory_to_s3(directory_path, bucket_name):
    # Ensure the directory exists
    if not os.path.isdir(directory_path):
        raise ValueError(f"Directory {directory_path} does not exist")

    # Create a compressed tar.gz file of the directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"{directory_path}_{timestamp}.tar.gz"
    
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(directory_path, arcname=os.path.basename(directory_path))

    # Upload the compressed file to AWS S3
    s3_client = boto3.client('s3')
    
    try:
        s3_client.upload_file(archive_name, bucket_name, archive_name)
        print(f"Backup successful: {archive_name} uploaded to {bucket_name}")
    except Exception as e:
        print(f"Failed to upload backup: {e}")
    finally:
        # Clean up the local archive file
        os.remove(archive_name)

# Usage example
# backup_directory_to_s3("/path/to/your/directory", "your-s3-bucket-name")
