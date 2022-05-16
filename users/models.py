from fastapi_users import models


class UserDTO(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(UserDTO, models.BaseUserDB):
    pass
