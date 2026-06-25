import uuid
from datetime import date, timedelta
from calendar import monthrange

from app.repositories.income_repo import IncomeRepository
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.goal_repo import GoalRepository
from app.schemas.analytics import AnalyticsResponse, CategoryBreakdown, BalanceHistory, MonthlyAnalytics


class AnalyticsService:
    def __init__(self, income_repo: IncomeRepository, expense_repo: ExpenseRepository, goal_repo: GoalRepository):
        self.income_repo = income_repo
        self.expense_repo = expense_repo
        self.goal_repo = goal_repo

    def _get_period_range(self, period: str) -> tuple[date, date, date, date]:
        today = date.today()
        if period == "week":
            start = today - timedelta(days=today.weekday())
            end = today
            prev_end = start - timedelta(days=1)
            prev_start = prev_end - timedelta(days=6)
        elif period == "month":
            start = today.replace(day=1)
            end = today
            prev_end = start - timedelta(days=1)
            prev_start = prev_end.replace(day=1)
        elif period == "quarter":
            quarter_month = ((today.month - 1) // 3) * 3 + 1
            start = today.replace(month=quarter_month, day=1)
            end = today
            prev_end = start - timedelta(days=1)
            prev_quarter_month = ((prev_end.month - 1) // 3) * 3 + 1
            prev_start = prev_end.replace(month=prev_quarter_month, day=1)
        else:  # year
            start = today.replace(month=1, day=1)
            end = today
            prev_end = start - timedelta(days=1)
            prev_start = prev_end.replace(month=1, day=1)
        return start, end, prev_start, prev_end

    async def get_analytics(self, user_id: uuid.UUID, period: str) -> AnalyticsResponse:
        start, end, prev_start, prev_end = self._get_period_range(period)

        total_income = await self.income_repo.get_total_by_period(user_id, start, end)
        total_expense = await self.expense_repo.get_total_by_period(user_id, start, end)
        prev_expense = await self.expense_repo.get_total_by_period(user_id, prev_start, prev_end)

        expenses = await self.expense_repo.get_by_period(user_id, start, end)
        transaction_count = len(expenses)
        average_check = round(total_expense / transaction_count, 2) if transaction_count > 0 else 0

        category_data = await self.expense_repo.get_category_totals(user_id, start, end)
        total = total_expense if total_expense > 0 else 1
        top_categories = [
            CategoryBreakdown(
                category_name=c["category_name"],
                icon=c["icon"],
                amount=round(c["amount"], 2),
                percentage=round(c["amount"] / total * 100, 1),
                transaction_count=c["count"],
            )
            for c in category_data
        ]

        change = 0
        if prev_expense > 0:
            change = round((total_expense - prev_expense) / prev_expense * 100, 1)

        return AnalyticsResponse(
            total_income=round(total_income, 2),
            total_expense=round(total_expense, 2),
            net_savings=round(total_income - total_expense, 2),
            average_check=average_check,
            transaction_count=transaction_count,
            top_categories=top_categories,
            change_vs_last_period=change,
        )

    async def get_balance_history(self, user_id: uuid.UUID, months: int = 6) -> list[BalanceHistory]:
        today = date.today()
        history = []
        running_balance = 0.0

        for i in range(months - 1, -1, -1):
            m = today.month - i
            y = today.year
            while m < 1:
                m += 12
                y -= 1

            month_income = await self.income_repo.get_monthly_total(user_id, y, m)
            month_expense = await self.expense_repo.get_monthly_total(user_id, y, m)
            running_balance += month_income - month_expense

            month_name = date(y, m, 1).strftime("%b %Y")
            history.append(
                BalanceHistory(
                    date=month_name,
                    balance=round(running_balance, 2),
                    income=round(month_income, 2),
                    expense=round(month_expense, 2),
                )
            )

        return history

    async def get_monthly_analytics(self, user_id: uuid.UUID, months: int = 6) -> list[MonthlyAnalytics]:
        today = date.today()
        result = []

        for i in range(months - 1, -1, -1):
            m = today.month - i
            y = today.year
            while m < 1:
                m += 12
                y -= 1

            income = await self.income_repo.get_monthly_total(user_id, y, m)
            expense = await self.expense_repo.get_monthly_total(user_id, y, m)
            month_name = date(y, m, 1).strftime("%b %Y")

            result.append(
                MonthlyAnalytics(
                    month=month_name,
                    income=round(income, 2),
                    expense=round(expense, 2),
                    savings=round(income - expense, 2),
                )
            )

        return result
