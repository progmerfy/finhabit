import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.expense import Expense
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.budget_repo import BudgetRepository
from app.services.notification_service import NotificationService
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseCategoryResponse

router = APIRouter()


@router.get("/categories", response_model=list[ExpenseCategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    repo = ExpenseRepository(db)
    categories = await repo.get_categories()
    return [ExpenseCategoryResponse(id=str(c.id), name=c.name, icon=c.icon) for c in categories]


@router.get("", response_model=list[ExpenseResponse])
async def get_expenses(
    limit: int = 100,
    offset: int = 0,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ExpenseRepository(db)
    expenses = await repo.get_by_user(user.id, limit, offset)
    result = []
    for exp in expenses:
        result.append(
            ExpenseResponse(
                id=str(exp.id),
                user_id=str(exp.user_id),
                category_id=str(exp.category_id),
                category=ExpenseCategoryResponse(id=str(exp.category.id), name=exp.category.name, icon=exp.category.icon) if exp.category else None,
                amount=exp.amount,
                description=exp.description,
                date=exp.date,
                created_at=exp.created_at,
            )
        )
    return result


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    data: ExpenseCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    expense_repo = ExpenseRepository(db)
    budget_repo = BudgetRepository(db)
    notification_service = NotificationService(db, expense_repo, budget_repo)

    expense = Expense(
        user_id=user.id,
        category_id=uuid.UUID(data.category_id),
        amount=data.amount,
        description=data.description,
        date=data.date,
    )
    expense = await expense_repo.create(expense)

    await notification_service.check_budget_alerts(user.id)

    return ExpenseResponse(
        id=str(expense.id),
        user_id=str(expense.user_id),
        category_id=str(expense.category_id),
        category=ExpenseCategoryResponse(id=str(expense.category.id), name=expense.category.name, icon=expense.category.icon) if expense.category else None,
        amount=expense.amount,
        description=expense.description,
        date=expense.date,
        created_at=expense.created_at,
    )


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str,
    data: ExpenseUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ExpenseRepository(db)
    expense = await repo.get_by_id(uuid.UUID(expense_id))
    if not expense or expense.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    if data.amount is not None:
        expense.amount = data.amount
    if data.description is not None:
        expense.description = data.description
    if data.date is not None:
        expense.date = data.date
    if data.category_id is not None:
        expense.category_id = uuid.UUID(data.category_id)

    expense = await repo.update(expense)
    return ExpenseResponse(
        id=str(expense.id),
        user_id=str(expense.user_id),
        category_id=str(expense.category_id),
        category=ExpenseCategoryResponse(id=str(expense.category.id), name=expense.category.name, icon=expense.category.icon) if expense.category else None,
        amount=expense.amount,
        description=expense.description,
        date=expense.date,
        created_at=expense.created_at,
    )


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ExpenseRepository(db)
    expense = await repo.get_by_id(uuid.UUID(expense_id))
    if not expense or expense.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    await repo.delete(expense)
