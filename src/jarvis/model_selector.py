from __future__ import annotations

from typing import Optional, Dict, Any

from langchain.chat_models import BedrockChat
from langchain.schema import HumanMessage, SystemMessage

from .services.sllm_client import SLLMClient


class ModelSelector:
    """Selects and manages different language models."""

    def __init__(
            self,
            model_type: str = "bedrock",
            model_config: Optional[Dict[str, Any]] = None
    ) -> None:
        self.model_type = model_type
        self.model_config = model_config or {}
        self.model = self._initialize_model()
        self.sllm_client = self.model if isinstance(self.model, SLLMClient) else None

    def _initialize_model(self) -> Any:
        """Initialize the selected model."""
        if self.model_type == "bedrock":
            return BedrockChat(
                model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                region_name="us-east-1",
                model_kwargs={"temperature": 0.7}
            )
        elif self.model_type == "sllm":
            return SLLMClient(
                api_key=self.model_config.get("api_key"),
                base_url=self.model_config.get("base_url", "http://localhost:8000")
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def generate_response(
            self,
            prompt: str,
            system_prompt: Optional[str] = None,
            **kwargs: Any
    ) -> str:
        """Generate a response using the selected model."""
        if self.model_type == "bedrock":
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            response = self.model.invoke(messages)
            return response.content
        elif self.model_type == "sllm":
            if system_prompt:
                prompt = f"{system_prompt}\n\n{prompt}"
            return self.model.generate(prompt, **kwargs)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def analyze_code(
            self,
            code: str,
            analysis_type: str = "general",
            **kwargs: Any
    ) -> Dict[str, Any]:
        """Analyze code using the selected model."""
        if self.model_type == "sllm":
            return self.model.code_analysis(code, analysis_type, **kwargs)
        else:
            # For other models, use the generate_response method
            prompt = f"Analyze this code:\n\n{code}\n\nAnalysis type: {analysis_type}"
            response = self.generate_response(prompt, **kwargs)
            return {"analysis": response}

    def explain_code(
            self,
            code: str,
            detail_level: str = "detailed",
            **kwargs: Any
    ) -> str:
        """Explain code using the selected model."""
        if self.model_type == "sllm":
            return self.model.explain_code(code, detail_level, **kwargs)
        else:
            # For other models, use the generate_response method
            prompt = f"Explain this code in {detail_level} detail:\n\n{code}"
            return self.generate_response(prompt, **kwargs)
