from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.config import get_db
from repositories import residence_repo
from schemas import schemas

router = APIRouter(tags=["Residence"], prefix="/residence")


@router.post("/create", response_model=schemas.Residence)
def create_residence(
        user_id: int,
        residence: schemas.ResidenceCreate,
        db: Annotated[Session, Depends(get_db)]
):
    return residence_repo.create_residence(db, residence=residence, user_id=user_id)

