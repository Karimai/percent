from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Status(StrEnum):
    motherland = "Motherland"
    travel = "Travel"
    study = "Study"
    work = "Work"
    other = "Other"


class Accommodation(StrEnum):
    house = "House"
    guest = "Guest"
    hotel = "Hotel"
    camp = "Camp"


class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    date_of_birth: Optional[date] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    residences: List[Residence] = []
    # residences = []

    class Config:
        orm_mode = True


class ResidenceBase(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    status: Optional[Status] = Status.motherland
    country: str
    city: str


class ResidenceCreate(ResidenceBase):
    pass


class ResidenceUpdate(ResidenceBase):
    pass


class Residence(ResidenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


#  for error:  File "<frozen abc>", line 123, in __subclasscheck__
# TypeError: issubclass() arg 1 must be a class
# for residences: List[Residence] = []
User.update_forward_refs()


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
