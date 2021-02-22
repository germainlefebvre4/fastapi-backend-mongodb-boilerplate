from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel


class ContractBase(BaseModel):
    airport_departure: str
    airport_return: str
    datetime_departure: datetime
    datetime_return: datetime
    cars: Optional[list]


class ContractCreate(ContractBase):
    airport_departure: str
    airport_return: str
    datetime_departure: datetime
    datetime_return: datetime
    cars: Optional[list]


class ContractUpdate(ContractBase):
    airport_departure: str
    airport_return: str
    datetime_departure: datetime
    datetime_return: datetime
    cars: Optional[list]


class ContractInDBBase(ContractBase):
    id: int
    user_id: int
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class Contract(ContractInDBBase):
    pass


class ContractInDB(ContractInDBBase):
    pass