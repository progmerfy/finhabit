import uuid
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.notification import Notification
from app.models.user import User
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.budget_repo import BudgetRepository


class NotificationService:
    def __init__(self, session: AsyncSession, expense_repo: ExpenseRepository, budget_repo: BudgetRepository):
        self.session = session
        self.expense_repo = expense_repo
        self.budget_repo = budget_repo

    async def create_notification(self, user_id: uuid.UUID, type: str, title: str, message: str) -> Notification:
        notification = Notification(
            user_id=user_id, type=type, title=title, message=message
        )
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def get_user_notifications(self, user_id: uuid.UUID, limit: int = 20) -> list[Notification]:
        result = await self.session.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def mark_read(self, notification_id: uuid.UUID) -> Notification | None:
        result = await self.session.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        notification = result.scalar_one_or_none()
        if notification:
            notification.is_read = True
            await self.session.commit()
            await self.session.refresh(notification)
        return notification

    async def generate_daily_report(self, user: User) -> Notification:
        today = date.today()
        today_expense = await self.expense_repo.get_total_by_period(
            user.id, today, today
        )

        budgets = await self.budget_repo.get_by_user_month(
            user.id, today.month, today.year
        )
        total_budget = sum(b.limit_amount for b in budgets) if budgets else 0
        daily_limit = round(total_budget / 30, 2) if total_budget > 0 else 0
        remaining = round(daily_limit - today_expense, 2)

        title = "Ежедневный отчет"
        message = (
            f"Сегодня потрачено: {today_expense:.2f} EUR\n"
            f"Дневной лимит: {daily_limit:.2f} EUR\n"
            f"Остаток: {remaining:.2f} EUR"
        )
        return await self.create_notification(user.id, "daily", title, message)

    async def check_budget_alerts(self, user_id: uuid.UUID) -> list[Notification]:
        today = date.today()
        alerts = []
        budgets = await self.budget_repo.get_by_user_month(
            user_id, today.month, today.year
        )

        for budget in budgets:
            spent = await self.expense_repo.get_category_total_for_month(
                user_id, budget.category_name, today.year, today.month
            )
            if budget.limit_amount > 0:
                usage = spent / budget.limit_amount * 100
                if usage >= 100:
                    n = await self.create_notification(
                        user_id, "alert",
                        "Превышение бюджета!",
                        f"Бюджет на «{budget.category_name}» превышен! "
                        f"Потрачено: {spent:.0f} EUR из {budget.limit_amount:.0f} EUR ({usage:.0f}%)."
                    )
                    alerts.append(n)
                elif usage >= 80:
                    n = await self.create_notification(
                        user_id, "alert",
                        "Близок к превышению бюджета",
                        f"Бюджет на «{budget.category_name}» использован на {usage:.0f}%. "
                        f"Потрачено: {spent:.0f} EUR из {budget.limit_amount:.0f} EUR."
                    )
                    alerts.append(n)

        return alerts
