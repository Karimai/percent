from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from config.config import get_db, templates
from repositories import user_repo
from schemas import schemas

router = APIRouter(tags=["Users"], prefix="/user")


@router.get("/register")
def register_user(request: Request):
    """
    Render the 'user_register.html' template for user registration.

    :param request: The HTTP request object.
    :return: A template response for user registration.
    """
    return templates.TemplateResponse("user_register.html", {"request": request})


@router.post("/register", response_model=schemas.User)
async def create_user(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Create a new user using data from the registration form.

    :param request: The HTTP request object.
    :param db: The database session dependency.
    :return: A redirection response after user creation or displaying errors.
    """
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
    """
    Retrieve a list of users from the database.

    :param db: The database session dependency.
    :return: List of users or an HTTPException if no users are found.
    """
    users = user_repo.get_users(db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users")
    return users


@router.get("/logout")
async def logout():
    """
    Perform user logout by deleting the access token cookie.

    :return: A redirection response to the root URL ("/") after logging out.
    """
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Retrieve a user by their ID from the database.

    :param user_id: The ID of the user to retrieve.
    :param db: The database session dependency.
    :return: The user object or an HTTPException if the user is not found.
    """
    db_user = user_repo.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Delete a user by their ID from the database.

    :param user_id: The ID of the user to delete.
    :param db: The database session dependency.
    :return: A message indicating successful user deletion or an HTTPException if the user is not
    found.
    """
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
):
    """
    Update a user by their ID in the database.

    :param user_id: The ID of the user to update.
    :param user_update: The updated user data.
    :param db: The database session dependency.
    :return: The updated user object or an HTTPException if the user is not found.
    """
    updated_user = user_repo.update_user(db, user_id=user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_repo.get_user(db, user_id=user_id)
