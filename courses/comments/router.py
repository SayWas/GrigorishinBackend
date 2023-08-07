from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession

import courses.comments.exceptions as exceptions
from auth.base_config import current_user
from courses.comments.manager import CommentsManager as cm
from courses.comments.schemas import CommentRead, CommentCreate
from courses.comments.utils import ErrorCode
from database import get_async_session

comments_router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@comments_router.get(
    "/",
    response_model=List[CommentRead],
    status_code=status.HTTP_200_OK,
    name="comments:get_comments",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.COMMENTS_NOT_FOUND: {
                            "summary": "The comments with these parameters has not been found.",
                            "value": {
                                "detail": ErrorCode.COMMENTS_NOT_FOUND
                            },
                        }
                    }
                }
            },
        }
    },
)
async def get_comments(
        course_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        comments = await cm(session).get_comments(course_id)
        return comments
    except exceptions.CommentsNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.COMMENTS_NOT_FOUND
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@comments_router.post(
    "/",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
    name="comments:create_comment",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "User doesn't have this course."
        }
    }
)
async def create_comment(
        comment: CommentCreate,
        user=Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        comment = await cm(session).create_comment(comment, user)
        return comment
    except exceptions.UserDoesNotOwnCourse:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User doesn't have this course."
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
