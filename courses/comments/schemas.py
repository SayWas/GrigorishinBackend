from pydantic import BaseModel

from auth.schemas import UserReadComment
from base_schema import CreateUpdateDictMixin


class BaseComment(BaseModel):
    text: str

    class Config:
        orm_mode = True


class CommentRead(BaseComment):
    id: int
    user: UserReadComment
    pass


class CommentCreate(BaseComment, CreateUpdateDictMixin):
    course_id: int
    pass


class CommentUpdate(BaseComment, CreateUpdateDictMixin):
    text: str | None
    user_id: int | None
    course_id: int | None
