from uuid import UUID
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from settings import USER_MANAGER_SECRET
from users.db import User, get_user_db
from utils.constants import verify_user_mail_template, forgot_password_mail_template
from utils.mailing import prepare_email, send_email

SECRET = USER_MANAGER_SECRET


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        forgot_password_mail = prepare_email(user.email, token, forgot_password_mail_template)
        await send_email(forgot_password_mail)
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        verify_user_mail = prepare_email(user.email, token, verify_user_mail_template)
        await send_email(verify_user_mail)
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
