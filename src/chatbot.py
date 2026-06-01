from typing import Any, Dict

from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger


class ChatbotBaseline:
    """
    Baseline chatbot for comparison with the ReAct agent.

    This class intentionally does not use tools or course catalog data. It asks
    the LLM to answer directly so evaluation can expose hallucinations on tasks
    that require course availability, coupon validation, or tuition calculation.
    """

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def get_system_prompt(self) -> str:
        return (
            "You are a helpful educational course advisor. "
            "Answer the student's question directly in Vietnamese. "
            "You do not have access to tools or live course data, so be concise "
            "and avoid claiming that you verified availability, coupons, or fees."
        )

    def run(self, query: str) -> Dict[str, Any]:
        logger.log_event(
            "CHATBOT_BASELINE_START",
            {"input": query, "model": self.llm.model_name},
        )

        result = self.llm.generate(query, system_prompt=self.get_system_prompt())

        logger.log_event(
            "CHATBOT_BASELINE_END",
            {
                "provider": result.get("provider"),
                "model": self.llm.model_name,
                "latency_ms": result.get("latency_ms"),
                "usage": result.get("usage", {}),
            },
        )

        return {
            "answer": result.get("content", ""),
            "provider": result.get("provider"),
            "model": self.llm.model_name,
            "latency_ms": result.get("latency_ms"),
            "usage": result.get("usage", {}),
            "used_tools": False,
        }
