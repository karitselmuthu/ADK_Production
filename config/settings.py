import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "enterprise-adk-project")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-east1")
LOGS_BUCKET_NAME = os.getenv("LOGS_BUCKET_NAME", "")
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")

# Recommended Session State Pattern
SESSION_KEYS = {
    "USER_ID": "user_id",
    "TENANT_ID": "tenant_id",
    "INTENT": "intent",
    "SELECTED_PRODUCT": "selected_product",
    "SEARCH_CONTEXT": "search_context",
    "APPROVAL_STATUS": "approval_status",
    "LAST_TOOL_RESULT": "last_tool_result",
}
