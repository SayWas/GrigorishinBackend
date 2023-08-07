from sqlalchemy.ext.asyncio import AsyncSession

import schedule.exceptions as exceptions
from schedule.db_adapter import SQLAlchemyScheduleAdapter
from schedule.schemas import ScheduleRead


class ScheduleManager:
    def __init__(self,
                 session: AsyncSession
                 ):
        self.db_adapter = SQLAlchemyScheduleAdapter(session=session)

    async def get_schedule(self) -> ScheduleRead:
        """
        Get a schedule from database.

        :raises ScheduleEmpty: The schedule is empty.
        :return: The schedule.
        """
        schedule = await self.db_adapter.get_schedule()

        if not schedule:
            raise exceptions.ScheduleEmpty()
        return schedule
