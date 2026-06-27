from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from config.model_config import ROOT_AGENT_CONFIG, DEFAULT_RETRY

# Import sub-agents
from agents.knowledge_agent.agent import knowledge_agent
from agents.workflow_agent.agent import workflow_agent
from agents.calculation_agent.agent import calculation_agent
from agents.validation_agent.agent import validation_agent
from agents.escalation_agent.agent import escalation_agent

# Import tools & callbacks
from tools.session_tools import get_session_state, set_session_state
from callbacks.logging_callbacks import before_agent_log, after_agent_log, before_model_log, after_model_log
from callbacks.safety_callbacks import input_guardrail_callback
from callbacks.tracing_callbacks import before_model_trace, after_model_trace

async def root_before_model(callback_context, llm_request):
    # 1. Run safety / PII check
    safety_response = await input_guardrail_callback(callback_context, llm_request)
    if safety_response:
        return safety_response  # Blocks LLM call with a guardrail violation message

    # 2. Run telemetry & tracing
    await before_model_log(callback_context, llm_request)
    await before_model_trace(callback_context, llm_request)
    return None

async def root_after_model(callback_context, llm_response):
    await after_model_log(callback_context, llm_response)
    await after_model_trace(callback_context, llm_response)
    return None

SYSTEM_INSTRUCTION = """You are the Root Orchestrator Agent of this enterprise ADK system.
Your primary role is to understand the user's intent, select the appropriate sub-agent to handle their request, manage session state, and coordinate delegation.

Sub-Agents:
1. `knowledge_agent`: Specializes in corporate policies, travel rules, and looking up transaction entries from financial statements (credit card or savings logs).
2. `workflow_agent`: Specializes in executing business actions like creating ServiceNow incidents, Jira tasks, and CRM opportunity updates.
3. `calculation_agent`: Specializes in travel cost estimations, growth forecasting, and compiling financial statement metrics (totals, category summaries, net savings, ending balances).
4. `validation_agent`: Specializes in auditing proposed responses to check grounding, compliance violations, and hallucination scores.
5. `escalation_agent`: Specializes in human support queue routing, ticket escalations, and handoffs.

State Management:
- Use `set_session_state` and `get_session_state` to read/write state keys (e.g., user_id, tenant_id, selected_product, last_tool_result).

Guidelines:
- Never do search, API execution, calculations, or auditing yourself. Always delegate to the correct sub-agent.
- Route lookup queries (e.g., "Find all Chevron transactions", "When did I pay Netflix?") to `knowledge_agent`.
- Route mathematical summaries and breakdowns (e.g., "Total spent on groceries in March", "What is my ending savings balance?") to `calculation_agent`.
- Before delegating, make sure you have set the `user_id` and `tenant_id` if provided.
- Once a sub-agent provides a response, you can delegate to the `validation_agent` to audit it.
- If the validation agent flags a response as failed (grade is "fail" or hallucination score > 0.85), delegate to the `escalation_agent`.
"""

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=ROOT_AGENT_CONFIG["model"],
        retry_options=DEFAULT_RETRY,
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=ROOT_AGENT_CONFIG["temperature"],
        max_output_tokens=ROOT_AGENT_CONFIG["max_output_tokens"],
    ),
    instruction=SYSTEM_INSTRUCTION,
    sub_agents=[
        knowledge_agent,
        workflow_agent,
        calculation_agent,
        validation_agent,
        escalation_agent,
    ],
    tools=[get_session_state, set_session_state],
    before_agent_callback=before_agent_log,
    after_agent_callback=after_agent_log,
    before_model_callback=root_before_model,
    after_model_callback=root_after_model,
)
