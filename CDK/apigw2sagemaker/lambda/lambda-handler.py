import os
import io
import boto3
import json

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

def handler(event, context):
    print(ENDPOINT_NAME)
    return 200