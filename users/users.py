from fastapi_users import FastAPIUsers

from users.authentication.auth_backend import auth_backend
from users.models import UserDB, UserUpdate, UserCreate, UserParam
from users.user_manager import get_user_manager

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    UserParam,
    UserCreate,
    UserUpdate,
    UserDB,
)
current_active_user = fastapi_users.current_user(active=True)
