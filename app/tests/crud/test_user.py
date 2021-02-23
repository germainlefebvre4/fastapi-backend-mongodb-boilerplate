from fastapi.encoders import jsonable_encoder

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.db.database import get_default_bucket
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user() -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password)
    user = crud.user.create(obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user() -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password)
    user = crud.user.create(obj_in=user_in)
    authenticated_user = crud.user.authenticate(email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user() -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.user.authenticate(email=email, password=password)
    assert user is None


def test_check_if_user_is_active() -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password)
    user = crud.user.create(obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive() -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password, disabled=True)
    user = crud.user.create(obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active


def test_check_if_user_is_superuser() -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password, is_superuser=True)
    user = crud.user.create(obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user() -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password)
    user = crud.user.create(obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


def test_get_user() -> None:
    full_name = random_lower_string()
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(full_name=full_name, email=email, password=password, is_superuser=True)
    user = crud.user.create(obj_in=user_in)
    user_2 = crud.user.get(id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_get_user_with_email() -> None:
    full_name = random_lower_string()
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(full_name=full_name, email=email, password=password, is_superuser=True)
    user = crud.user.create(obj_in=user_in)
    user_2 = crud.user.get_by_email(email=user.email)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user() -> None:
    full_name = random_lower_string()
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(full_name=full_name, email=email, password=password, is_superuser=True)
    user = crud.user.create(obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    crud.user.update(db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)


def test_delete_user() -> None:
    full_name = random_lower_string()
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(full_name=full_name, email=email, password=password, is_superuser=True)
    user = crud.user.create(obj_in=user_in)
    user2 = crud.user.remove(id=user.id)
    user3 = crud.user.get_by_email(email=user.email)
    assert user3 is None
    assert user2.id == user.id
    assert user2.email == email
