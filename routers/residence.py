import os
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from jose import jwt
from sqlalchemy.orm import Session

from config.config import Date_format, get_db, templates
from repositories import residence_repo
from schemas import schemas

from .login import get_current_user

router = APIRouter(tags=["Residence"], prefix="/residence")


@router.post("/create", response_model=schemas.Residence)
def create_residence(
    user_id: int,
    residence: schemas.ResidenceCreate,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Create a new residence using data from the residence creation form.

    :param user_id: The ID of the user creating the residence.
    :param residence: The data for creating the residence.
    :param db: The database session dependency.
    :return: The created residence object.
    """
    return residence_repo.create_residence(db, residence=residence, user_id=user_id)


@router.get("/oauthresidences")
def get_residences_secretly(
    db: Annotated[Session, Depends(get_db)],
    current_user: int = Depends(get_current_user),
):
    """
    Retrieve residences for the current user securely. It is a protected endpoint. User should be
    logged in with oauth2 to be able to trigger this api.

    :param db: The database session dependency.
    :param current_user: The ID of the current authenticated user.
    :return: Residences associated with the current user.
    """
    residences = residence_repo.get_residences(db, current_user)
    return residences


@router.get("/residences", include_in_schema=False)
def get_residences(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Retrieve residences for the current user and render them on the "residence.html" template.

    :param request: The HTTP request object.
    :param db: The database session dependency.
    :return: A template response displaying the user's residences.
    """
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
    """
    Delete a residence by its ID from the database.

    :param residence_id: The ID of the residence to delete.
    :param db: The database session dependency.
    :return: A message indicating successful deletion or an error message.
    """
    deleted = residence_repo.delete_residence(db, residence_id)
    if not deleted:
        return {"message": "Database issue"}
    return {"message": "Deleted successfully"}


@router.get("/newresidence", include_in_schema=False)
def new_residence(request: Request):
    """
    Render the page for creating a new residence.

    :param request: The HTTP request object.
    :return: A template response for the "new_residence.html" page.
    """
    return templates.TemplateResponse("new_residence.html", {"request": request})


@router.post("/newresidence", include_in_schema=False)
async def save_residence(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Save a new residence using data from the new residence creation form.

    :param request: The HTTP request object.
    :param db: The database session dependency.
    :return: A redirect response after processing the new residence creation.
    """
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
            end_date="present"
            if form.get("present")
            else datetime.strptime(form.get("end-date"), Date_format).strftime(
                Date_format
            ),
            status=form.get("status").capitalize(),
            country=form.get("country"),
            city=form.get("city"),
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


@router.get("/{residence_id}", include_in_schema=False)
def get_residence(
    residence_id: int, request: Request, db: Annotated[Session, Depends(get_db)]
):
    """
    Retrieve a specific residence by its ID and render it on the "edit_residence.html" template.

    :param residence_id: The ID of the residence to retrieve.
    :param request: The HTTP request object.
    :param db: The database session dependency.
    :return: A template response displaying the retrieved residence for editing.
    """
    residence = residence_repo.get_residence(db, residence_id=residence_id)
    return templates.TemplateResponse(
        "edit_residence.html",
        {"request": request, "residence": residence},
    )


@router.post("/{residence_id}")
async def set_residence(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Update a residence based on data from the edit residence form.

    :param request: The HTTP request object.
    :param db: The database session dependency.
    :return: A redirect response after processing the residence update.
    """
    form = await request.form()
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    try:
        residence_id = int(form.get("residence_id"))
        residence = schemas.ResidenceUpdate(
            start_date=datetime.strptime(form.get("start-date"), Date_format),
            end_date="present"
            if form.get("present")
            else datetime.strptime(form.get("end-date"), Date_format).strftime(
                Date_format
            ),
            status=form.get("status").capitalize(),
            country=form.get("country"),
            city=form.get("city"),
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
