from __future__ import annotations

import boto3

class BedrockClient:
    def __init__(self, region_name: str = "us-east-1") -> None:
        self.client = boto3.client("bedrock-runtime", region_name=region_name)

    def generate(self, prompt: str) -> str:
        # This is a simplified call; real parameters may differ.
        response = self.client.invoke_model(body=prompt.encode(), modelId="claude-v1")
        return response.get("body", b"").decode()
