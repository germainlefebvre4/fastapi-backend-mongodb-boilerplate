from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

from app.schemas.config import USERPROFILE_DOC_TYPE
from app.schemas.role import RoleEnum
from app.schemas.utils import PyObjectId


class UserBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[PyObjectId]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
