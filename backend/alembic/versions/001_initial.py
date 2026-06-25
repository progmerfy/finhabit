"""initial migration

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("telegram_id", sa.Integer(), unique=True, nullable=False),
        sa.Column("username", sa.String(128), nullable=True),
        sa.Column("first_name", sa.String(128), nullable=True),
        sa.Column("last_name", sa.String(128), nullable=True),
        sa.Column("photo_url", sa.String(512), nullable=True),
        sa.Column("level", sa.String(32), server_default="новичок"),
        sa.Column("experience", sa.Integer(), server_default="0"),
        sa.Column("streak_days", sa.Integer(), server_default="0"),
        sa.Column("last_active_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("preferred_currency", sa.String(8), server_default="EUR"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "income_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(64), unique=True, nullable=False),
        sa.Column("icon", sa.String(16), server_default="💰"),
    )

    op.create_table(
        "expense_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(64), unique=True, nullable=False),
        sa.Column("icon", sa.String(16), server_default="💳"),
    )

    op.create_table(
        "income",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("income_categories.id"), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("comment", sa.String(512), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "expenses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("expense_categories.id"), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("description", sa.String(512), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "saving_goals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("target_amount", sa.Float(), nullable=False),
        sa.Column("current_amount", sa.Float(), server_default="0"),
        sa.Column("deadline", sa.Date(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "goal_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("goal_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("saving_goals.id"), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("type", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "budgets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("category_name", sa.String(64), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("limit_amount", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("message", sa.String(2048), nullable=False),
        sa.Column("is_read", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "ai_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("report_type", sa.String(32), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "achievements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(128), unique=True, nullable=False),
        sa.Column("description", sa.String(512), nullable=False),
        sa.Column("icon", sa.String(16), server_default="🏆"),
        sa.Column("condition_type", sa.String(32), nullable=False),
        sa.Column("condition_value", sa.Integer(), nullable=False),
    )

    op.create_table(
        "user_achievements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("achievement_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("achievements.id"), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Seed categories
    income_cats = [
        ("зарплата", "💼"), ("фриланс", "💻"), ("бизнес", "🏪"),
        ("инвестиции", "📈"), ("подарки", "🎁"), ("другое", "💰"),
    ]
    for name, icon in income_cats:
        op.execute(f"INSERT INTO income_categories (id, name, icon) VALUES (gen_random_uuid(), '{name}', '{icon}')")

    expense_cats = [
        ("продукты", "🛒"), ("кафе", "☕"), ("транспорт", "🚌"),
        ("аренда", "🏠"), ("коммунальные услуги", "⚡"), ("подписки", "📱"),
        ("развлечения", "🎮"), ("путешествия", "✈️"), ("спорт", "🏋️"),
        ("медицина", "💊"), ("образование", "📚"), ("другое", "💳"),
    ]
    for name, icon in expense_cats:
        op.execute(f"INSERT INTO expense_categories (id, name, icon) VALUES (gen_random_uuid(), '{name}', '{icon}')")

    # Seed achievements
    achievements = [
        ("30 дней учета подряд", "Ведите учет 30 дней подряд", "🔥", "streak_days", 30),
        ("Первая цель выполнена", "Достигните первой финансовой цели", "🎯", "first_goal", 1),
        ("Накоплено 1000 EUR", "Накопите 1000 EUR", "💵", "savings_amount", 1000),
        ("Накоплено 5000 EUR", "Накопите 5000 EUR", "💎", "savings_amount", 5000),
        ("6 месяцев без перерасхода", "Не превышайте бюджет 6 месяцев подряд", "🛡️", "no_overspend_months", 6),
    ]
    for name, desc, icon, cond_type, cond_val in achievements:
        op.execute(
            f"INSERT INTO achievements (id, name, description, icon, condition_type, condition_value) "
            f"VALUES (gen_random_uuid(), '{name}', '{desc}', '{icon}', '{cond_type}', {cond_val})"
        )


def downgrade() -> None:
    op.drop_table("user_achievements")
    op.drop_table("achievements")
    op.drop_table("ai_reports")
    op.drop_table("notifications")
    op.drop_table("budgets")
    op.drop_table("goal_transactions")
    op.drop_table("saving_goals")
    op.drop_table("expenses")
    op.drop_table("income")
    op.drop_table("expense_categories")
    op.drop_table("income_categories")
    op.drop_table("users")
