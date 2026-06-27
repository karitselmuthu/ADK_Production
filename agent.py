# Top-Level ADK App Entrypoint
from google.adk.apps import App
from agents.root.agent import root_agent

# The App must be named 'app'
app = App(
    root_agent=root_agent,
    name="enterprise_adk_agent",
)
