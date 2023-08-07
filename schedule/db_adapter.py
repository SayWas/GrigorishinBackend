from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base_db_adapter import base_get
from models import Schedule
from schedule.schemas import ScheduleRead, ScheduleRowRead


class SQLAlchemyScheduleAdapter:
    session: AsyncSession

    def __init__(self,
                 session: AsyncSession,
                 ):
        self.session = session

    # group schedule by weekdays to the dict with key - weekday, value - list of schedule rows. Schedule object only have start_time and end_time as datetime objects.
    async def get_schedule(self) -> ScheduleRead:
        statement = select(Schedule)
        schedule = await base_get(self.session, statement, one_scalar=False)

        schedule_dict: Dict[int, List[ScheduleRowRead]] = {}
        for schedule_row in schedule:
            schedule_row_read = ScheduleRowRead.from_orm(schedule_row)
            schedule_dict.setdefault(schedule_row.start_time.weekday(), []).append(
                schedule_row_read)

        return ScheduleRead(schedule=schedule_dict)
