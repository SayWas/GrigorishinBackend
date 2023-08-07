from typing import Any

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession


async def base_get(session: AsyncSession, statement: Select, one_scalar=True) -> Any:
    results = await session.execute(statement)
    if one_scalar:
        return results.unique().scalar_one_or_none()
    return results.unique().scalars().all()


async def base_create_update(session: AsyncSession, model: Any) -> None:
    session.add(model)
    await session.commit()
