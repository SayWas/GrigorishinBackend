from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession

import courses.exceptions as exceptions
from auth.base_config import current_superuser
from courses.manager import CoursesManager as cm
from courses.schemas import CourseRead, CourseCreate, CourseUpdate
from courses.utils import ErrorCode
from database import get_async_session

courses_router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@courses_router.get(
    "/{course_id}",
    response_model=CourseRead,
    status_code=status.HTTP_200_OK,
    name="courses:get_course",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.COURSE_NOT_FOUND: {
                            "summary": "The course with this id has not been found.",
                            "value": {
                                "detail": ErrorCode.COURSE_NOT_FOUND
                            },
                        }
                    }
                }
            },
        }
    },
)
async def get_course(
        course_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        course = await cm(session).get_course(course_id)
        return course
    except exceptions.CourseNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.COURSE_NOT_FOUND
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@courses_router.get(
    "/",
    response_model=List[CourseRead],
    status_code=status.HTTP_200_OK,
    name="courses:get_courses",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.COURSES_NOT_FOUND: {
                            "summary": "The courses with these parameters has not been found.",
                            "value": {
                                "detail": ErrorCode.COURSES_NOT_FOUND
                            },
                        }
                    }
                }
            },
        }
    },
)
async def get_courses(
        country_name: str = None,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        courses = await cm(session).get_courses(country_name)
        return courses
    except exceptions.CoursesNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.COURSES_NOT_FOUND
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@courses_router.post(
    "/",
    response_model=CourseRead,
    status_code=status.HTTP_201_CREATED,
    name="courses:create_course",
    dependencies=[Depends(current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        }
    }
)
async def create_course(
        course: CourseCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        course = await cm(session).create_course(course)
        return course
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@courses_router.patch(
    "/{course_id}",
    response_model=CourseRead,
    status_code=status.HTTP_200_OK,
    name="courses:edit_course",
    dependencies=[Depends(current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The course does not exist."
        }
    }
)
async def update_course(
        course_id: int,
        course: CourseUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        course = await cm(session).update_course(course_id, course)
        return course
    except exceptions.CourseNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.COURSE_NOT_EXIST
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@courses_router.delete(
    "/{course_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    name="courses:delete_course",
    dependencies=[Depends(current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The course does not exist."
        }
    }
)
async def delete_course(
        course_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await cm(session).delete_course(course_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except exceptions.CourseNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.COURSE_NOT_EXIST
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
