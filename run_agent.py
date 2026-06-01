import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.provider_factory import create_provider

try:
    from src.tools.educourse_tools import TOOLS
except ImportError:
    from src.tools.educourse_mock_tools import TOOLS


DEFAULT_QUERY = (
    "Em muốn học Python beginner vào buổi tối, ngân sách khoảng 1.500.000 VND. "
    "Còn lớp nào phù hợp không và học phí sau mã STUDENT10 là bao nhiêu?"
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run EduCourse ReAct Agent with selected LLM provider."
    )

    parser.add_argument(
        "--provider",
        choices=["openai", "gemini", "google"],
        default=None,
        help="LLM provider to use. Example: openai or gemini.",
    )

    parser.add_argument(
        "--model",
        default=None,
        help="Optional model override. Example: gpt-4o or gemini-2.5-flash.",
    )

    parser.add_argument(
        "--query",
        default=DEFAULT_QUERY,
        help="User query for the agent.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    llm = create_provider(
        provider_name=args.provider,
        model_name=args.model,
    )

    tool_names = [tool["name"] for tool in TOOLS]

    print("\n=== RUN CONFIG ===")
    print(f"Provider model: {llm.model_name}")
    print(f"Available tools: {', '.join(tool_names)}")
    print(f"Query: {args.query}")

    result = llm.generate(
        prompt=(
            "You are a course registration assistant. "
            "For now, simply acknowledge the user query in one Vietnamese sentence.\n\n"
            f"User query: {args.query}"
        ),
        system_prompt=(
            "You are a concise assistant for a course registration demo."
        ),
    )

    print("\n=== PROVIDER RESPONSE ===")
    print("Provider:", result.get("provider"))
    print("Latency:", result.get("latency_ms"), "ms")
    print("Usage:", result.get("usage"))
    print("Content:", result.get("content"))


if __name__ == "__main__":
    main()