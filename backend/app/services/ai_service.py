import uuid
from datetime import date, timedelta
from app.repositories.income_repo import IncomeRepository
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.goal_repo import GoalRepository
from app.models.ai_report import AIReport


class AIService:
    def __init__(self, income_repo: IncomeRepository, expense_repo: ExpenseRepository, goal_repo: GoalRepository, session=None):
        self.income_repo = income_repo
        self.expense_repo = expense_repo
        self.goal_repo = goal_repo
        self.session = session
        self.openai_api_key = ""

    def set_openai_key(self, key: str):
        self.openai_api_key = key

    async def generate_report(self, user_id: uuid.UUID, report_type: str = "on_demand") -> str:
        today = date.today()
        month_start = today.replace(day=1)
        prev_month_end = month_start - timedelta(days=1)
        prev_month_start = prev_month_end.replace(day=1)

        income = await self.income_repo.get_total_by_period(user_id, month_start, today)
        expense = await self.expense_repo.get_total_by_period(user_id, month_start, today)
        prev_income = await self.income_repo.get_total_by_period(user_id, prev_month_start, prev_month_end)
        prev_expense = await self.expense_repo.get_total_by_period(user_id, prev_month_start, prev_month_end)

        category_data = await self.expense_repo.get_category_totals(user_id, month_start, today)
        goals = await self.goal_repo.get_by_user(user_id)
        total_savings = sum(g.current_amount for g in goals if not g.is_completed)

        report_parts = []

        if expense > 0:
            for cat in category_data[:3]:
                pct = round(cat["amount"] / expense * 100, 1)
                report_parts.append(f"Вы тратите {pct}% бюджета на {cat['category_name']} ({cat['amount']:.0f} EUR).")

        if prev_expense > 0:
            change = round((expense - prev_expense) / prev_expense * 100, 1)
            if change > 0:
                report_parts.append(f"За последний месяц расходы выросли на {change}%.")
            elif change < 0:
                report_parts.append(f"За последний месяц расходы снизились на {abs(change)}%.")

        if income > 0:
            savings_rate = round((income - expense) / income * 100, 1)
            report_parts.append(f"Норма сбережения: {savings_rate}% от дохода.")

        if total_savings > 0:
            report_parts.append(f"Всего накоплено: {total_savings:.0f} EUR.")

        # Savings suggestion
        entertainment = next((c for c in category_data if c["category_name"] == "развлечения"), None)
        if entertainment:
            reduction = entertainment["amount"] * 0.2
            report_parts.append(
                f"Если сократить расходы на развлечения на 20%, вы сможете откладывать "
                f"дополнительно {reduction:.0f} EUR в месяц."
            )

        if not report_parts:
            report_parts.append("Добавьте больше транзакций для получения персональных рекомендаций.")

        report = "\n".join(report_parts)

        if self.openai_api_key:
            try:
                from openai import AsyncOpenAI

                client = AsyncOpenAI(api_key=self.openai_api_key)
                prompt = (
                    f"Ты финансовый советник. Проанализируй данные пользователя за текущий месяц:\n"
                    f"Доход: {income} EUR\nРасход: {expense} EUR\n"
                    f"Топ категории расходов: {[(c['category_name'], c['amount']) for c in category_data]}\n"
                    f"Накопления: {total_savings} EUR\n"
                    f"Дай 2-3 коротких рекомендации на русском языке."
                )
                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                )
                ai_result = response.choices[0].message.content
                if ai_result:
                    report = ai_result
            except Exception:
                pass

        return report

    async def save_report(self, user_id: uuid.UUID, content: str, report_type: str = "on_demand") -> AIReport:
        report = AIReport(user_id=user_id, content=content, report_type=report_type)
        if self.session:
            self.session.add(report)
            await self.session.commit()
            await self.session.refresh(report)
        return report
