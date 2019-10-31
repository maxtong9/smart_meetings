# Python access to S3
import boto3
import os

s3 = boto3.resource('s3')

bucket_name = 'smartmeetingsbelieving'

# Key and filename for testing
# file_key = 'ts65ue95bv6vi70y3gnogbmcs6mz'
# file_name = 'gordonBurger.txt'

# Create '/tmp/' directory for storing files temporarily to process
if not os.path.exists('./tmp'):
    os.makedirs('./tmp')

def download_file_from_S3(file_key, file_name):
    s3.meta.client.download_file(bucket_name, file_key, './tmp/' + file_name)

# Function call for testing
# download_file_from_S3(file_key, file_name)
