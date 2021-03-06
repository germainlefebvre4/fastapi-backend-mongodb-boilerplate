from typing import Dict

from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.USER_ADMIN_EMAIL
    assert current_user["full_name"] == settings.USER_ADMIN_FULLNAME


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.USER_TEST_EMAIL
    assert current_user["full_name"] == settings.USER_TEST_FULLNAME


def test_create_user_new_email_by_admin(
    client: TestClient, superuser_token_headers: dict,
) -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    data = {"full_name": full_name, "email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(email=email)
    assert user
    assert created_user["email"] == user.email
    assert created_user["is_superuser"] is False


def test_create_user_new_email_by_user(
    client: TestClient, normal_user_token_headers: dict,
) -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    data = {"full_name": full_name, "email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict
) -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password)
    user = crud.user.create(obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(email=email)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_create_user_existing_email(
    client: TestClient, superuser_token_headers: dict
) -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password)
    crud.user.create(obj_in=user_in)
    data = {"full_name": full_name, "email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    data = {"full_name": full_name, "email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict
) -> None:
    full_name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(full_name=full_name, email=email, password=password)
    crud.user.create(obj_in=user_in)

    full_name2 = random_lower_string()
    email2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(full_name=full_name2, email=email2, password=password2)
    crud.user.create(obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
