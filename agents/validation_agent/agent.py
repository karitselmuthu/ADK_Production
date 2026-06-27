from pydantic import BaseModel, Field
from typing import Literal, List
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from config.model_config import VALIDATION_AGENT_CONFIG, DEFAULT_RETRY
from callbacks.logging_callbacks import before_agent_log, after_agent_log, before_model_log, after_model_log

class ValidationReport(BaseModel):
    grade: Literal["pass", "fail"] = Field(description="The evaluation result.")
    hallucination_score: float = Field(description="Score between 0.0 (perfectly grounded) and 1.0 (fully hallucinated) relative to grounding text.")
    missing_assumptions: List[str] = Field(description="List of key assumptions or facts that are missing from the response.")
    compliance_issues: List[str] = Field(description="List of compliance format violations found.")
    feedback: str = Field(description="Explanation and recommendations for improvement.")

SYSTEM_INSTRUCTION = """You are the Validation / Critic Agent.
Your responsibility is to review responses to check if they are fully grounded, detect missing assumptions, validate compliance language, check format consistency, and ensure there are no hallucinated details.

Input format will consist of:
1. User Query
2. Proposed Response
3. Grounding Context (RAG context / Retrieved facts)

Analyze these three components carefully, compute a hallucination score, detect missing assumptions or formatting issues, and return a structured ValidationReport.
"""

validation_agent = Agent(
    name="validation_agent",
    description="Reviews proposed responses to score hallucinations, check compliance terms, and audit missing assumptions.",
    model=Gemini(
        model=VALIDATION_AGENT_CONFIG["model"],
        retry_options=DEFAULT_RETRY,
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=VALIDATION_AGENT_CONFIG["temperature"],
        max_output_tokens=VALIDATION_AGENT_CONFIG["max_output_tokens"],
    ),
    instruction=SYSTEM_INSTRUCTION,
    output_schema=ValidationReport,
    output_key="validation_result",
    before_agent_callback=before_agent_log,
    after_agent_callback=after_agent_log,
    before_model_callback=before_model_log,
    after_model_callback=after_model_log,
)
