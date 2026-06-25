import uuid
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.budget import Budget
from app.repositories.budget_repo import BudgetRepository
from app.repositories.expense_repo import ExpenseRepository
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse

router = APIRouter()


@router.get("", response_model=list[BudgetResponse])
async def get_budgets(
    month: int | None = None,
    year: int | None = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    today = date.today()
    month = month or today.month
    year = year or today.year

    budget_repo = BudgetRepository(db)
    expense_repo = ExpenseRepository(db)

    budgets = await budget_repo.get_by_user_month(user.id, month, year)
    result = []
    for b in budgets:
        spent = await expense_repo.get_category_total_for_month(user.id, b.category_name, year, month)
        usage = round(spent / b.limit_amount * 100, 1) if b.limit_amount > 0 else 0
        result.append(
            BudgetResponse(
                id=str(b.id),
                user_id=str(b.user_id),
                category_name=b.category_name,
                month=b.month,
                year=b.year,
                limit_amount=b.limit_amount,
                spent=round(spent, 2),
                usage_percent=usage,
            )
        )
    return result


@router.post("", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_budget(
    data: BudgetCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BudgetRepository(db)
    existing = await repo.get_by_category(user.id, data.category_name, data.month, data.year)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget already exists for this category and month")

    budget = Budget(
        user_id=user.id,
        category_name=data.category_name,
        month=data.month,
        year=data.year,
        limit_amount=data.limit_amount,
    )
    budget = await repo.create(budget)
    return BudgetResponse(
        id=str(budget.id),
        user_id=str(budget.user_id),
        category_name=budget.category_name,
        month=budget.month,
        year=budget.year,
        limit_amount=budget.limit_amount,
        spent=0.0,
        usage_percent=0.0,
    )


@router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    data: BudgetUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BudgetRepository(db)
    expense_repo = ExpenseRepository(db)
    budget = await repo.get_by_id(uuid.UUID(budget_id))
    if not budget or budget.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

    budget.limit_amount = data.limit_amount
    budget = await repo.update(budget)

    spent = await expense_repo.get_category_total_for_month(user.id, budget.category_name, budget.year, budget.month)
    usage = round(spent / budget.limit_amount * 100, 1) if budget.limit_amount > 0 else 0
    return BudgetResponse(
        id=str(budget.id),
        user_id=str(budget.user_id),
        category_name=budget.category_name,
        month=budget.month,
        year=budget.year,
        limit_amount=budget.limit_amount,
        spent=round(spent, 2),
        usage_percent=usage,
    )


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BudgetRepository(db)
    budget = await repo.get_by_id(uuid.UUID(budget_id))
    if not budget or budget.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    await repo.delete(budget)
