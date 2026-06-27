from google.adk.tools import ToolContext
from config.settings import SESSION_KEYS

def get_session_state(key: str, tool_context: ToolContext) -> dict:
    """Retrieves a value from the session state by key.

    Args:
        key: The key in session state to retrieve (e.g., user_id, Selected_product, search_context).

    Returns:
        A dictionary containing the status and the retrieved value.
    """
    val = tool_context.state.get(key)
    return {"status": "success", "key": key, "value": val}

def set_session_state(key: str, value: str, tool_context: ToolContext) -> dict:
    """Sets a value in the session state by key.

    Args:
        key: The key in session state to set. Must be a valid session state key or prefixed with user:, app:, or temp:.
        value: The value to store.

    Returns:
        A dictionary confirming the status.
    """
    valid_base_keys = list(SESSION_KEYS.values())
    
    # Check if it has a prefix
    has_valid_prefix = any(key.startswith(prefix) for prefix in ["user:", "app:", "temp:"])
    
    if key not in valid_base_keys and not has_valid_prefix:
        return {
            "status": "error",
            "message": f"Invalid state key '{key}'. Must be in {valid_base_keys} or use user:/app:/temp: prefix."
        }

    tool_context.state[key] = value
    return {"status": "success", "key": key, "value": value}
