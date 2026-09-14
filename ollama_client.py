import json
import os

import requests

from system_prompt import SYSTEM_PROMPT


DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1"
OLLAMA_API_ENDPOINT = "/api/generate"


class OllamaClient:

    def __init__(
        self,
        host: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
    ):
        self.host = (
            host
            or os.getenv(
                "OLLAMA_HOST",
                DEFAULT_OLLAMA_HOST,
            )
        ).rstrip("/")

        self.model = (
            model
            or os.getenv(
                "OLLAMA_MODEL",
                DEFAULT_MODEL,
            )
        )

        self.api_key = (
            api_key
            or os.getenv("OLLAMA_API_KEY")
        )

        self.endpoint = (
            f"{self.host}{OLLAMA_API_ENDPOINT}"
        )

    def generate(self, prompt: str) -> str:

        payload = {
            "model": self.model,
            "system": SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = (
                f"Bearer {self.api_key}"
            )

        print("\nAnalyzing with Ollama...")
        print(f"Model: {self.model}")

        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=180,
            )

        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(
                f"Could not connect to Ollama at "
                f"{self.endpoint}."
            ) from exc

        except requests.exceptions.Timeout as exc:
            raise RuntimeError(
                "Ollama request timed out."
            ) from exc

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                f"Ollama request failed: {exc}"
            ) from exc

        if response.status_code != 200:
            raise RuntimeError(
                f"Ollama API returned HTTP "
                f"{response.status_code}.\n"
                f"{response.text.strip()}"
            )

        try:
            response_data = response.json()

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Ollama returned an invalid response."
            ) from exc

        generated_text = response_data.get(
            "response"
        )

        if not generated_text:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        return generated_text