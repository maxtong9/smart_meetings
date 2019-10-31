# Python access to S3
import os
import logging
import boto3
from botocore.exceptions import ClientError

################## FILE DOWNLOAD ####################

# Key and filename for testing download
# bucket = 'smartmeetingsbelieving'
# object_key = 'ts65ue95bv6vi70y3gnogbmcs6mz'
# object_name = 'gordonBurger.txt'

# Create directory for storing files temporarily to process
directory = "/tmp/"
os.makedirs(directory, exist_ok=True)

def download_file_from_S3(bucket, object_key, object_name):
    """Download a file from an S3 bucket

    :param bucket: Bucket to download from
    :param object_key: Key of object to download
    :param object_name: Local object name to download to
    :return: True if file was downloaded, else False
    """
    s3 = boto3.resource('s3')

    try:
        response = s3.meta.client.download_file(bucket, object_key, directory + object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Function call for testing File Download
# download_file_from_S3(file_key, file_name)

############# FILE DOWNLOAD END ######################

######## FILE UPLOAD ####################
