def estimate_travel_reimbursement(
    flight_cost: float,
    hotel_cost: float,
    days: int,
    daily_allowance: float = 75.0
) -> dict:
    """Calculates the estimated travel reimbursement request total and validates against limits.

    Args:
        flight_cost: Cost of the flight ticket.
        hotel_cost: Nightly rate of the hotel.
        days: Duration of the trip in days.
        daily_allowance: Daily food/transport allowance.

    Returns:
        dict containing total cost estimation and VP approval flag if exceeding $1000 threshold.
    """
    total_hotel = hotel_cost * days
    total_allowance = daily_allowance * days
    grand_total = flight_cost + total_hotel + total_allowance

    requires_vp_approval = grand_total > 1000.0

    return {
        "status": "success",
        "flight_cost": flight_cost,
        "total_hotel": total_hotel,
        "total_allowance": total_allowance,
        "grand_total": grand_total,
        "requires_vp_approval": requires_vp_approval,
        "policy_verdict": "Requires VP approval (exceeds $1000)" if requires_vp_approval else "Approved within standard limits",
    }

import csv
import os

def calculate_financial_metrics(
    statement_type: str,
    metric_type: str,
    month: str = ""
) -> dict:
    """Calculates sums, averages, or category breakdowns from credit card or savings statements.

    Args:
        statement_type: The type of statement to analyze ('savings' or 'credit_card').
        metric_type: The calculation type ('total_spent', 'category_breakdown', 'savings_summary').
        month: Optional filter for a specific month in YYYY-MM format (e.g., '2026-03'). If omitted, analyzes all six months.

    Returns:
        dict containing calculation details and computed values.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = "savings_statements.csv" if statement_type.lower() == "savings" else "credit_card_statements.csv"
    filepath = os.path.join(base_dir, "data", "statements", filename)

    if not os.path.exists(filepath):
        return {"status": "error", "message": f"Statement file not found at {filepath}."}

    rows = []
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row.get("Date", "")
                if month and not date.startswith(month):
                    continue
                rows.append(row)
    except Exception as e:
        return {"status": "error", "message": f"Failed to parse CSV statement: {str(e)}"}

    if not rows:
        return {"status": "success", "message": "No transaction records matched the filters.", "computed_value": 0.0}

    if statement_type.lower() == "credit_card":
        if metric_type == "total_spent":
            total = sum(float(r["Amount"]) for r in rows if r.get("Amount"))
            return {
                "status": "success",
                "statement_type": statement_type,
                "metric_type": metric_type,
                "month": month or "all",
                "computed_value": round(total, 2)
            }
        elif metric_type == "category_breakdown":
            breakdown = {}
            for r in rows:
                cat = r.get("Category", "Uncategorized")
                amt = float(r["Amount"]) if r.get("Amount") else 0.0
                breakdown[cat] = breakdown.get(cat, 0.0) + amt
            for k in breakdown:
                breakdown[k] = round(breakdown[k], 2)
            return {
                "status": "success",
                "statement_type": statement_type,
                "metric_type": metric_type,
                "month": month or "all",
                "breakdown": breakdown
            }

    elif statement_type.lower() == "savings":
        if metric_type == "savings_summary":
            total_deposits = sum(float(r["Amount"]) for r in rows if r.get("Type") == "Deposit" and r.get("Amount"))
            total_withdrawals = sum(float(r["Amount"]) for r in rows if r.get("Type") == "Withdrawal" and r.get("Amount"))
            net_savings = total_deposits - total_withdrawals
            ending_balance = float(rows[-1]["RunningBalance"]) if rows and rows[-1].get("RunningBalance") else 0.0

            return {
                "status": "success",
                "statement_type": statement_type,
                "metric_type": metric_type,
                "month": month or "all",
                "total_deposits": round(total_deposits, 2),
                "total_withdrawals": round(total_withdrawals, 2),
                "net_savings": round(net_savings, 2),
                "ending_balance": round(ending_balance, 2)
            }

    return {"status": "error", "message": f"Unsupported combination: statement_type={statement_type}, metric_type={metric_type}."}

