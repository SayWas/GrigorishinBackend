import re
from threading import Thread
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from auth.email_service import send_reset_password_mail
from auth.utils import get_user_db
from config import RESET_SECRET, VERIFICATION_SECRET
from models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = RESET_SECRET
    verification_token_secret = VERIFICATION_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        Thread(target=send_reset_password_mail, args=(user.email, token)).start()

    async def on_after_reset_password(
            self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        print("reset")

    async def validate_password(self, password: str, user: models.UP):
        if len(password) < 8:
            raise exceptions.InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if len(password) > 1024:
            raise exceptions.InvalidPasswordException(
                reason="Password is too long"
            )
        if re.match("^.*(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&?]).*$", password) is None:
            raise exceptions.InvalidPasswordException(
                reason="Password should contain at least one letter, one number and one special character"
            )

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
