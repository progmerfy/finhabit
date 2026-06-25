from datetime import date, datetime
from pydantic import BaseModel


class ExpenseCategoryResponse(BaseModel):
    id: str
    name: str
    icon: str

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    category_id: str
    amount: float
    description: str | None = None
    date: date


class ExpenseUpdate(BaseModel):
    category_id: str | None = None
    amount: float | None = None
    description: str | None = None
    date: date | None = None


class ExpenseResponse(BaseModel):
    id: str
    user_id: str
    category_id: str
    category: ExpenseCategoryResponse | None = None
    amount: float
    description: str | None
    date: date
    created_at: datetime

    class Config:
        from_attributes = True
