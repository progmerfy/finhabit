import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.income import Income, IncomeCategory
from app.repositories.income_repo import IncomeRepository
from app.schemas.income import IncomeCreate, IncomeUpdate, IncomeResponse, IncomeCategoryResponse

router = APIRouter()


@router.get("/categories", response_model=list[IncomeCategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    repo = IncomeRepository(db)
    categories = await repo.get_categories()
    return [IncomeCategoryResponse(id=str(c.id), name=c.name, icon=c.icon) for c in categories]


@router.get("", response_model=list[IncomeResponse])
async def get_incomes(
    limit: int = 100,
    offset: int = 0,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = IncomeRepository(db)
    incomes = await repo.get_by_user(user.id, limit, offset)
    result = []
    for inc in incomes:
        result.append(
            IncomeResponse(
                id=str(inc.id),
                user_id=str(inc.user_id),
                category_id=str(inc.category_id),
                category=IncomeCategoryResponse(id=str(inc.category.id), name=inc.category.name, icon=inc.category.icon) if inc.category else None,
                amount=inc.amount,
                comment=inc.comment,
                date=inc.date,
                created_at=inc.created_at,
            )
        )
    return result


@router.post("", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
async def create_income(
    data: IncomeCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = IncomeRepository(db)
    income = Income(
        user_id=user.id,
        category_id=uuid.UUID(data.category_id),
        amount=data.amount,
        comment=data.comment,
        date=data.date,
    )
    income = await repo.create(income)
    return IncomeResponse(
        id=str(income.id),
        user_id=str(income.user_id),
        category_id=str(income.category_id),
        category=IncomeCategoryResponse(id=str(income.category.id), name=income.category.name, icon=income.category.icon) if income.category else None,
        amount=income.amount,
        comment=income.comment,
        date=income.date,
        created_at=income.created_at,
    )


@router.put("/{income_id}", response_model=IncomeResponse)
async def update_income(
    income_id: str,
    data: IncomeUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = IncomeRepository(db)
    income = await repo.get_by_id(uuid.UUID(income_id))
    if not income or income.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")

    if data.amount is not None:
        income.amount = data.amount
    if data.comment is not None:
        income.comment = data.comment
    if data.date is not None:
        income.date = data.date
    if data.category_id is not None:
        income.category_id = uuid.UUID(data.category_id)

    income = await repo.update(income)
    return IncomeResponse(
        id=str(income.id),
        user_id=str(income.user_id),
        category_id=str(income.category_id),
        category=IncomeCategoryResponse(id=str(income.category.id), name=income.category.name, icon=income.category.icon) if income.category else None,
        amount=income.amount,
        comment=income.comment,
        date=income.date,
        created_at=income.created_at,
    )


@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_income(
    income_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = IncomeRepository(db)
    income = await repo.get_by_id(uuid.UUID(income_id))
    if not income or income.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    await repo.delete(income)
