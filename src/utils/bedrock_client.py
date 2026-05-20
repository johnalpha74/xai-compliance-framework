import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID")


def generate_with_bedrock(prompt: str, max_tokens: int = 400):

    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_REGION
    )

    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": 0.2,
            "topP": 0.9
        }
    }
