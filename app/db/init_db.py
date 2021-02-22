from pymongo import MongoClient

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401


def init_db() -> None:
    db = get_default_bucket()
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
