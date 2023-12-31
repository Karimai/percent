import os
from pathlib import Path
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

app = FastAPI(
    title="Percent app",
    description="App to figure out how you discovered the world geographically!",
    version="1.0.0",
    terms_of_service="Free of charge!",
    contact={"Developer": "Karim Moradi", "email": "kmoradi.ai@gmail.com"},
)

api_v01 = FastAPI()
app.mount(path="/api/v01", app=api_v01)

ALLOWED_URLS = ["/user/register", "/"]

app.include_router(user.router)
api_v01.include_router(user.api_v01_router)

app.include_router(login.router)
api_v01.include_router(login.api_v01_router)

app.include_router(residence.router)
api_v01.include_router(residence.api_v01_router)

app.include_router(diagram.router)
api_v01.include_router(diagram.api_v01_router)

dynamic_dir = Path(__file__).resolve().parent / "dynamic"
static_dir = Path(__file__).resolve().parent / "static"

app.mount("/dynamic", StaticFiles(directory=str(dynamic_dir)), name="dynamic")
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
api_v01.mount("/dynamic", StaticFiles(directory=str(dynamic_dir)), name="dynamic")
api_v01.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.on_event("startup")
async def startup():
    with engine.begin() as connection:
        models.Base.metadata.create_all(bind=connection)
        db = Session(bind=connection)
        # Create an admin user
        create_admin_user(db)


@app.get("/", include_in_schema=False)
async def index(
    request: Request, msg: str | None = None, errors: List[str] | None = None
):
    return templates.TemplateResponse("index.html", {"request": request, "msg": msg})


@app.middleware("http")
async def access_check(request: Request, call_next):
    if (
        "api" in request.url.path
        or "login" in request.url.path
        or request.url.path not in ALLOWED_URLS
    ):
        response = await call_next(request)
        return response

    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login/")
    try:
        # just to check if the token is still valid.
        # It will raise an exception if it is already expired.
        jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
    except jwt.ExpiredSignatureError:
        response = RedirectResponse(url="/login/")
        response.delete_cookie("access_token")
        return response

    response = await call_next(request)
    return response
