import os

# Datastore Config for Knowledge Agent
VERTEX_AI_SEARCH_DATASTORE = os.getenv(
    "VERTEX_AI_SEARCH_DATASTORE",
    "projects/enterprise-adk-project/locations/global/collections/default_collection/dataStores/default-datastore",
)

# API Configurations
API_TIMEOUT = 10
API_RETRIES = 3
API_BACKOFF_FACTOR = 0.5

# Mock Instance URLs
SERVICENOW_INSTANCE = os.getenv("SERVICENOW_INSTANCE", "https://dev-mock.service-now.com")
JIRA_INSTANCE = os.getenv("JIRA_INSTANCE", "https://mock-company.atlassian.net")
CRM_INSTANCE = os.getenv("CRM_INSTANCE", "https://mock-crm.com")
