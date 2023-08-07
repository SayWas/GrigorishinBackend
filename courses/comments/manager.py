from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

import courses.comments.exceptions as exceptions
from courses.comments.db_adapter import SQLAlchemyCommentsAdapter
from courses.comments.schemas import CommentRead, CommentCreate, CommentUpdate
from models import User


class CommentsManager:
    def __init__(self,
                 session: AsyncSession
                 ):
        self.db_adapter = SQLAlchemyCommentsAdapter(session=session)

    async def get_comments(
            self,
            course_id: int
    ) -> List[CommentRead]:
        """
        Get comments with parameters.

        :param course_id: A course id.
        :raises CommentsNotFound: A comments with these parameters is empty.
        :return: A comments.
        """
        comments = await self.db_adapter.get_comments(course_id)

        if not comments:
            raise exceptions.CommentsNotFound
        return comments

    async def create_comment(
            self,
            comment_create: CommentCreate,
            user: User
    ) -> CommentRead:
        """
        Create a comment in database.

        :param comment_create: The CommentCreate model to create.
        :param user: A user.
        :return: A new comment.
        """
        comment_dict = comment_create.create_update_dict()
        comment_dict['user_id'] = user.id

        created_comment = await self.db_adapter.create_comment(comment_dict)

        if created_comment is None:
            raise exceptions.UserDoesNotOwnCourse
        return created_comment

    async def update_comment(
            self,
            comment_id: int,
            comment_update: CommentUpdate
    ) -> CommentRead:
        """
        Update a comment in database.

        :param comment_id: A comment id.
        :param comment_update: The CommentUpdate model to update.
        :raises CommentNotExist: A comment with this id is not exist.
        :return: An updated comment.
        """
        comment = await self.db_adapter.get_comment(comment_id)
        if comment is None:
            raise exceptions.CommentNotExist
        comment_dict = comment_update.create_update_dict()

        updated_comment = await self.db_adapter.update_comment(comment, comment_dict)
        return updated_comment

    async def delete_comment(
            self,
            comment_id: int
    ) -> None:
        """
        Delete a comment in database.

        :param comment_id: The id of the comment to delete.
        :raises CommentNotExist: A comment with this id is not exist.
        """
        comment = await self.db_adapter.get_comment(comment_id)
        if comment is None:
            raise exceptions.CommentNotExist

        await self.db_adapter.delete_comment(comment)