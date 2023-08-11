import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config.config import get_db, templates
from models import models
from repositories.user_repo import pwd_context
from utility.helper import generate_token

load_dotenv()

router = APIRouter(tags=["Login"], prefix="/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/auth/")


@router.get("/")
async def login(request: Request, msg: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.post("/")
async def login(  # noqa: F811
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    errors = []
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        errors.append("Username not found")
    elif user and not pwd_context.verify(password, user.password):
        errors.append("Invalid password")

    if errors:
        return templates.TemplateResponse(
            "/login.html", {"request": request, "errors": errors}
        )

    access_token = generate_token(data={"username": user.username, "userid": user.id})
    response = templates.TemplateResponse(
        "/index.html", {"request": request, "msg": "Successful Login"}
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",
    )
    return response


# TODO: only for use with Swagger
@router.post("/auth/")
def auth(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = (
        db.query(models.User).filter(models.User.username == request.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username not found"
        )
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password"
        )
    # Generating JWT token
    access_token = generate_token(data={"username": user.username, "userid": user.id})

    # return RedirectResponse(url="/dashboard", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credential",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        username: str = payload.get("userid")
        if not username:
            raise credential_exception
        return username
    except JWTError:
        raise credential_exception
