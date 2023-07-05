from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from config.config import get_db, templates
from repositories import residence_repo, user_repo
from schemas import schemas

router = APIRouter(tags=["Residence"], prefix="/residence")


@router.post("/create", response_model=schemas.Residence)
def create_residence(
    user_id: int,
    residence: schemas.ResidenceCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return residence_repo.create_residence(db, residence=residence, user_id=user_id)


@router.get("/residences")
def get_residences(request: Request, db: Annotated[Session, Depends(get_db)]):
    residences = residence_repo.get_residences(db)
    return templates.TemplateResponse(
        "residence.html", {"request": request, "residences": residences}
    )


@router.get("/{residence_id}")
def get_residence(
    residence_id: int, request: Request, db: Annotated[Session, Depends(get_db)]
):
    residence = residence_repo.get_residence(db, residence_id=residence_id)
    user = user_repo.get_user(db, residence.user_id)
    return templates.TemplateResponse(
        "residence_details.html",
        {"request": request, "residence": residence, "user": user},
    )
