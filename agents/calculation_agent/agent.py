from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from config.model_config import CALCULATION_AGENT_CONFIG, DEFAULT_RETRY
from tools.calculation_tools import estimate_travel_reimbursement, calculate_financial_metrics
from agents.calculation_agent.tools import forecast_quarterly_growth
from callbacks.logging_callbacks import before_agent_log, after_agent_log, before_model_log, after_model_log

SYSTEM_INSTRUCTION = """You are the Calculation / Business Logic Agent.
Your responsibility is to perform deterministic computations, cost estimations, quarterly growth forecasting, financial statement calculations, and evaluate rules-based recommendations.

Guidelines:
1. Always use the appropriate calculation tool to compute values (e.g., estimate_travel_reimbursement, forecast_quarterly_growth, calculate_financial_metrics). Do not perform manual arithmetic.
2. For questions regarding total spending, category totals, deposits, withdrawals, net savings, or account balances, use `calculate_financial_metrics`.
3. Present mathematical results in clear structured tables.
4. Highlight if the result requires VP approval (for travel reimbursements) or if savings metrics indicate negative net savings.
"""

calculation_agent = Agent(
    name="calculation_agent",
    description="Performs travel cost calculations, growth forecasting, and credit card/savings statement metrics computations.",
    model=Gemini(
        model=CALCULATION_AGENT_CONFIG["model"],
        retry_options=DEFAULT_RETRY,
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=CALCULATION_AGENT_CONFIG["temperature"],
        max_output_tokens=CALCULATION_AGENT_CONFIG["max_output_tokens"],
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[estimate_travel_reimbursement, forecast_quarterly_growth, calculate_financial_metrics],
    before_agent_callback=before_agent_log,
    after_agent_callback=after_agent_log,
    before_model_callback=before_model_log,
    after_model_callback=after_model_log,
)
