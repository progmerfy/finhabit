from pydantic import BaseModel


class CategoryBreakdown(BaseModel):
    category_name: str
    icon: str
    amount: float
    percentage: float
    transaction_count: int


class AnalyticsResponse(BaseModel):
    total_income: float
    total_expense: float
    net_savings: float
    average_check: float
    transaction_count: int
    top_categories: list[CategoryBreakdown]
    change_vs_last_period: float  # percentage change in expenses


class BalanceHistory(BaseModel):
    date: str
    balance: float
    income: float
    expense: float


class MonthlyAnalytics(BaseModel):
    month: str
    income: float
    expense: float
    savings: float
