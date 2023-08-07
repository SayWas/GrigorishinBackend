from datetime import datetime
from typing import List

from pydantic import BaseModel

from courses.schemas import CourseRead


class BaseScheduleRow(BaseModel):
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True


class ScheduleRowRead(BaseScheduleRow):
    id: int
    course: CourseRead
    pass


class BaseSchedule(BaseModel):
    class Config:
        orm_mode = True


class ScheduleRead(BaseSchedule):
    schedule: dict[int, List[ScheduleRowRead]]
    pass
