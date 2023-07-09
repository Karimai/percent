from typing import List

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
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

app.include_router(user.router)
app.include_router(login.router)
app.include_router(residence.router)
app.include_router(web_residences.router)
app.include_router(diagram.router)

app.mount("/dynamic", StaticFiles(directory="dynamic"), name="dynamic")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    # Create the tables
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
