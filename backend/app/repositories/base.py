from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
