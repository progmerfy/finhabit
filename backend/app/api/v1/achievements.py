from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.achievement import Achievement, UserAchievement
from app.repositories.income_repo import IncomeRepository
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.goal_repo import GoalRepository
from app.services.gamification import GamificationService
from app.schemas.achievement import AchievementResponse

router = APIRouter()


@router.get("", response_model=list[AchievementResponse])
async def get_achievements(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Achievement))
    achievements = result.scalars().all()

    ua_result = await db.execute(
        select(UserAchievement).where(UserAchievement.user_id == user.id)
    )
    unlocked = {ua.achievement_id for ua in ua_result.scalars().all()}

    return [
        AchievementResponse(
            id=str(a.id),
            name=a.name,
            description=a.description,
            icon=a.icon,
            unlocked=a.id in unlocked,
            unlocked_at=next((ua.unlocked_at for ua in ua_result.scalars().all() if ua.achievement_id == a.id), None),
        )
        for a in achievements
    ]


@router.post("/check")
async def check_achievements(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    income_repo = IncomeRepository(db)
    expense_repo = ExpenseRepository(db)
    goal_repo = GoalRepository(db)
    service = GamificationService(db, income_repo, expense_repo, goal_repo)
    new_achievements = await service.check_achievements(user)
    return {
        "new_achievements": [
            AchievementResponse(
                id=str(a.id),
                name=a.name,
                description=a.description,
                icon=a.icon,
                unlocked=True,
            )
            for a in new_achievements
        ]
    }


@router.post("/streak")
async def update_streak(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    income_repo = IncomeRepository(db)
    expense_repo = ExpenseRepository(db)
    goal_repo = GoalRepository(db)
    service = GamificationService(db, income_repo, expense_repo, goal_repo)
    user = await service.update_streak(user)
    await service.check_achievements(user)
    return {"streak_days": user.streak_days, "level": user.level, "experience": user.experience}
