from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from config.config import get_db, templates
from repositories import user_repo
from routers.login import get_current_user
from schemas import schemas

router = APIRouter(tags=["Users"], prefix="/user")


@router.get("/register")
def register_user(request: Request):
    return templates.TemplateResponse("user_register.html", {"request": request})


@router.post("/register", response_model=schemas.User)
async def create_user(request: Request, db: Annotated[Session, Depends(get_db)]):
    usr_form = await request.form()
    try:
        usr = schemas.UserCreate(
            username=usr_form.get("username"),
            first_name=usr_form.get("name"),
            last_name=usr_form.get("lastname"),
            email=usr_form.get("email"),
            password=usr_form.get("password"),
            date_of_birth=usr_form.get("date_of_birth"),
        )
        user_repo.create_user(db, usr)
    except HTTPException as e:
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": [str(e.detail)]}
        )

    return RedirectResponse(
        "/?msg=successfully registered", status_code=status.HTTP_302_FOUND
    )


@router.get("/users")
def get_users(db: Annotated[Session, Depends(get_db)]):
    users = user_repo.get_users(db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users")
    return users


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    db_user = user_repo.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    deleted = user_repo.delete_user(db, user_id=user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": "User deleted successfully"}


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    updated_user = user_repo.update_user(db, user_id=user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_repo.get_user(db, user_id=user_id)
