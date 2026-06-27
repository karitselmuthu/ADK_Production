import os
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# Default environment settings
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "enterprise-adk-project")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-east1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

allow_origins = os.getenv("ALLOW_ORIGINS", "*").split(",")
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

# Build the FastAPI server wrapping our ADK agents
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    otel_to_cloud=False,  # Set to False to avoid local OTel export warnings
)

app.title = "enterprise-adk-agent"
app.description = "API endpoint for the Enterprise ADK Multi-Agent Orchestrator"

if __name__ == "__main__":
    import uvicorn
    # Load and run the server
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
