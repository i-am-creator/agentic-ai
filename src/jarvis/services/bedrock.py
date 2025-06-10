from __future__ import annotations

import boto3

class BedrockClient:
    def __init__(self, region_name: str = "eu-central-1") -> None:  # Removed extra space
        self.client = boto3.client("bedrock-runtime", region_name=region_name)

    def generate(self, prompt: str) -> str:
        response = self.client.invoke_model(
            body=prompt.encode(),
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0"
        )
        return response.get("body", b"").decode()