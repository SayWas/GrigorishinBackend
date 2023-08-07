from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

import library.exceptions as exceptions
from library.db_adapter import SQLAlchemyLibraryAdapter
from library.schemas import LibraryPreviewRead, LibraryPreviewCreate, LibraryPreviewUpdate, BookRead, BookCreate, \
    BookUpdate, LibraryRead


class LibraryManager:
    def __init__(self,
                 session: AsyncSession
                 ):
        self.db_adapter = SQLAlchemyLibraryAdapter(session=session)

    async def get_library_preview(self) -> LibraryPreviewRead:
        """
        Get a random library preview.

        :raises LibraryPreviewEmpty: A library preview is empty.
        :return: A library preview.
        """
        preview = await self.db_adapter.get_preview()

        if preview is None:
            raise exceptions.LibraryPreviewEmpty()

        return preview

    async def get_library(self, limit: int, offset: int, courses_ids: List[int]) -> LibraryRead:
        """
        Get books from a library with parameters.

        :param limit: A limit for query pagination.
        :param offset: An offset for query pagination.
        :param courses_ids: A courses ids.
        :raises LibraryNotFound: A library with these parameters is empty.
        :return: A books from library.
        """
        library = await self.db_adapter.get_library(limit, offset, courses_ids)

        if not library.books:
            raise exceptions.LibraryNotFound()
        return library

    async def create_library_preview(
            self,
            preview_create: LibraryPreviewCreate
    ) -> LibraryPreviewRead:
        """
        Create a library preview in database.

        :param preview_create: The LibraryPreviewCreate model to create.
        :return: A new library preview.
        """
        preview_dict = preview_create.create_update_dict()

        created_preview = await self.db_adapter.create_preview(preview_dict)
        return created_preview

    async def create_book(
            self,
            book_create: BookCreate
    ) -> BookRead:
        """
        Create a book in database.

        :param book_create: The BookCreate model to create.
        :return: A new book.
        """
        book_dict = book_create.create_update_dict()

        created_book = await self.db_adapter.create_book(book_dict)
        return created_book

    async def update_library_preview(
            self,
            preview_id: int,
            preview_update: LibraryPreviewUpdate
    ) -> LibraryPreviewRead:
        """
        Update a library preview.

        :param preview_id: The id of the library preview to change.
        :param preview_update: The LibraryPreviewUpdate model containing the changes to apply to the preview.
        :raises LibraryPreviewNotExist: A library preview with this id is not exist.
        :return: The updated library preview.
        """
        preview = await self.db_adapter.get_preview(preview_id)
        if preview is None:
            raise exceptions.LibraryPreviewNotExist
        preview_dict = preview_update.create_update_dict()

        updated_preview = await self.db_adapter.update_preview(preview, preview_dict)
        return updated_preview

    async def update_book(
            self,
            book_id: int,
            book_update: BookUpdate
    ) -> BookRead:
        """
        Update a book.

        :param book_id: The id of the book to change.
        :param book_update: The BookUpdate model containing the changes to apply to the book.
        :raises LibraryBookNotExist: A book with this id is not exist.
        :return: The updated book.
        """
        book = await self.db_adapter.get_book(book_id)
        if book is None:
            raise exceptions.LibraryBookNotExist
        book_dict = book_update.create_update_dict()

        updated_book = await self.db_adapter.update_book(book, book_dict)
        return updated_book

    async def delete_library_preview(
            self,
            preview_id: int
    ) -> None:
        """
        Delete a library preview.

        :param preview_id: The id of library preview to delete.
        :raises LibraryPreviewNotExist: A library preview with this id is not exist.
        """
        preview = await self.db_adapter.get_preview(preview_id)
        if preview is None:
            raise exceptions.LibraryPreviewNotExist

        await self.db_adapter.delete_preview(preview)

    async def delete_book(
            self,
            book_id: int
    ) -> None:
        """
        Delete a book.

        :param book_id: The id of book to delete.
        :raises LibraryBookNotExist: A book with this id is not exist.
        """
        book = await self.db_adapter.get_book(book_id)
        if book is None:
            raise exceptions.LibraryBookNotExist

        await self.db_adapter.delete_book(book)
