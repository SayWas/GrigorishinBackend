from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base_db_adapter import base_get, base_create_update
from models import Course, Country


class SQLAlchemyCoursesAdapter:
    session: AsyncSession

    def __init__(self,
                 session: AsyncSession,
                 ):
        self.session = session

    async def get_course(self, course_id: int) -> Course:
        statement = select(Course).where(Course.id == course_id)
        return await base_get(self.session, statement)

    async def get_courses(self, country_name: str) -> List[Course]:
        if country_name:
            statement = select(Course).join(Country).where(Country.name == country_name)
            # statement = select(Course).where(Course.country_name == country_name)
        else:
            statement = select(Course)
        statement = statement.order_by(Course.starting_at.desc())
        return await base_get(self.session, statement, one_scalar=False)

    async def create_course(self, course_dict: Dict[str, Any]) -> Course:
        course = Course(**course_dict)
        await base_create_update(self.session, course)

        course = await self.get_course(course.id)
        return course

    async def update_course(self, update_course: Course, update_dict: Dict[str, Any]) -> Course:
        for key, value in update_dict.items():
            if value is None:
                continue
            setattr(update_course, key, value)
        await base_create_update(self.session, update_course)

        course = await self.get_course(update_course.id)
        return course

    async def delete_course(self, course: Course) -> None:
        await self.session.delete(course)
        await self.session.commit()
