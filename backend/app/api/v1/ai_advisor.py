from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.income_repo import IncomeRepository
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.goal_repo import GoalRepository
from app.services.ai_service import AIService
from app.config import settings

router = APIRouter()


@router.get("/report")
async def get_ai_report(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    income_repo = IncomeRepository(db)
    expense_repo = ExpenseRepository(db)
    goal_repo = GoalRepository(db)
    service = AIService(income_repo, expense_repo, goal_repo)
    if settings.openai_api_key:
        service.set_openai_key(settings.openai_api_key)
    report = await service.generate_report(user.id)
    return {"report": report}
