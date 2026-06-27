def forecast_quarterly_growth(current_amount: float, growth_rate: float, quarters: int) -> dict:
    """Forecasts the quarterly growth of an expense or cost over multiple quarters.

    Args:
        current_amount: Starting amount/cost.
        growth_rate: Quarterly growth rate (e.g., 0.05 for 5%).
        quarters: Number of quarters to project.

    Returns:
        dict containing the projected values.
    """
    projections = []
    val = current_amount
    for q in range(1, quarters + 1):
        val = val * (1 + growth_rate)
        projections.append({"quarter": q, "projected_amount": round(val, 2)})

    return {
        "status": "success",
        "current_amount": current_amount,
        "growth_rate": growth_rate,
        "quarters": quarters,
        "projections": projections,
        "final_projected_amount": round(val, 2),
    }
