from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth.base_config import auth_backend
from auth.base_config import fastapi_users
from auth.schemas import UserRead, UserCreate, UserUpdate
from courses.comments.router import comments_router
from courses.countries.router import countries_router
from courses.router import courses_router
from library.router import library_router
from schedule.router import schedule_router

app = FastAPI(title="Grigorishin Api")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

app.include_router(library_router)

app.include_router(countries_router)

app.include_router(courses_router)

app.include_router(comments_router)

app.include_router(schedule_router)

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PATCH', 'DELETE'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Authorization', 'Access-Control-Allow-Origin',
                   'Access-Control-Allow-Headers']
)
