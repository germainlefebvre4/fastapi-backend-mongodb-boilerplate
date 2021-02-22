import requests
from fastapi.encoders import jsonable_encoder

from typing import Any, Dict, Optional, Union

from app.db.database import get_default_bucket
from bson.objectid import ObjectId

from app.core import config
from app.core.security import get_password_hash, verify_password
from app.schemas.role import RoleEnum
from app.schemas.user import User, UserCreate, UserInDB, UserUpdate


def get(*, id: ObjectId):
    db = get_default_bucket()
    collection = db["users"]
    query_str = { "id": str(id) }
    user_db = collection.find_one(query_str)

    if not user_db:
        return None

    user = UserInDB(**user_db)

    return user


def get_multi(*, skip: int = 0, limit: int = 100):
    db = get_default_bucket()
    collection = db["users"]
    users = []
    for user_db in collection.find():
        user = UserInDB(**user_db)
        users.append(user)
    return users


def get_by_email(*, email: str) -> Optional[User]:
    query_str = { "email": f"{email}" }
    
    db = get_default_bucket()
    collection = db["users"]
    user_db = collection.find_one(query_str)
    
    if not user_db:
        return None

    user = UserInDB(**user_db)

    return user


def create(*, obj_in: UserCreate) -> User:
    passwordhash = get_password_hash(obj_in.password)
    user = UserInDB(**obj_in.dict(by_alias=True), hashed_password=passwordhash)
    doc_data = jsonable_encoder(user)
    db = get_default_bucket()
    collection = db["users"]
    res = collection.insert_one(doc_data)

    user_db = collection.find_one({"_id": ObjectId(res.inserted_id)})
    user = UserInDB(**user_db)

    return user


def update(*, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)

    if update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    obj_data = jsonable_encoder(update_data)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])

    query_str = { "email": f"{db_obj.email}" }
    newvalues = { "$set": obj_data }
    
    db = get_default_bucket()
    collection = db["users"]
    user_db = collection.find_one_and_update(query_str, newvalues)

    user = UserInDB(**user_db)

    return user


def remove(*, id: str) -> User:
    user = get(id=id)
    
    db = get_default_bucket()
    collection = db["users"]
    res = collection.delete_one({"id": str(id)})

    return user


def authenticate(*, email: str, password: str) -> Optional[User]:
    user = get_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user: User) -> bool:
    return user.is_active


def is_superuser(user: User) -> bool:
    return user.is_superuser
