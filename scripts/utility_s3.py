import os
from dotenv import load_dotenv
import boto3

load_dotenv('.env',override=True)

def load_env():
    grobid_url = os.getenv("GROBID_URL")
    pdf_directory = os.getenv("PDF_DIR_PATH") # Store the downloaded PDF files from S3
    output_dir = os.getenv("OUTPUT_DIR_PATH") # Store the extracted txt files
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")
    access_key = os.getenv("S3_ACCESS_KEY")
    secret_key = os.getenv("S3_SECRET_KEY")
    region = os.getenv("S3_REGION")
    
    return grobid_url, pdf_directory, output_dir, s3_bucket_name, access_key, secret_key, region

# load env
grobid_url, pdf_directory, output_dir, s3_bucket_name, access_key, secret_key, region = load_env() 

def download_files_from_s3(local_folder, s3_folder):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name = region)

    # List objects in the specified S3 folder
    response = s3.list_objects_v2(Bucket=s3_bucket_name, Prefix=s3_folder)
    # print(response)
    file_paths = []

    # Download each file to the local directory
    for obj in response.get('Contents')[1:]:
        key = obj['Key']
        local_file_path = os.path.join(local_folder, os.path.basename(key))

        s3.download_file(s3_bucket_name, key, local_file_path)
        print(f"Downloaded: {key} to {local_file_path}")
        path = f"https://{s3_bucket_name}.s3.amazonaws.com/{key}"
        file_paths.append(path)

    print(file_paths)
    return file_paths

