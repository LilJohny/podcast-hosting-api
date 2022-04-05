from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from users.authentication.models import AccessToken
from users.db_adapter import get_access_token_db
from users.models import UserCreate, UserDB


def get_database_strategy(
        access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy[UserCreate, UserDB, AccessToken]:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)