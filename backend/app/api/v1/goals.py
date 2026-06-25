import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.goal import SavingGoal, GoalTransaction
from app.repositories.goal_repo import GoalRepository
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse, GoalTransactionCreate, GoalTransactionResponse

router = APIRouter()


@router.get("", response_model=list[GoalResponse])
async def get_goals(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GoalRepository(db)
    goals = await repo.get_by_user(user.id)
    return [
        GoalResponse(
            id=str(g.id),
            user_id=str(g.user_id),
            name=g.name,
            target_amount=g.target_amount,
            current_amount=g.current_amount,
            deadline=g.deadline,
            is_completed=g.is_completed,
            progress_percent=round(g.current_amount / g.target_amount * 100, 1) if g.target_amount > 0 else 0,
            created_at=g.created_at,
        )
        for g in goals
    ]


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    data: GoalCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GoalRepository(db)
    goal = SavingGoal(
        user_id=user.id,
        name=data.name,
        target_amount=data.target_amount,
        current_amount=data.current_amount,
        deadline=data.deadline,
    )
    goal = await repo.create(goal)
    return GoalResponse(
        id=str(goal.id),
        user_id=str(goal.user_id),
        name=goal.name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        deadline=goal.deadline,
        is_completed=goal.is_completed,
        progress_percent=round(goal.current_amount / goal.target_amount * 100, 1) if goal.target_amount > 0 else 0,
        created_at=goal.created_at,
    )


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: str,
    data: GoalUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GoalRepository(db)
    goal = await repo.get_by_id(uuid.UUID(goal_id))
    if not goal or goal.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    if data.name is not None:
        goal.name = data.name
    if data.target_amount is not None:
        goal.target_amount = data.target_amount
    if data.current_amount is not None:
        goal.current_amount = data.current_amount
    if data.deadline is not None:
        goal.deadline = data.deadline
    if goal.target_amount > 0 and goal.current_amount >= goal.target_amount:
        goal.is_completed = True

    goal = await repo.update(goal)
    return GoalResponse(
        id=str(goal.id),
        user_id=str(goal.user_id),
        name=goal.name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        deadline=goal.deadline,
        is_completed=goal.is_completed,
        progress_percent=round(goal.current_amount / goal.target_amount * 100, 1) if goal.target_amount > 0 else 0,
        created_at=goal.created_at,
    )


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GoalRepository(db)
    goal = await repo.get_by_id(uuid.UUID(goal_id))
    if not goal or goal.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    await repo.delete(goal)


@router.post("/{goal_id}/transactions", response_model=GoalTransactionResponse)
async def add_goal_transaction(
    goal_id: str,
    data: GoalTransactionCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GoalRepository(db)
    goal = await repo.get_by_id(uuid.UUID(goal_id))
    if not goal or goal.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    txn = GoalTransaction(goal_id=goal.id, amount=data.amount, type=data.type)
    txn = await repo.create_transaction(txn)

    if data.type == "deposit":
        goal.current_amount += data.amount
    else:
        goal.current_amount = max(0, goal.current_amount - data.amount)

    if goal.target_amount > 0 and goal.current_amount >= goal.target_amount:
        goal.is_completed = True

    await repo.update(goal)

    return GoalTransactionResponse(
        id=str(txn.id),
        goal_id=str(txn.goal_id),
        amount=txn.amount,
        type=txn.type,
        created_at=txn.created_at,
    )


@router.get("/{goal_id}/transactions", response_model=list[GoalTransactionResponse])
async def get_goal_transactions(
    goal_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GoalRepository(db)
    goal = await repo.get_by_id(uuid.UUID(goal_id))
    if not goal or goal.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")

    result = await db.execute(
        select(GoalTransaction).where(GoalTransaction.goal_id == goal.id).order_by(GoalTransaction.created_at.desc())
    )
    txns = result.scalars().all()
    return [
        GoalTransactionResponse(
            id=str(t.id), goal_id=str(t.goal_id), amount=t.amount, type=t.type, created_at=t.created_at
        )
        for t in txns
    ]
