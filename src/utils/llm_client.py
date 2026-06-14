import os
from dotenv import load_dotenv
import ollama

from src.utils.bedrock_client import generate_with_bedrock

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
OLLAMA_MODEL = "phi3:mini"


def generate_with_ollama(prompt: str) -> str:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 0.2,
            "num_predict": 300
        }
    )

    if hasattr(response, "message"):
        return response.message.content

    if isinstance(response, dict):
        return response.get("message", {}).get("content", "")

    return str(response)


def generate_response(prompt: str) -> str:
    if LLM_PROVIDER == "bedrock":
        return generate_with_bedrock(prompt)

    if LLM_PROVIDER == "ollama":
        return generate_with_ollama(prompt)

    raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")