# Python access to S3
import os
import logging
import boto3
from botocore.exceptions import ClientError

################## FILE DOWNLOAD ####################

# Create directory for storing files temporarily to process
directory = "./tmp/"
# if not os.path.exists(directory):
#     os.makedirs(directory)

def download_file_from_S3(bucket, file_name, object_key):
    """Download a file from an S3 bucket

    :param bucket: Bucket to download from
    :param file_name: Local object name to download to
    :param object_key: Key of object to download
    :return: True if file was downloaded, else False
    """

    # Download the file
    s3 = boto3.resource('s3')
    try:
        response = s3.meta.client.download_file(bucket, object_key, directory+file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

################ FILE DOWNLOAD END ################

################ FILE UPLOAD ################

# Adapted from AWS S3 documentation
def upload_file_to_S3(bucket, file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param bucket: Bucket to upload to
    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3 = boto3.resource('s3')
    try:
        response = s3.meta.client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    except FileNotFoundError as e:
        logging.error(e)
        return False
    return True

################ FILE UPLOAD END ################
