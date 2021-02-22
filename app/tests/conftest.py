from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.core.config import settings
from app.main import app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers

from app.db.database import get_default_bucket
from app.db.init_db import init_db


@pytest.fixture(scope="session")
def db() -> Generator:
    yield


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def database_initialization(db):
    db = get_default_bucket()
    collection = db["users"]
    collection.delete_many({})
    init_db()
    yield


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, full_name=settings.USER_TEST_FULLNAME, email=settings.USER_TEST_EMAIL
    )
