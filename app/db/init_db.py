from pymongo import MongoClient

from app import crud, schemas
from app.core.config import settings


def init_db() -> None:
    user = crud.user.get_by_email(email=settings.USER_ADMIN_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            full_name=settings.USER_ADMIN_FULLNAME,
            email=settings.USER_ADMIN_EMAIL,
            password=settings.USER_ADMIN_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(obj_in=user_in)

    user = crud.user.get_by_email(email=settings.USER_TEST_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            full_name=settings.USER_TEST_FULLNAME,
            email=settings.USER_TEST_EMAIL,
            password=settings.USER_TEST_PASSWORD,
            is_superuser=False,
        )
        user = crud.user.create(obj_in=user_in)
