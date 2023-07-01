# this will allow you to declare the type of the db parameters and have better type checks
# and completion in your functions.
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import models
from schemas import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Separation of concepts
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            error_mes = e.orig.diag.message_detail
            if "email" in error_mes:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already exist!")
            if "username" in error_mes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="User name is already exist!"
                )
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    return wrapper


@handle_exceptions
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
        date_of_birth=user.date_of_birth,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


@handle_exceptions
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> bool:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return True
    return False
