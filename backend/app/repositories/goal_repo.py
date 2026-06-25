import uuid
from sqlalchemy import select, func
from app.models.goal import SavingGoal, GoalTransaction
from app.repositories.base import BaseRepository


class GoalRepository(BaseRepository):
    async def get_by_user(self, user_id: uuid.UUID) -> list[SavingGoal]:
        result = await self.session.execute(
            select(SavingGoal).where(SavingGoal.user_id == user_id).order_by(SavingGoal.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, goal_id: uuid.UUID) -> SavingGoal | None:
        result = await self.session.execute(select(SavingGoal).where(SavingGoal.id == goal_id))
        return result.scalar_one_or_none()

    async def create(self, goal: SavingGoal) -> SavingGoal:
        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def update(self, goal: SavingGoal) -> SavingGoal:
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def delete(self, goal: SavingGoal) -> None:
        await self.session.delete(goal)
        await self.session.commit()

    async def get_total_savings(self, user_id: uuid.UUID) -> float:
        result = await self.session.execute(
            select(func.coalesce(func.sum(SavingGoal.current_amount), 0)).where(
                SavingGoal.user_id == user_id, SavingGoal.is_completed.is_(False)
            )
        )
        return float(result.scalar())

    async def create_transaction(self, txn: GoalTransaction) -> GoalTransaction:
        self.session.add(txn)
        await self.session.commit()
        await self.session.refresh(txn)
        return txn
