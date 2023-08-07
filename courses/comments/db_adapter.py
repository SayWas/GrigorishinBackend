from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base_db_adapter import base_get, base_create_update
from models import Comment, User


class SQLAlchemyCommentsAdapter:
    session: AsyncSession

    def __init__(self,
                 session: AsyncSession,
                 ):
        self.session = session

    async def get_comment(self, comment_id: int) -> Comment:
        statement = select(Comment).where(Comment.id == comment_id)
        return await base_get(self.session, statement)

    async def get_comments(self, course_id: int) -> List[Comment]:
        statement = select(Comment).where(Comment.course_id == course_id).order_by(Comment.created_at.desc())
        return await base_get(self.session, statement, one_scalar=False)

    async def create_comment(self, comment_dict: Dict[str, Any]) -> Comment | None:
        if await self._is_user_bought_course(comment_dict['user_id'], comment_dict['course_id']) is False:
            return None

        comment = Comment(**comment_dict)
        await base_create_update(self.session, comment)

        comment = await self.get_comment(comment.id)
        return comment

    async def update_comment(self, update_comment: Comment, update_dict: Dict[str, Any]) -> Comment:
        for key, value in update_dict.items():
            if value is None:
                continue
            setattr(update_comment, key, value)
        await base_create_update(self.session, update_comment)

        comment = await self.get_comment(update_comment.id)
        return comment

    async def delete_comment(self, comment: Comment) -> None:
        await self.session.delete(comment)
        await self.session.commit()

    async def _is_user_bought_course(self, user_id: int, course_id: int) -> bool:
        statement = select(User).where(User.id == user_id).where(User.courses.any(id=course_id))
        user = await base_get(self.session, statement)
        return user is not None
