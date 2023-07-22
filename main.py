import os
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from jose import jwt
from sqlalchemy.orm import Session

from config.config import engine, templates
from models import models
from repositories.user_repo import create_admin_user
from routers import login, residence, user
from webapps import diagram
from webapps import residences as web_residences

app = FastAPI(
    title="Percent app",
    description="App to figure out how you discovered the world geographically!",
    version="1.0.0",
    terms_of_service="Free of charge!",
    contact={"Developer": "Karim Moradi", "email": "kmoradi.ai@gmail.com"},
)

ALLOWED_URLS = ["/login", "/login/", "/user/register", "/"]

app.include_router(user.router)
app.include_router(login.router)
app.include_router(residence.router)
app.include_router(web_residences.router)
app.include_router(diagram.router)

app.mount("/dynamic", StaticFiles(directory="dynamic"), name="dynamic")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    with engine.begin() as connection:
        models.Base.metadata.create_all(bind=connection)
        db = Session(bind=connection)
        # Create an admin user
        create_admin_user(db)


@app.get("/")
async def index(
    request: Request, msg: str | None = None, errors: List[str] | None = None
):
    return templates.TemplateResponse("index.html", {"request": request, "msg": msg})


@app.middleware("http")
async def access_check(request: Request, call_next):
    if request.url.path not in ALLOWED_URLS:
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse(url="/login/")
        try:
            # just to check if the token is still valid.
            # It will raise an exception if it is already expired.
            jwt.decode(
                token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM")
            )
        except jwt.ExpiredSignatureError:
            response = RedirectResponse(url="/login/")
            response.delete_cookie("access_token")
            return response
    response = await call_next(request)
    return response
