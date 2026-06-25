from pydantic import BaseModel


class BudgetCreate(BaseModel):
    category_name: str
    month: int
    year: int
    limit_amount: float


class BudgetUpdate(BaseModel):
    limit_amount: float


class BudgetResponse(BaseModel):
    id: str
    user_id: str
    category_name: str
    month: int
    year: int
    limit_amount: float
    spent: float = 0.0
    usage_percent: float = 0.0

    class Config:
        from_attributes = True
