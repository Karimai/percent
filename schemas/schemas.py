from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Optional

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
    # residences: List[Residence] = []
    residences = []

    class Config:
        orm_mode = True


class ResidenceBase(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: Optional[Status] = Status.motherland
    country: str


class ResidenceCreate(ResidenceBase):
    pass


class ResidenceUpdate(ResidenceBase):
    pass


class Residence(ResidenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# class TripBase(BaseModel):
#     start_date: datetime
#     end_date: datetime
#     user_id: int
#     address_id: int
#
#
# class TripCreate(TripBase):
#     pass
#
#
# class TripUpdate(TripBase):
#     pass
#
#
# class Trip(TripBase):
#     id: int
#     user: User
#     address: Address
#
#     class Config:
#         orm_mode: True
# class AddressBase(BaseModel):
#     country: str
#     city: Optional[str]
#     street: Optional[str]
#     postal_code: Optional[str]
#     # accommodation: Optional[Accommodation] = Accommodation.house
#
#
# class AddressCreate(AddressBase):
#     pass
#
#
# class AddressUpdate(AddressBase):
#     pass
#
#
# class Address(AddressBase):
#     id: int
#
#     class Config:
#         # The orm_mode will tell the Pydantic model to read the data even if it is not
#         # a dict, but an ORM model (or any other arbitrary object with attributes).
#         orm_mode = True
