import uuid
from datetime import date
from sqlalchemy import select, func, and_
from app.models.income import Income, IncomeCategory
from app.repositories.base import BaseRepository


class IncomeRepository(BaseRepository):
    async def get_categories(self) -> list[IncomeCategory]:
        result = await self.session.execute(select(IncomeCategory))
        return list(result.scalars().all())

    async def get_by_user(self, user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> list[Income]:
        result = await self.session.execute(
            select(Income).where(Income.user_id == user_id).order_by(Income.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_id(self, income_id: uuid.UUID) -> Income | None:
        result = await self.session.execute(select(Income).where(Income.id == income_id))
        return result.scalar_one_or_none()

    async def create(self, income: Income) -> Income:
        self.session.add(income)
        await self.session.commit()
        await self.session.refresh(income)
        return income

    async def update(self, income: Income) -> Income:
        await self.session.commit()
        await self.session.refresh(income)
        return income

    async def delete(self, income: Income) -> None:
        await self.session.delete(income)
        await self.session.commit()

    async def get_monthly_total(self, user_id: uuid.UUID, year: int, month: int) -> float:
        result = await self.session.execute(
            select(func.coalesce(func.sum(Income.amount), 0)).where(
                and_(
                    Income.user_id == user_id,
                    func.extract("year", Income.date) == year,
                    func.extract("month", Income.date) == month,
                )
            )
        )
        return float(result.scalar())

    async def get_by_period(self, user_id: uuid.UUID, start: date, end: date) -> list[Income]:
        result = await self.session.execute(
            select(Income).where(and_(Income.user_id == user_id, Income.date >= start, Income.date <= end))
        )
        return list(result.scalars().all())

    async def get_total_by_period(self, user_id: uuid.UUID, start: date, end: date) -> float:
        result = await self.session.execute(
            select(func.coalesce(func.sum(Income.amount), 0)).where(
                and_(Income.user_id == user_id, Income.date >= start, Income.date <= end)
            )
        )
        return float(result.scalar())
