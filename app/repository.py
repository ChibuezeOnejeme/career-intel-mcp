from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Candidate


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, model: Any, id: str) -> Any:
        result = await self.session.execute(select(model).where(model.id == id))
        return result.scalar_one_or_none()

    async def list(self, model: Any, limit: int = 100, offset: int = 0) -> list[Any]:
        result = await self.session.execute(select(model).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def create(self, instance: Any) -> Any:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: Any) -> Any:
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: Any) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    async def count(self, model: Any) -> int:
        from sqlalchemy import func, select

        result = await self.session.execute(select(func.count(model.id)))
        return result.scalar() or 0


class CandidateRepository(BaseRepository):
    async def find_by_email(self, email: str) -> Candidate | None:
        result = await self.session.execute(
            select(Candidate).where(Candidate.email == email)
        )
        return result.scalar_one_or_none()

    async def search_by_skills(self, skills: list[str], limit: int = 20) -> list[Candidate]:
        result = await self.session.execute(select(Candidate).limit(limit))
        return list(result.scalars().all())
