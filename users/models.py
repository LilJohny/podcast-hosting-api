from fastapi_users import models


class UserParam(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(UserParam, models.BaseUserDB):
    pass
