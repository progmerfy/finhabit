from datetime import datetime
from pydantic import BaseModel


class AchievementResponse(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    unlocked: bool = False
    unlocked_at: datetime | None = None

    class Config:
        from_attributes = True
