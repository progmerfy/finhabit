from pydantic import BaseModel


class DashboardResponse(BaseModel):
    balance: float
    monthly_income: float
    monthly_expense: float
    total_savings: float
    savings_percent: float
    financial_rating: int
    today_spent: float
    daily_limit: float
    daily_remaining: float
