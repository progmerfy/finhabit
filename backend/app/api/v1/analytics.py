from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.income_repo import IncomeRepository
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.goal_repo import GoalRepository
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsResponse, BalanceHistory, MonthlyAnalytics

router = APIRouter()


@router.get("", response_model=AnalyticsResponse)
async def get_analytics(
    period: str = "month",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    income_repo = IncomeRepository(db)
    expense_repo = ExpenseRepository(db)
    goal_repo = GoalRepository(db)
    service = AnalyticsService(income_repo, expense_repo, goal_repo)
    return await service.get_analytics(user.id, period)


@router.get("/balance-history", response_model=list[BalanceHistory])
async def get_balance_history(
    months: int = 6,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    income_repo = IncomeRepository(db)
    expense_repo = ExpenseRepository(db)
    goal_repo = GoalRepository(db)
    service = AnalyticsService(income_repo, expense_repo, goal_repo)
    return await service.get_balance_history(user.id, months)


@router.get("/monthly", response_model=list[MonthlyAnalytics])
async def get_monthly_analytics(
    months: int = 6,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    income_repo = IncomeRepository(db)
    expense_repo = ExpenseRepository(db)
    goal_repo = GoalRepository(db)
    service = AnalyticsService(income_repo, expense_repo, goal_repo)
    return await service.get_monthly_analytics(user.id, months)
