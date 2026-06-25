import uuid
from datetime import date
from sqlalchemy import select, func, and_
from app.models.expense import Expense, ExpenseCategory
from app.repositories.base import BaseRepository


class ExpenseRepository(BaseRepository):
    async def get_categories(self) -> list[ExpenseCategory]:
        result = await self.session.execute(select(ExpenseCategory))
        return list(result.scalars().all())

    async def get_by_user(self, user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> list[Expense]:
        result = await self.session.execute(
            select(Expense).where(Expense.user_id == user_id).order_by(Expense.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_id(self, expense_id: uuid.UUID) -> Expense | None:
        result = await self.session.execute(select(Expense).where(Expense.id == expense_id))
        return result.scalar_one_or_none()

    async def create(self, expense: Expense) -> Expense:
        self.session.add(expense)
        await self.session.commit()
        await self.session.refresh(expense)
        return expense

    async def update(self, expense: Expense) -> Expense:
        await self.session.commit()
        await self.session.refresh(expense)
        return expense

    async def delete(self, expense: Expense) -> None:
        await self.session.delete(expense)
        await self.session.commit()

    async def get_monthly_total(self, user_id: uuid.UUID, year: int, month: int) -> float:
        result = await self.session.execute(
            select(func.coalesce(func.sum(Expense.amount), 0)).where(
                and_(
                    Expense.user_id == user_id,
                    func.extract("year", Expense.date) == year,
                    func.extract("month", Expense.date) == month,
                )
            )
        )
        return float(result.scalar())

    async def get_category_totals(self, user_id: uuid.UUID, start: date, end: date) -> list[dict]:
        result = await self.session.execute(
            select(
                ExpenseCategory.name,
                ExpenseCategory.icon,
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
                func.count(Expense.id).label("count"),
            )
            .join(ExpenseCategory, Expense.category_id == ExpenseCategory.id)
            .where(and_(Expense.user_id == user_id, Expense.date >= start, Expense.date <= end))
            .group_by(ExpenseCategory.name, ExpenseCategory.icon)
            .order_by(func.sum(Expense.amount).desc())
        )
        rows = result.all()
        return [{"category_name": r[0], "icon": r[1], "amount": float(r[2]), "count": r[3]} for r in rows]

    async def get_total_by_period(self, user_id: uuid.UUID, start: date, end: date) -> float:
        result = await self.session.execute(
            select(func.coalesce(func.sum(Expense.amount), 0)).where(
                and_(Expense.user_id == user_id, Expense.date >= start, Expense.date <= end)
            )
        )
        return float(result.scalar())

    async def get_by_period(self, user_id: uuid.UUID, start: date, end: date) -> list[Expense]:
        result = await self.session.execute(
            select(Expense).where(and_(Expense.user_id == user_id, Expense.date >= start, Expense.date <= end))
        )
        return list(result.scalars().all())

    async def get_category_total_for_month(self, user_id: uuid.UUID, category_name: str, year: int, month: int) -> float:
        result = await self.session.execute(
            select(func.coalesce(func.sum(Expense.amount), 0))
            .join(ExpenseCategory, Expense.category_id == ExpenseCategory.id)
            .where(
                and_(
                    Expense.user_id == user_id,
                    ExpenseCategory.name == category_name,
                    func.extract("year", Expense.date) == year,
                    func.extract("month", Expense.date) == month,
                )
            )
        )
        return float(result.scalar())
