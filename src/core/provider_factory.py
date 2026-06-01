import os
from typing import Optional

from dotenv import load_dotenv

from src.core.openai_provider import OpenAIProvider
from src.core.gemini_provider import GeminiProvider


def create_provider(
    provider_name: Optional[str] = None,
    model_name: Optional[str] = None,
):
    """
    Create an LLM provider using CLI overrides or .env defaults.

    Priority:
    1. CLI argument provider_name / model_name
    2. .env DEFAULT_PROVIDER / provider-specific default model
    """

    load_dotenv()

    provider = (
        provider_name
        or os.getenv("DEFAULT_PROVIDER", "openai")
    ).lower().strip()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing in .env")

        model = (
            model_name
            or os.getenv("DEFAULT_OPENAI_MODEL")
            or os.getenv("DEFAULT_MODEL")
            or "gpt-4o"
        )

        return OpenAIProvider(
            model_name=model,
            api_key=api_key,
        )

    if provider in ["gemini", "google"]:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in .env")

        model = (
            model_name
            or os.getenv("DEFAULT_GEMINI_MODEL")
            or os.getenv("DEFAULT_MODEL")
            or "gemini-2.5-flash"
        )

        return GeminiProvider(
            model_name=model,
            api_key=api_key,
        )

    raise ValueError(
        f"Unknown provider: {provider}. "
        "Use one of: openai, gemini, google."
    )