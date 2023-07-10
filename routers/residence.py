import os
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from jose import jwt
from sqlalchemy.orm import Session

from config.config import get_db, templates
from repositories import residence_repo
from schemas import schemas

router = APIRouter(tags=["Residence"], prefix="/residence")
Date_format = "%Y-%m-%d"


@router.post("/create", response_model=schemas.Residence)
def create_residence(
    user_id: int,
    residence: schemas.ResidenceCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return residence_repo.create_residence(db, residence=residence, user_id=user_id)


@router.get("/residences")
def get_residences(request: Request, db: Annotated[Session, Depends(get_db)]):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM")
        )
        userid = int(payload.get("userid"))
        residences = residence_repo.get_residences(db, userid)
        return templates.TemplateResponse(
            "residence.html", {"request": request, "residences": residences}
        )
    except Exception as e:
        errors = [str(e)]
        return templates.TemplateResponse(
            name="index.html", context={"request": request, "errors": errors}
        )


@router.delete("/delete/{residence_id}")
def delete_residence(residence_id: int, db: Annotated[Session, Depends(get_db)]):
    deleted = residence_repo.delete_residence(db, residence_id)
    if not deleted:
        return {"message": "Database issue"}
    return {"message": "Deleted successfully"}


@router.get("/newresidence")
def new_residence(request: Request):
    return templates.TemplateResponse("new_residence.html", {"request": request})


@router.post("/newresidence")
async def save_residence(request: Request, db: Annotated[Session, Depends(get_db)]):
    from datetime import datetime

    form = await request.form()
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM")
        )
        userid = int(payload.get("userid"))
        residence = schemas.ResidenceCreate(
            start_date=datetime.strptime(form.get("start-date"), Date_format),
            end_date=datetime.strptime(form.get("end-date"), Date_format),
            status=form.get("status").capitalize(),
            country=form.get("country"),
        )
        residence_repo.create_residence(db, residence=residence, user_id=userid)
        return RedirectResponse(
            url="/residence/residences", status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        errors = [str(e)]
        return templates.TemplateResponse(
            name="index.html", context={"request": request, "errors": errors}
        )


@router.get("/{residence_id}")
def get_residence(
    residence_id: int, request: Request, db: Annotated[Session, Depends(get_db)]
):
    residence = residence_repo.get_residence(db, residence_id=residence_id)
    return templates.TemplateResponse(
        "edit_residence.html",
        {"request": request, "residence": residence},
    )


@router.post("/{residence_id}")
async def set_residence(request: Request, db: Annotated[Session, Depends(get_db)]):
    form = await request.form()
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    try:
        residence_id = int(form.get("residence_id"))
        residence = schemas.ResidenceUpdate(
            start_date=datetime.strptime(form.get("start-date"), Date_format),
            end_date=datetime.strptime(form.get("end-date"), Date_format),
            status=form.get("status").capitalize(),
            country=form.get("country"),
        )
        residence_repo.update_residence(
            db, residence_update=residence, residence_id=residence_id
        )
        return RedirectResponse(
            url="/residence/residences", status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        errors = [str(e)]
        return templates.TemplateResponse(
            name="index.html", context={"request": request, "errors": errors}
        )
