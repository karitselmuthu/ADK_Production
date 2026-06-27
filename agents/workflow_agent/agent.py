from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from config.model_config import WORKFLOW_AGENT_CONFIG, DEFAULT_RETRY
from tools.api_tools import create_servicenow_incident, create_jira_issue, update_crm_opportunity
from tools.approval_tools import submit_for_approval
from agents.workflow_agent.prompts import SYSTEM_INSTRUCTION
from callbacks.logging_callbacks import before_agent_log, after_agent_log, before_model_log, after_model_log

workflow_agent = Agent(
    name="workflow_agent",
    description="Executes business transactions such as ServiceNow tickets, Jira tasks, CRM updates, and approvals.",
    model=Gemini(
        model=WORKFLOW_AGENT_CONFIG["model"],
        retry_options=DEFAULT_RETRY,
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=WORKFLOW_AGENT_CONFIG["temperature"],
        max_output_tokens=WORKFLOW_AGENT_CONFIG["max_output_tokens"],
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        create_servicenow_incident,
        create_jira_issue,
        update_crm_opportunity,
        submit_for_approval
    ],
    before_agent_callback=before_agent_log,
    after_agent_callback=after_agent_log,
    before_model_callback=before_model_log,
    after_model_callback=after_model_log,
)
