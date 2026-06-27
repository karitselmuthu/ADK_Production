import logging
from config.tool_config import VERTEX_AI_SEARCH_DATASTORE
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

MOCK_KB = {
    "leave": [
        {
            "title": "Corporate Leave Policy",
            "content": "All employees receive 25 days of paid annual leave. Leave requests must be submitted through ServiceNow at least 2 weeks in advance and approved by their direct supervisor.",
            "source": "HR-POL-024",
        }
    ],
    "travel": [
        {
            "title": "Travel Reimbursement Rules",
            "content": "Business travel expenses are fully reimbursable if pre-approved. Flights must be booked through the company portal. Expense claims above $1000 require VP approval.",
            "source": "FIN-POL-108",
        }
    ],
    "access": [
        {
            "title": "IT System Access Policy",
            "content": "Access to production systems is restricted to certified engineers and requires multi-factor authentication. Keys must be stored in Secret Manager and rotated every 90 days.",
            "source": "IT-SEC-003",
        }
    ]
}

def query_enterprise_kb(query: str, tool_context: ToolContext) -> dict:
    """Queries the Enterprise Knowledge Base for policies, guides, or manuals.

    Args:
        query: The search query string (e.g., 'leave rules', 'travel reimbursement limit').

    Returns:
        dict with list of retrieved doc fragments and citations.
    """
    logger.info(f"Searching KB with query: {query}")

    results = []
    query_lower = query.lower()

    if "leave" in query_lower or "vacation" in query_lower:
        results.extend(MOCK_KB["leave"])
    if "travel" in query_lower or "reimbursement" in query_lower or "expense" in query_lower:
        results.extend(MOCK_KB["travel"])
    if "access" in query_lower or "system" in query_lower or "security" in query_lower or "keys" in query_lower:
        results.extend(MOCK_KB["access"])

    if not results:
        results.append({
            "title": "Enterprise General Policy",
            "content": "For queries not explicitly covered by specific policies, refer to the Code of Conduct or contact the HR Support Center.",
            "source": "GEN-POL-001"
        })

    # Save results to session state search_context
    tool_context.state["search_context"] = str(results)

    return {
        "status": "success",
        "results": results,
        "datastore_queried": VERTEX_AI_SEARCH_DATASTORE if "enterprise-adk-project" not in VERTEX_AI_SEARCH_DATASTORE else "Mocked Local KB"
    }

import csv
import os

def query_financial_statements(
    statement_type: str,
    query: str,
    tool_context: ToolContext
) -> dict:
    """Queries the user's financial statements (savings or credit card) for transactions or details.

    Args:
        statement_type: The type of statement to search ('savings' or 'credit_card').
        query: The keyword or pattern to search for in transaction descriptions/categories (e.g., 'Starbucks', 'Dining', 'Salary', 'Rent').

    Returns:
        dict containing filtered list of transaction records.
    """
    logger.info(f"Searching financial statement {statement_type} for query: {query}")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = "savings_statements.csv" if statement_type.lower() == "savings" else "credit_card_statements.csv"
    filepath = os.path.join(base_dir, "data", "statements", filename)

    if not os.path.exists(filepath):
        return {"status": "error", "message": f"Statement file not found at {filepath}."}

    results = []
    query_lower = query.lower()

    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                desc = row.get("Description", "").lower()
                cat = row.get("Category", "").lower()
                typ = row.get("Type", "").lower()

                if query_lower in desc or query_lower in cat or query_lower in typ or query_lower == "all" or query_lower == "":
                    results.append(row)
    except Exception as e:
        return {"status": "error", "message": f"Failed to parse CSV statement: {str(e)}"}

    tool_context.state["search_context"] = str(results)

    return {
        "status": "success",
        "statement_type": statement_type,
        "results": results,
        "total_records_matched": len(results)
    }

