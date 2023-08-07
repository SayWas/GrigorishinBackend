from typing import List

from pydantic import BaseModel, HttpUrl

from base_schema import CreateUpdateDictMixin
from courses.schemas import CourseRead


class BaseBook(BaseModel):
    title: str
    author: str
    download_link: HttpUrl | None

    class Config:
        orm_mode = True


class BookRead(BaseBook):
    id: int
    courses: List["CourseRead"]
    pass


class BookCreate(BaseBook, CreateUpdateDictMixin):
    pass


class BookUpdate(BaseBook, CreateUpdateDictMixin):
    title: str | None
    author: str | None
    download_link: HttpUrl | None


class LibraryRead(BaseModel):
    total_books: int
    total_pages: int
    books: List[BookRead]


class BaseLibraryPreview(BaseModel):
    quote: str
    quote_author: str

    class Config:
        orm_mode = True


class LibraryPreviewRead(BaseLibraryPreview):
    id: int
    book: BookRead
    pass


class LibraryPreviewCreate(BaseLibraryPreview, CreateUpdateDictMixin):
    book_id: int
    pass


class LibraryPreviewUpdate(BaseLibraryPreview, CreateUpdateDictMixin):
    quote: str | None
    quote_author: str | None
    book_id: int | None
