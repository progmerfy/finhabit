from datetime import date, datetime
from pydantic import BaseModel


class IncomeCategoryResponse(BaseModel):
    id: str
    name: str
    icon: str

    class Config:
        from_attributes = True


class IncomeCreate(BaseModel):
    category_id: str
    amount: float
    comment: str | None = None
    date: date


class IncomeUpdate(BaseModel):
    category_id: str | None = None
    amount: float | None = None
    comment: str | None = None
    date: date | None = None


class IncomeResponse(BaseModel):
    id: str
    user_id: str
    category_id: str
    category: IncomeCategoryResponse | None = None
    amount: float
    comment: str | None
    date: date
    created_at: datetime

    class Config:
        from_attributes = True
