from google.adk.tools import ToolContext

def submit_for_approval(request_details: str, tool_context: ToolContext) -> dict:
    """Submits a request for human/manager approval.

    Args:
        request_details: Description of what needs approval.

    Returns:
        dict detailing the request status.
    """
    tool_context.state["approval_status"] = "Pending"
    return {
        "status": "pending_approval",
        "request_details": request_details,
        "message": "The request has been submitted for manager approval. State has been set to Pending."
    }

def approve_request(tool_context: ToolContext) -> dict:
    """Approves the currently pending request.

    Returns:
        dict confirming approval.
    """
    tool_context.state["approval_status"] = "Approved"
    return {
        "status": "approved",
        "message": "The request has been approved."
    }
