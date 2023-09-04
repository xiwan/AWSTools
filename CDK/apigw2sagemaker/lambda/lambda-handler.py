import os
import io
import boto3
import json
import csv

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    inputsData = {'inputs': event}
    data = json.dumps(inputsData)
    payload = data
    
    # print("=================1")
    # print(payload)
    
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        Accept = "application/json",
        Body=payload)
       
    # print("=================2")
    # print(response)
    result = json.loads(response['Body'].read().decode())
    print(result)
    
    return 200