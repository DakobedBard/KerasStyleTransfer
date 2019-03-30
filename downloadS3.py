import sys
import boto3
import botocore

filename = sys.argv[1]
outputfilename = sys.argv[2]
S3_BUCKET='heyward-style-transfer-images'

s3_resource = boto3.resource('s3')
try:
    s3_resource.Bucket(S3_BUCKET).download_file(filename, outputfilename)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise