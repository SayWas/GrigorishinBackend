from datetime import datetime
from typing import List

from pydantic import BaseModel, HttpUrl

from base_schema import CreateUpdateDictMixin
from courses.comments.schemas import CommentRead
from courses.countries.schemas import CountryRead


class BaseCourse(BaseModel):
    title: str
    subtitle: str
    description: str
    image_link: str
    # link: HttpUrl
    price: int
    starting_at: datetime

    class Config:
        orm_mode = True


class CourseRead(BaseCourse):
    id: int
    country: CountryRead
    comments: List["CommentRead"]
    pass


class CourseCreate(BaseCourse, CreateUpdateDictMixin):
    country_id: int
    pass


class CourseUpdate(BaseCourse, CreateUpdateDictMixin):
    title: str | None
    subtitle: str | None
    description: str | None
    link: HttpUrl | None
    price: int | None
    starting_at: datetime | None
