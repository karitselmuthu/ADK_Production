from tools.calculation_tools import estimate_travel_reimbursement
from tools.api_tools import create_servicenow_incident, create_jira_issue
from unittest.mock import MagicMock
from google.adk.tools import ToolContext

def test_estimate_travel_reimbursement_under_limit():
    res = estimate_travel_reimbursement(
        flight_cost=300.0, hotel_cost=100.0, days=3, daily_allowance=50.0
    )
    assert res["status"] == "success"
    assert res["grand_total"] == 750.0
    assert res["requires_vp_approval"] is False

def test_estimate_travel_reimbursement_over_limit():
    res = estimate_travel_reimbursement(
        flight_cost=600.0, hotel_cost=200.0, days=4, daily_allowance=75.0
    )
    assert res["status"] == "success"
    assert res["grand_total"] == 1700.0
    assert res["requires_vp_approval"] is True

def test_create_servicenow_incident_authorized():
    # Mock ToolContext state
    ctx = MagicMock(spec=ToolContext)
    ctx.state = {"user_id": "USR-123"}

    res = create_servicenow_incident(
        short_description="System Access Issue",
        description="Database connection refused.",
        urgency="2",
        tool_context=ctx
    )

    assert res["status"] == "success"
    assert res["incident_id"].startswith("INC")
    assert res["created_by"] == "USR-123"

def test_create_servicenow_incident_unauthorized():
    # Mock ToolContext without user_id
    ctx = MagicMock(spec=ToolContext)
    ctx.state = {}

    res = create_servicenow_incident(
        short_description="Access Issue",
        description="Refused",
        urgency="2",
        tool_context=ctx
    )

    assert res["status"] == "error"
    assert "Unauthorized" in res["message"]

from tools.search_tools import query_financial_statements
from tools.calculation_tools import calculate_financial_metrics

def test_query_financial_statements_cc():
    ctx = MagicMock(spec=ToolContext)
    ctx.state = {}

    res = query_financial_statements(
        statement_type="credit_card",
        query="Netflix",
        tool_context=ctx
    )

    assert res["status"] == "success"
    assert res["statement_type"] == "credit_card"
    assert res["total_records_matched"] == 6
    assert all(r["Description"].lower() == "netflix" for r in res["results"])

def test_calculate_financial_metrics_cc_total():
    res = calculate_financial_metrics(
        statement_type="credit_card",
        metric_type="total_spent"
    )
    assert res["status"] == "success"
    assert res["computed_value"] > 0.0

def test_calculate_financial_metrics_savings_summary():
    res = calculate_financial_metrics(
        statement_type="savings",
        metric_type="savings_summary",
        month="2026-03"
    )
    assert res["status"] == "success"
    assert res["total_deposits"] == 2500.0
    assert res["total_withdrawals"] == 1200.0
    assert res["net_savings"] == 1300.0
    assert res["ending_balance"] == 8900.0

