import random
from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base_db_adapter import base_get, base_create_update
from library.schemas import LibraryRead
from models import LibraryPreview, Book, Course


class SQLAlchemyLibraryAdapter:
    session: AsyncSession

    def __init__(self,
                 session: AsyncSession,
                 ):
        self.session = session

    async def get_preview(self, preview_id: int = None) -> LibraryPreview:
        if preview_id is None:
            preview_id = random.randint(2, 2)
        statement = select(LibraryPreview).where(LibraryPreview.id == preview_id)
        return await base_get(self.session, statement)

    async def get_book(self, book_id: int) -> Book:
        statement = select(Book).where(Book.id == book_id)
        return await base_get(self.session, statement)

    async def get_library(self, limit: int, offset: int, courses_ids: List[int]) -> LibraryRead:
        if courses_ids:
            statement = select(Book).join(Course.books).where(Course.id.in_(courses_ids)).order_by(Course.id)
        else:
            statement = select(Book)
        books = await base_get(self.session, statement, one_scalar=False)
        total_books = len(books)
        total_pages = total_books // limit + 1 if total_books % limit else total_books // limit
        statement = statement.order_by(Book.id).offset(offset).limit(limit)
        books = await base_get(self.session, statement, one_scalar=False)
        return LibraryRead(books=books, total_pages=total_pages, total_books=total_books)

    async def create_preview(self, create_dict: Dict[str, Any]) -> LibraryPreview:
        preview = LibraryPreview(**create_dict)
        await base_create_update(self.session, preview)

        preview = await self.get_preview(preview.id)
        return preview

    async def create_book(self, create_dict: Dict[str, Any]) -> Book:
        book = Book(**create_dict)
        await base_create_update(self.session, book)

        book = await self.get_book(book.id)
        return book

    async def update_preview(self, update_preview: LibraryPreview, update_dict: Dict[str, Any]) -> LibraryPreview:
        for key, value in update_dict.items():
            if value is None:
                continue
            setattr(update_preview, key, value)
        await base_create_update(self.session, update_preview)

        preview = await self.get_preview(update_preview.id)
        return preview

    async def update_book(self, update_book: Book, update_dict: Dict[str, Any]) -> Book:
        for key, value in update_dict.items():
            if value is None:
                continue
            setattr(update_book, key, value)
        await base_create_update(self.session, update_book)

        book = await self.get_book(update_book.id)
        return book

    async def delete_preview(self, preview: LibraryPreview) -> None:
        await self.session.delete(preview)
        await self.session.commit()

    async def delete_book(self, book: Book) -> None:
        await self.session.delete(book)
        await self.session.commit()
