from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from config.model_config import KNOWLEDGE_AGENT_CONFIG, DEFAULT_RETRY
from tools.search_tools import query_enterprise_kb, query_financial_statements
from agents.knowledge_agent.prompts import SYSTEM_INSTRUCTION
from callbacks.logging_callbacks import before_agent_log, after_agent_log, before_model_log, after_model_log

knowledge_agent = Agent(
    name="knowledge_agent",
    description="Queries policies, travel rules, HR manuals, and financial credit card / savings statement logs to answer questions.",
    model=Gemini(
        model=KNOWLEDGE_AGENT_CONFIG["model"],
        retry_options=DEFAULT_RETRY,
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=KNOWLEDGE_AGENT_CONFIG["temperature"],
        max_output_tokens=KNOWLEDGE_AGENT_CONFIG["max_output_tokens"],
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[query_enterprise_kb, query_financial_statements],
    before_agent_callback=before_agent_log,
    after_agent_callback=after_agent_log,
    before_model_callback=before_model_log,
    after_model_callback=after_model_log,
)
