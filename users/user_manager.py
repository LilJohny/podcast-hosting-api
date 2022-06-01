from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager

from settings import USER_MANAGER_SECRET
from utils.constants import forgot_password_mail_template, verify_user_mail_template
from utils.mailing import send_email, prepare_email
from .db_adapter import get_user_db
from .models import UserCreate, UserDB

SECRET = USER_MANAGER_SECRET


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        forgot_password_mail = prepare_email(user.email, token, forgot_password_mail_template)
        await send_email(forgot_password_mail)
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        verify_user_mail = prepare_email(user.email, token, verify_user_mail_template)
        await send_email(verify_user_mail)
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
