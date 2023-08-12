from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, validator

from config.config import Date_format


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

    class Config:
        orm_mode = True


class ResidenceBase(BaseModel):
    start_date: date
    end_date: str
    status: Status = Status.motherland
    country: str
    city: str

    @validator("start_date")
    def validate_start_date(cls, value):
        if not value or value > date.today():
            raise ValueError("Start date cannot be in the future")
        return value

    @validator("end_date")
    def validate_end_date(cls, value):
        if not value:
            raise ValueError(
                "End date is empty. It should have a valid date or 'present'"
            )
        if value == "present":
            return value
        value = datetime.strptime(value, Date_format).date()
        if value > date.today():
            raise ValueError("End date cannot be in the future.")
        return value

    @validator("country")
    def validate_country(cls, value):
        if not value:
            raise ValueError("Country name is mandatory")
        return value

    @validator("city")
    def validate_city(cls, value):
        if not value:
            raise ValueError("City name is mandatory")
        return value

    @validator("status")
    def validate_status(cls, value):
        if value not in Status:
            raise ValueError("Invalid status value")
        return value


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
