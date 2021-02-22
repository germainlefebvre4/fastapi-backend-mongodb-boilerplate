from enum import Enum
from typing import List

from pydantic import BaseModel

from app.core.config import settings


class RoleEnum(Enum):
    superuser = settings.FIRST_SUPERUSER


class Roles(BaseModel):
    roles: List[RoleEnum]
