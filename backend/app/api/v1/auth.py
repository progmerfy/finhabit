import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/login", response_model=UserResponse)
async def telegram_login(data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_telegram_id(data.telegram_id)

    if not user:
        user = User(
            telegram_id=data.telegram_id,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            photo_url=data.photo_url,
        )
        user = await repo.create(user)
    else:
        if data.username:
            user.username = data.username
        if data.first_name:
            user.first_name = data.first_name
        if data.last_name:
            user.last_name = data.last_name
        if data.photo_url:
            user.photo_url = data.photo_url
        user = await repo.update(user)

    return UserResponse(
        id=str(user.id),
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        photo_url=user.photo_url,
        level=user.level,
        experience=user.experience,
        streak_days=user.streak_days,
        preferred_currency=user.preferred_currency,
        created_at=user.created_at,
    )
