import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.budget_repo import BudgetRepository
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationResponse

router = APIRouter()


@router.get("", response_model=list[NotificationResponse])
async def get_notifications(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    expense_repo = ExpenseRepository(db)
    budget_repo = BudgetRepository(db)
    service = NotificationService(db, expense_repo, budget_repo)
    notifications = await service.get_user_notifications(user.id)
    return [
        NotificationResponse(
            id=str(n.id),
            user_id=str(n.user_id),
            type=n.type,
            title=n.title,
            message=n.message,
            is_read=n.is_read,
            created_at=n.created_at,
        )
        for n in notifications
    ]


@router.post("/daily", response_model=NotificationResponse)
async def get_daily_report(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    expense_repo = ExpenseRepository(db)
    budget_repo = BudgetRepository(db)
    service = NotificationService(db, expense_repo, budget_repo)
    notification = await service.generate_daily_report(user)
    return NotificationResponse(
        id=str(notification.id),
        user_id=str(notification.user_id),
        type=notification.type,
        title=notification.title,
        message=notification.message,
        is_read=notification.is_read,
        created_at=notification.created_at,
    )


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_read(
    notification_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    expense_repo = ExpenseRepository(db)
    budget_repo = BudgetRepository(db)
    service = NotificationService(db, expense_repo, budget_repo)
    notification = await service.mark_read(uuid.UUID(notification_id))
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return NotificationResponse(
        id=str(notification.id),
        user_id=str(notification.user_id),
        type=notification.type,
        title=notification.title,
        message=notification.message,
        is_read=notification.is_read,
        created_at=notification.created_at,
    )
