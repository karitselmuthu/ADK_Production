import re
import logging
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from config.policy_config import PII_PATTERNS, PROMPT_INJECTION_KEYWORDS

logger = logging.getLogger("enterprise_adk_agent.safety")

def check_pii(text: str) -> str | None:
    for entity, pattern in PII_PATTERNS.items():
        if re.search(pattern, text):
            return entity
    return None

def check_injection(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in PROMPT_INJECTION_KEYWORDS)

async def input_guardrail_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> LlmResponse | None:
    """Scans incoming prompt contents for PII or Prompt Injection patterns, returning a block response if matched."""
    request_text = ""
    if llm_request.contents:
        request_text = " ".join(
            part.text for c in llm_request.contents if c.parts for part in c.parts if part.text
        )

    if check_injection(request_text):
        logger.warning("Prompt injection blocked in input guardrail.")
        content = types.Content(
            role="model",
            parts=[types.Part.from_text("[GUARDRAIL VIOLATION] Input rejected: Prompt injection pattern detected.")]
        )
        return LlmResponse(content=content)

    pii_entity = check_pii(request_text)
    if pii_entity:
        logger.warning(f"PII leak blocked in input guardrail: {pii_entity}")
        content = types.Content(
            role="model",
            parts=[types.Part.from_text(f"[GUARDRAIL VIOLATION] Input rejected: Potential PII ({pii_entity}) detected.")]
        )
        return LlmResponse(content=content)

    return None
