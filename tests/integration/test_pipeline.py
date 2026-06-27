from google.adk.apps import App
from agents.root.agent import root_agent

def test_agent_orchestrator_initialization():
    """Verifies that the ADK App and multi-agent hierarchy are fully and correctly bound."""
    app = App(root_agent=root_agent, name="app")
    
    # Check App config
    assert app.name == "app"
    assert app.root_agent.name == "root_agent"
    
    # Verify sub-agents are properly attached
    sub_agents = {sa.name: sa for sa in app.root_agent.sub_agents}
    expected_sub_agents = [
        "knowledge_agent",
        "workflow_agent",
        "calculation_agent",
        "validation_agent",
        "escalation_agent",
    ]
    for agent_name in expected_sub_agents:
        assert agent_name in sub_agents
        
    # Verify root agent tool registrations
    registered_tools = {t.__name__ for t in app.root_agent.tools}
    assert "get_session_state" in registered_tools
    assert "set_session_state" in registered_tools
