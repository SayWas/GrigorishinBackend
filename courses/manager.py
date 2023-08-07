from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

import courses.exceptions as exceptions
from courses.db_adapter import SQLAlchemyCoursesAdapter
from courses.schemas import CourseRead, CourseCreate, CourseUpdate


class CoursesManager:
    def __init__(self,
                 session: AsyncSession
                 ):
        self.db_adapter = SQLAlchemyCoursesAdapter(session=session)

    async def get_course(
            self,
            course_id: int
    ) -> CourseRead:
        """
        Get course by id.

        :param course_id: A course id.
        :raises CourseNotFound: A course with this id is not exist.
        :return: A course.
        """
        course = await self.db_adapter.get_course(course_id)

        if course is None:
            raise exceptions.CourseNotFound
        return course

    async def get_courses(
            self,
            country_name: str
    ) -> List[CourseRead]:
        """
        Get courses with parameters.

        :param country_name: A country name.
        :raises CoursesNotFound: A courses with these parameters is empty.
        :return: A courses.
        """
        courses = await self.db_adapter.get_courses(country_name)

        if not courses:
            raise exceptions.CoursesNotFound()
        return courses

    async def create_course(
            self,
            course_create: CourseCreate
    ) -> CourseRead:
        """
        Create a course in database.

        :param course_create: The CourseCreate model to create.
        :return: A new course.
        """
        course_dict = course_create.create_update_dict()

        created_course = await self.db_adapter.create_course(course_dict)
        return created_course

    async def update_course(
            self,
            course_id: int,
            course_update: CourseUpdate
    ) -> CourseRead:
        """
        Update a course in database.

        :param course_id: A course id.
        :param course_update: The CourseUpdate model to update.
        :raises CourseNotExist: A course with this id is not exist.
        :return: An updated course.
        """
        course = await self.db_adapter.get_course(course_id)
        if course is None:
            raise exceptions.CourseNotExist
        course_dict = course_update.create_update_dict()

        updated_course = await self.db_adapter.update_course(course, course_dict)
        return updated_course

    async def delete_course(
            self,
            course_id: int
    ) -> None:
        """
        Delete a course from database.

        :param course_id: The id of the course to delete.
        :raises CourseNotExist: A course with this id is not exist.
        """
        course = await self.db_adapter.get_course(course_id)
        if course is None:
            raise exceptions.CourseNotExist

        await self.db_adapter.delete_course(course)
