from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from episodes import episodes_router
from episodes.models import EpisodeAdmin
from images.models import ImageAdmin
from settings import ENGINE
from shows import shows_router
from shows.models import ShowAdmin
from users import auth_backend, UserDB, fastapi_users, current_active_user
from users.db_adapter import UserAdmin

app = FastAPI()

admin = Admin(app, ENGINE)

admin.register_model(UserAdmin)
admin.register_model(ImageAdmin)
admin.register_model(ShowAdmin)
admin.register_model(EpisodeAdmin)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
app.include_router(shows_router, tags=["shows"])
# app.include_router(images_router, tags=["images"])
app.include_router(episodes_router, tags=["episodes"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/url-list")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list
