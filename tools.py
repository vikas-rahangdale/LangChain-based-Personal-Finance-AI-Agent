from langchain.tools import tool

@tool
def calculator(expression: str) -> float:
    """Useful for general mathematical calculations. Input: expression string."""
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"

@tool
def emi_calculator(principal: float, annual_rate: float, years: int) -> float:
    """Calculate EMI for a loan. Input: principal, annual_rate, years."""
    r = annual_rate / 12 / 100
    n = years * 12
    emi = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return round(emi, 2)

@tool
def sip_calculator(monthly_investment: float, annual_rate: float, years: int) -> float:
    """Calculate future value of monthly investments. Input: monthly_investment, annual_rate, years."""
    r = annual_rate / 12 / 100
    n = years * 12
    fv = monthly_investment * (((1 + r)**n - 1) / r)
    return round(fv, 2)

@tool
def budget_planner(income: float) -> dict:
    """Create a budget plan using 50-30-20 rule. Input: income."""
    return {
        "Needs (50%)": round(income * 0.50, 2),
        "Wants (30%)": round(income * 0.30, 2),
        "Savings (20%)": round(income * 0.20, 2),
    }
