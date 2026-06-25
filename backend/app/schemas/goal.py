from datetime import date, datetime
from pydantic import BaseModel


class GoalCreate(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0.0
    deadline: date | None = None


class GoalUpdate(BaseModel):
    name: str | None = None
    target_amount: float | None = None
    current_amount: float | None = None
    deadline: date | None = None


class GoalTransactionCreate(BaseModel):
    amount: float
    type: str  # deposit / withdraw


class GoalTransactionResponse(BaseModel):
    id: str
    goal_id: str
    amount: float
    type: str
    created_at: datetime

    class Config:
        from_attributes = True


class GoalResponse(BaseModel):
    id: str
    user_id: str
    name: str
    target_amount: float
    current_amount: float
    deadline: date | None
    is_completed: bool
    progress_percent: float = 0.0
    created_at: datetime

    class Config:
        from_attributes = True
