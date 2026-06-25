from fastapi import APIRouter

from app.api.v1 import auth, income, expense, goals, budgets, analytics, dashboard, notifications, ai_advisor, achievements

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(income.router, prefix="/income", tags=["Income"])
router.include_router(expense.router, prefix="/expenses", tags=["Expenses"])
router.include_router(goals.router, prefix="/goals", tags=["Goals"])
router.include_router(budgets.router, prefix="/budgets", tags=["Budgets"])
router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
router.include_router(ai_advisor.router, prefix="/ai-advisor", tags=["AI Advisor"])
router.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
