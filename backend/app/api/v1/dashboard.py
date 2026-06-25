from datetime import date, datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.income_repo import IncomeRepository
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.goal_repo import GoalRepository
from app.repositories.budget_repo import BudgetRepository
from app.schemas.dashboard import DashboardResponse

router = APIRouter()


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    today = date.today()
    month_start = today.replace(day=1)

    income_repo = IncomeRepository(db)
    expense_repo = ExpenseRepository(db)
    goal_repo = GoalRepository(db)
    budget_repo = BudgetRepository(db)

    monthly_income = await income_repo.get_total_by_period(user.id, month_start, today)
    monthly_expense = await expense_repo.get_total_by_period(user.id, month_start, today)

    goals = await goal_repo.get_by_user(user.id)
    total_savings = sum(g.current_amount for g in goals)

    balance = monthly_income - monthly_expense - total_savings
    savings_percent = round((total_savings / monthly_income * 100), 1) if monthly_income > 0 else 0

    # Financial rating 0-1000
    rating = 500
    if user.streak_days > 0:
        rating += min(user.streak_days * 5, 200)
    if savings_percent >= 20:
        rating += 100
    elif savings_percent >= 10:
        rating += 50
    if total_savings > 0:
        rating += min(int(total_savings / 10), 200)
    rating = min(rating, 1000)

    # Daily budget
    today_expense = await expense_repo.get_total_by_period(user.id, today, today)
    budgets = await budget_repo.get_by_user_month(user.id, today.month, today.year)
    total_budget = sum(b.limit_amount for b in budgets) if budgets else 0
    daily_limit = round(total_budget / 30, 2) if total_budget > 0 else 0
    daily_remaining = round(daily_limit - today_expense, 2)

    return DashboardResponse(
        balance=round(balance, 2),
        monthly_income=round(monthly_income, 2),
        monthly_expense=round(monthly_expense, 2),
        total_savings=round(total_savings, 2),
        savings_percent=savings_percent,
        financial_rating=rating,
        today_spent=round(today_expense, 2),
        daily_limit=daily_limit,
        daily_remaining=daily_remaining,
    )
