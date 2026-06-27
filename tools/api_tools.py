import logging
from config.tool_config import SERVICENOW_INSTANCE, JIRA_INSTANCE, CRM_INSTANCE
from google.adk.tools import ToolContext

# Setup logger
logger = logging.getLogger(__name__)

def create_servicenow_incident(
    short_description: str,
    description: str,
    urgency: str,
    tool_context: ToolContext
) -> dict:
    """Creates a ServiceNow incident.

    Args:
        short_description: Brief summary of the incident.
        description: Detailed explanation of the issue.
        urgency: Urgency level ('1' - High, '2' - Medium, '3' - Low).

    Returns:
        dict with creation status and mock incident details.
    """
    logger.info(f"Creating incident in ServiceNow instance {SERVICENOW_INSTANCE}")

    # Check authorization in state
    user_id = tool_context.state.get("user_id")
    if not user_id:
        return {"status": "error", "message": "Unauthorized request: user_id is missing from session state."}

    # Generate mock response
    incident_id = f"INC{abs(hash(short_description)) % 10000000:07d}"

    return {
        "status": "success",
        "incident_id": incident_id,
        "short_description": short_description,
        "description": description,
        "urgency": urgency,
        "assigned_to": "Enterprise Tier-2 Support",
        "state": "New",
        "created_by": user_id,
    }

def create_jira_issue(
    project_key: str,
    summary: str,
    description: str,
    issue_type: str,
    tool_context: ToolContext
) -> dict:
    """Creates an issue ticket in Jira.

    Args:
        project_key: Key of the project (e.g., 'PROD', 'ENG').
        summary: Short summary of the task.
        description: Full details of the task/bug.
        issue_type: Type of issue ('Bug', 'Story', 'Task').

    Returns:
        dict with Jira issue creation response.
    """
    logger.info(f"Creating issue in Jira instance {JIRA_INSTANCE}")

    user_id = tool_context.state.get("user_id")
    if not user_id:
        return {"status": "error", "message": "Unauthorized request: user_id is missing."}

    issue_id = f"{project_key}-{abs(hash(summary)) % 1000:03d}"

    return {
        "status": "success",
        "issue_id": issue_id,
        "summary": summary,
        "issue_type": issue_type,
        "status_name": "To Do",
        "reporter": user_id,
    }

def update_crm_opportunity(
    opportunity_id: str,
    stage: str,
    amount: float,
    tool_context: ToolContext
) -> dict:
    """Updates the stage or amount of a CRM opportunity.

    Args:
        opportunity_id: Identifier of the opportunity.
        stage: New stage (e.g., 'Prospecting', 'Qualification', 'Closed Won').
        amount: Estimated revenue value.

    Returns:
        dict with CRM update status.
    """
    logger.info(f"Updating opportunity {opportunity_id} in CRM {CRM_INSTANCE}")

    return {
        "status": "success",
        "opportunity_id": opportunity_id,
        "updated_stage": stage,
        "updated_amount": amount,
        "message": f"Successfully updated CRM opportunity {opportunity_id} to '{stage}' with amount {amount}."
    }
