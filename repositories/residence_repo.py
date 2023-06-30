from sqlalchemy.orm import Session

from models import models
from schemas import schemas


def create_residence(
        db: Session,
        residence: schemas.ResidenceCreate,
        user_id: int
) -> models.Residence:

    db_residence = models.Residence(
        start_date=residence.start_date,
        end_date=residence.end_date,
        status=residence.status,
        country=residence.country,
        user_id=user_id
    )
    db.add(db_residence)
    db.commit()
    db.refresh(db_residence)
    return db_residence
