import uuid
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.achievement import Achievement, UserAchievement
from app.models.goal import SavingGoal
from app.repositories.income_repo import IncomeRepository
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.goal_repo import GoalRepository


class GamificationService:
    LEVELS = [
        ("Новичок", 0),
        ("Экономный", 100),
        ("Финансово грамотный", 300),
        ("Инвестор", 700),
        ("Финансово независимый", 1500),
    ]

    def __init__(self, session: AsyncSession, income_repo: IncomeRepository, expense_repo: ExpenseRepository, goal_repo: GoalRepository):
        self.session = session
        self.income_repo = income_repo
        self.expense_repo = expense_repo
        self.goal_repo = goal_repo

    def get_level(self, experience: int) -> str:
        level = self.LEVELS[0][0]
        for lvl, exp in self.LEVELS:
            if experience >= exp:
                level = lvl
        return level

    async def add_experience(self, user: User, points: int) -> User:
        user.experience += points
        new_level = self.get_level(user.experience)
        user.level = new_level
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_streak(self, user: User) -> User:
        today = date.today()
        if user.last_active_date:
            last = user.last_active_date.date() if isinstance(user.last_active_date, datetime) else user.last_active_date
            if last == today:
                return user
            if last == today - timedelta(days=1):
                user.streak_days += 1
            else:
                user.streak_days = 1
        else:
            user.streak_days = 1
        user.last_active_date = datetime.now()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def check_achievements(self, user: User) -> list[Achievement]:
        unlocked = []
        result = await self.session.execute(
            select(UserAchievement).where(UserAchievement.user_id == user.id)
        )
        existing = {ua.achievement_id for ua in result.scalars().all()}

        achievements_result = await self.session.execute(select(Achievement))
        all_achievements = list(achievements_result.scalars().all())

        goals = await self.goal_repo.get_by_user(user.id)
        total_savings = sum(g.current_amount for g in goals)

        for achievement in all_achievements:
            if achievement.id in existing:
                continue

            earned = False
            if achievement.condition_type == "streak_days":
                earned = user.streak_days >= achievement.condition_value
            elif achievement.condition_type == "first_goal":
                earned = any(g.is_completed for g in goals)
            elif achievement.condition_type == "savings_amount":
                earned = total_savings >= achievement.condition_value
            elif achievement.condition_type == "no_overspend_months":
                earned = False  # Complex logic - simplified

            if earned:
                ua = UserAchievement(user_id=user.id, achievement_id=achievement.id)
                self.session.add(ua)
                unlocked.append(achievement)

        if unlocked:
            await self.session.commit()

        return unlocked
