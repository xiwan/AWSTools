# Bedrock Runtime Wrapper


### How to call claude3

```
import json
import os
import sys
import logging
import boto3
import botocore

logger = logging.getLogger(__name__)

module_path = ".."
sys.path.append(os.path.abspath(module_path))
from utils.BedrockRuntimeWrapper import BedrockRuntimeWrapper, invoke
from botocore.exceptions import ClientError

client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
wrapper = BedrockRuntimeWrapper(client)

mode_id = "anthropic.claude-3-sonnet-20240229-v1:0"

text_generation_prompt = "5+3等于多少？"
print("\n====claude3====\n")
invoke(wrapper, mode_id, text_generation_prompt)
print("\n====claude3 with stream response====\n")
try:
    async for completion in wrapper.invoke_claude3_with_response_stream(text_generation_prompt):
        print(completion, end="")

except ClientError:
    logger.exception("Couldn't invoke model %s", model_id)
    raise

```