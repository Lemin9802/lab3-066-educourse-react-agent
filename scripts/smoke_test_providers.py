import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.openai_provider import OpenAIProvider
from src.core.gemini_provider import GeminiProvider


def test_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("DEFAULT_OPENAI_MODEL", "gpt-4o")

    if not api_key:
        print("OPENAI_API_KEY is missing. Skipping OpenAI test.")
        return

    provider = OpenAIProvider(model_name=model, api_key=api_key)

    result = provider.generate(
        prompt="Reply with exactly this sentence: OpenAI provider works.",
        system_prompt="You are a concise test assistant."
    )

    print("\n=== OpenAI Test ===")
    print("Provider:", result.get("provider"))
    print("Model:", provider.model_name)
    print("Latency:", result.get("latency_ms"), "ms")
    print("Usage:", result.get("usage"))
    print("Content:", result.get("content"))


def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("DEFAULT_GEMINI_MODEL", "gemini-1.5-flash")

    if not api_key:
        print("GEMINI_API_KEY is missing. Skipping Gemini test.")
        return

    provider = GeminiProvider(model_name=model, api_key=api_key)

    result = provider.generate(
        prompt="Reply with exactly this sentence: Gemini provider works.",
        system_prompt="You are a concise test assistant."
    )

    print("\n=== Gemini Test ===")
    print("Provider:", result.get("provider"))
    print("Model:", provider.model_name)
    print("Latency:", result.get("latency_ms"), "ms")
    print("Usage:", result.get("usage"))
    print("Content:", result.get("content"))


def main():
    load_dotenv()
    test_openai()
    test_gemini()


if __name__ == "__main__":
    main()