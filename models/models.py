from datetime import date

from email_validator import validate_email
from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship, validates

from config.config import Base
from schemas.schemas import Status


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    date_of_birth = Column(Date)
    role = Column(String, default="Regular")  # Admin, Regular

    residences = relationship("Residence", back_populates="user")

    @validates("password")
    def validate_password(self, key, password):
        if not (8 <= len(password) <= 200):
            raise ValueError("Password length must be between 8 and 20")
        return password

    @validates("email")
    def validate_email(self, key, value):
        validate_email(value)
        return value

    @validates("date_of_birth")
    def validate_date_of_birth(self, key, date_of_birth):
        if date_of_birth is None:
            return None
        if not isinstance(date_of_birth, date):
            raise ValueError("Invalid type for Date of birth")
        if date_of_birth > date.today():
            raise ValueError("Date of Birth cannot be in the future.")
        return date_of_birth


class Residence(Base):
    __tablename__ = "residence"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, default=func.now())
    end_date = Column(Date, default=func.now())
    status = Column(Enum(Status), default=Status.motherland)
    country = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="residences")


# class Trip(Base):
#     __tablename__ = "trip"
#
#     id = Column(Integer, primary_key=True, index=True)
#     start_date = Column(DateTime, nullable=False)
#     end_date = Column(DateTime, nullable=False)
#     user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
#     address_id = Column(Integer, ForeignKey("address.id", ondelete="CASCADE"))

# user = relationship("User", back_populates="trips")
# address = relationship("Address", back_populates="trips")

# class Address(Base):
#     __tablename__ = "address"
#
#     id = Column(Integer, primary_key=True, index=True)
#     country = Column(String, nullable=False)
#     city = Column(String)
#     street = Column(String)
#     postal_code = Column(String)
#     accomodation = Column(Enum(Accommodation), default=Accommodation.house)
#     user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

# user = relationship("User", back_populates="addresses", cascade="all, delete")
