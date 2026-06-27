from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from config.model_config import ESCALATION_AGENT_CONFIG, DEFAULT_RETRY
from callbacks.logging_callbacks import before_agent_log, after_agent_log, before_model_log, after_model_log
from google.adk.tools import ToolContext

def create_human_handoff(
    issue_summary: str,
    context_details: str,
    tool_context: ToolContext
) -> dict:
    """Creates a human handoff event and places the session into the human support queue.

    Args:
        issue_summary: Short explanation of why we are escalating (e.g., low confidence, HR conflict).
        context_details: Summary of the conversation details to prepare the human support agent.

    Returns:
        dict detailing the escalation ticket.
    """
    user_id = tool_context.state.get("user_id", "anonymous")
    ticket_id = f"ESC-{abs(hash(issue_summary)) % 100000:05d}"
    
    # Store escalation status in state and flag escalation to runtime
    tool_context.state["approval_status"] = "Escalated"
    tool_context.actions.escalate = True  
    
    return {
        "status": "escalated",
        "ticket_id": ticket_id,
        "assigned_queue": "L2_Human_Support_Queue",
        "issue_summary": issue_summary,
        "context_details": context_details,
        "user_id": user_id,
        "message": f"Escalated to human support under ticket {ticket_id}. Execution flow halted."
    }

SYSTEM_INSTRUCTION = """You are the Human Escalation Agent.
Your responsibility is to handle scenarios where automation should stop (e.g., HR complaints, financial approvals above limit, or low-confidence outcomes).
You must:
1. Generate a comprehensive handoff summary.
2. Route the session to the human queue using the `create_human_handoff` tool.
3. Be professional and reassure the user that a human expert is taking over.
"""

escalation_agent = Agent(
    name="escalation_agent",
    description="Handles human handoffs, creates escalation tickets, and halts flow on low-confidence cases.",
    model=Gemini(
        model=ESCALATION_AGENT_CONFIG["model"],
        retry_options=DEFAULT_RETRY,
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=ESCALATION_AGENT_CONFIG["temperature"],
        max_output_tokens=ESCALATION_AGENT_CONFIG["max_output_tokens"],
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[create_human_handoff],
    before_agent_callback=before_agent_log,
    after_agent_callback=after_agent_log,
    before_model_callback=before_model_log,
    after_model_callback=after_model_log,
)
