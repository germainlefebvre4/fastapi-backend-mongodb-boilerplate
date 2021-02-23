from typing import Optional

from odmantic import Model as BaseModel


class UserBase(BaseModel):
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: str


class UserCreate(UserBase):
    full_name: str
    email: str
    password: str


class UserUpdate(UserBase):
    full_name: Optional[str]
    email: Optional[str]
    password: Optional[str] = None


class UserInDBBase(UserBase):
    pass


class User(UserInDBBase):
    full_name: str
    email: str
    is_active: bool
    is_superuser: bool


class UserInDB(UserInDBBase):
    full_name: str
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    hashed_password: str
