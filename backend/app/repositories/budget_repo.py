import uuid
from sqlalchemy import select, and_
from app.models.budget import Budget
from app.repositories.base import BaseRepository


class BudgetRepository(BaseRepository):
    async def get_by_user_month(self, user_id: uuid.UUID, month: int, year: int) -> list[Budget]:
        result = await self.session.execute(
            select(Budget).where(and_(Budget.user_id == user_id, Budget.month == month, Budget.year == year))
        )
        return list(result.scalars().all())

    async def get_by_id(self, budget_id: uuid.UUID) -> Budget | None:
        result = await self.session.execute(select(Budget).where(Budget.id == budget_id))
        return result.scalar_one_or_none()

    async def get_by_category(self, user_id: uuid.UUID, category_name: str, month: int, year: int) -> Budget | None:
        result = await self.session.execute(
            select(Budget).where(
                and_(
                    Budget.user_id == user_id,
                    Budget.category_name == category_name,
                    Budget.month == month,
                    Budget.year == year,
                )
            )
        )
        return result.scalar_one_or_none()

    async def create(self, budget: Budget) -> Budget:
        self.session.add(budget)
        await self.session.commit()
        await self.session.refresh(budget)
        return budget

    async def update(self, budget: Budget) -> Budget:
        await self.session.commit()
        await self.session.refresh(budget)
        return budget

    async def delete(self, budget: Budget) -> None:
        await self.session.delete(budget)
        await self.session.commit()
