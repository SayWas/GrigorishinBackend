from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Response, Query
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession

import library.exceptions as exceptions
from auth.base_config import current_superuser
from database import get_async_session
from library.manager import LibraryManager as lm
from library.schemas import BookCreate, BookRead, BookUpdate, LibraryPreviewRead, LibraryPreviewCreate, \
    LibraryPreviewUpdate, LibraryRead
from library.utils import ErrorCode

library_router = APIRouter(
    prefix="/library",
    tags=["Library"]
)


class PaginatedParams:
    def __init__(self,
                 page: int = Query(ge=1),
                 per_page: int = Query(ge=1, default=2)
                 ):
        self.limit = per_page
        self.offset = (page - 1) * per_page


@library_router.get(
    "/",
    response_model=LibraryRead,
    status_code=status.HTTP_200_OK,
    name="library:get_books",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LIBRARY_BOOKS_NOT_FOUND: {
                            "summary": "The page does not exist or there is no books with that filters in the library.",
                            "value": {
                                "detail": ErrorCode.LIBRARY_BOOKS_NOT_FOUND
                            },
                        }
                    }
                }
            },
        }
    },
)
async def get_books(
        pgp: PaginatedParams = Depends(),
        courses_ids: List[int] = Query(default=None),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        library = await lm(session).get_library(pgp.limit, pgp.offset, courses_ids)
        return library
    except exceptions.LibraryNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LIBRARY_BOOKS_NOT_FOUND
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@library_router.post(
    "/",
    response_model=BookRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    name="library:create_book",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        }
    }
)
async def create_book(
        book: BookCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        created_book = await lm(session).create_book(book)
        return BookRead.from_orm(created_book)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@library_router.patch(
    "/{book_id}",
    response_model=BookRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_200_OK,
    name="library:patch_book",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The book does not exist."
        }
    }
)
async def update_book(
        book_id: int,
        book_update: BookUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        book = await lm(session).update_book(book_id, book_update)
        return BookRead.from_orm(book)
    except exceptions.LibraryBookNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.LIBRARY_BOOK_NOT_EXIST)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@library_router.delete(
    "/{book_id}",
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    name="library:delete_book",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The book does not exist."
        }
    }
)
async def delete_book(
        book_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await lm(session).delete_book(book_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except exceptions.LibraryBookNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.LIBRARY_BOOK_NOT_EXIST)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@library_router.get(
    "/preview",
    response_model=LibraryPreviewRead,
    status_code=status.HTTP_200_OK,
    name="library:get_preview",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LIBRARY_PREVIEW_EMPTY: {
                            "summary": "The library preview is empty.",
                            "value": {
                                "detail": ErrorCode.LIBRARY_PREVIEW_EMPTY
                            },
                        }
                    }
                }
            },
        },
    },
)
async def get_preview(
        session: AsyncSession = Depends(get_async_session)
):
    try:
        lib_preview = await lm(session).get_library_preview()
        return LibraryPreviewRead.from_orm(lib_preview)
    except exceptions.LibraryPreviewEmpty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LIBRARY_PREVIEW_EMPTY,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@library_router.post(
    "/preview",
    response_model=LibraryPreviewRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    name="library:create_preview",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        }
    }
)
async def create_preview(
        preview: LibraryPreviewCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        created_preview = await lm(session).create_library_preview(preview)
        return LibraryPreviewRead.from_orm(created_preview)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@library_router.patch(
    "/preview/{preview_id}",
    response_model=LibraryPreviewRead,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_200_OK,
    name="library:patch_preview",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The library preview does not exist.",
        }
    }
)
async def update_preview(
        preview_id: int,
        preview_update: LibraryPreviewUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        preview = await lm(session).update_library_preview(preview_id, preview_update)
        return LibraryPreviewRead.from_orm(preview)
    except exceptions.LibraryPreviewNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.LIBRARY_PREVIEW_NOT_EXIST)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@library_router.delete(
    "/preview/{preview_id}",
    response_class=Response,
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
    name="library:delete_preview",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The library preview does not exist.",
        },
    },
)
async def delete_preview(
        preview_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await lm(session).delete_library_preview(preview_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except exceptions.LibraryPreviewNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.LIBRARY_PREVIEW_NOT_EXIST)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
