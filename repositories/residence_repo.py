from sqlalchemy.orm import Session

from models import models
from schemas import schemas


def create_residence(
    db: Session, residence: schemas.ResidenceCreate, user_id: int
) -> models.Residence:
    db_residence = models.Residence(
        start_date=residence.start_date,
        end_date=residence.end_date,
        status=residence.status,
        country=residence.country,
        user_id=user_id,
    )
    db.add(db_residence)
    db.commit()
    db.refresh(db_residence)
    return db_residence


def get_residence(db: Session, residence_id: int) -> models.Residence:
    return (
        db.query(models.Residence).filter(models.Residence.id == residence_id).first()
    )


def get_residences(db: Session, userid: int):
    residences = (
        db.query(models.Residence).filter(models.Residence.user_id == userid).all()
    )
    return residences


def delete_residence(db: Session, residence_id: int):
    residence = (
        db.query(models.Residence).filter(models.Residence.id == residence_id).first()
    )
    if residence:
        db.delete(residence)
        db.commit()
        return True
    return False


def update_residence(
    db: Session, residence_update: schemas.ResidenceUpdate, residence_id: int
):
    residence = (
        db.query(models.Residence).filter(models.Residence.id == residence_id).first()
    )
    if residence:
        for field, value in residence_update.dict(exclude_unset=True).items():
            setattr(residence, field, value)
        db.commit()
        db.refresh(residence)
        return residence
    return None
