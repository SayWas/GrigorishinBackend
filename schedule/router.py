from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession

import schedule.exceptions as exceptions
from database import get_async_session
from schedule.manager import ScheduleManager as sm
from schedule.schemas import ScheduleRead
from schedule.utils import ErrorCode

schedule_router = APIRouter(
    prefix="/schedule",
    tags=["Schedule"]
)


@schedule_router.get(
    "/",
    response_model=ScheduleRead,
    status_code=status.HTTP_200_OK,
    name="schedule:get_schedule",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.SCHEDULE_EMPTY: {
                            "summary": "Schedule is empty.",
                            "value": {
                                "detail": ErrorCode.SCHEDULE_EMPTY
                            },
                        }
                    }
                }
            },
        }
    },
)
async def get_schedule(
        session: AsyncSession = Depends(get_async_session)
):
    try:
        schedule = await sm(session).get_schedule()
        return ScheduleRead.from_orm(schedule)
    except exceptions.ScheduleEmpty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.SCHEDULE_EMPTY
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
