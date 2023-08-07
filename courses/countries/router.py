from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession

import courses.countries.exceptions as exceptions
from auth.base_config import current_superuser
from courses.countries.manager import CountriesManager as cm
from courses.countries.schemas import CountryRead, CountryBlockRead, CountryBlockCreate, CountryCreate, CountryUpdate, \
    CountryBlockUpdate
from courses.countries.utils import ErrorCode
from database import get_async_session

countries_router = APIRouter(
    prefix="/countries",
    tags=["Countries"]
)


@countries_router.get(
    "/",
    response_model=List[CountryRead],
    status_code=status.HTTP_200_OK,
    name="countries:get_countries",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.COUNTRIES_NOT_FOUND: {
                            "summary": "The countries with these parameters has not been found.",
                            "value": {
                                "detail": ErrorCode.COUNTRIES_NOT_FOUND
                            },
                        }
                    }
                }
            },
        }
    },
)
async def get_countries(
        country_block_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        countries = await cm(session).get_countries(country_block_id)
        return countries
    except exceptions.CountriesNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.COUNTRIES_NOT_FOUND
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@countries_router.post(
    "/",
    response_model=CountryRead,
    status_code=status.HTTP_201_CREATED,
    name="countries:create_country",
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
async def create_country(
        country: CountryCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        country = await cm(session).create_country(country)
        return country
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@countries_router.patch(
    "/{country_id}",
    response_model=CountryRead,
    status_code=status.HTTP_200_OK,
    name="countries:update_country",
    dependencies=[Depends(current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The country does not exist."
        }
    }
)
async def update_country(
        country_id: int,
        country: CountryUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        country = await cm(session).update_country(country_id, country)
        return country
    except exceptions.CountryNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.COUNTRY_NOT_EXIST
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@countries_router.delete(
    "/{country_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    name="countries:delete_country",
    dependencies=[Depends(current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The country does not exist."
        }
    }
)
async def delete_country(
        country_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await cm(session).delete_country(country_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except exceptions.CountryNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.COUNTRY_NOT_EXIST
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@countries_router.get(
    "/blocks",
    response_model=List[CountryBlockRead],
    status_code=status.HTTP_200_OK,
    name="countries:get_country_blocks"
)
async def get_country_blocks(
        session: AsyncSession = Depends(get_async_session)
):
    try:
        country_blocks = await cm(session).get_country_blocks()
        return country_blocks
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@countries_router.post(
    "/blocks",
    response_model=CountryBlockRead,
    status_code=status.HTTP_201_CREATED,
    name="countries:create_country_block",
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
async def create_country_block(
        country_block: CountryBlockCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        country_block = await cm(session).create_country_block(country_block)
        return country_block
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@countries_router.patch(
    "/blocks/{country_block_id}",
    response_model=CountryBlockRead,
    status_code=status.HTTP_200_OK,
    name="countries:update_country_block",
    dependencies=[Depends(current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The country block does not exist."
        }
    }
)
async def update_country_block(
        country_block_id: int,
        country_block: CountryBlockUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        country_block = await cm(session).update_country_block(country_block_id, country_block)
        return country_block
    except exceptions.CountryBlockNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.COUNTRY_BLOCK_NOT_EXIST
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@countries_router.delete(
    "/blocks/{country_block_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    name="countries:delete_country_block",
    dependencies=[Depends(current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The country block does not exist."
        }
    }
)
async def delete_country_block(
        country_block_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await cm(session).delete_country_block(country_block_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except exceptions.CountryBlockNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.COUNTRY_BLOCK_NOT_EXIST
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )