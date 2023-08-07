from datetime import datetime
from typing import Any, List

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, Json, HttpUrl

from courses.countries.schemas import CountryRead


class CourseReadUser(BaseModel):
    id: int
    title: str
    subtitle: str
    description: str
    image_link: str
    link: HttpUrl
    price: int
    starting_at: datetime
    country: CountryRead

    class Config:
        orm_mode = True


class BaseRole(BaseModel):
    id: int
    name: str
    permissions: Json[Any] | None

    class Config:
        orm_mode = True


class RoleRead(BaseRole):
    pass


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    firstName: str
    lastName: str
    role_id: int
    role: RoleRead
    courses: List[CourseReadUser]

    class Config:
        orm_mode = True


class UserReadComment(schemas.BaseUser[int]):
    firstName: str
    lastName: str

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    firstName: str
    lastName: str
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    firstName: str | None
    lastName: str | None
    email: EmailStr | None
