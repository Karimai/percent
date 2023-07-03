import matplotlib.pyplot as plt
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from config.config import engine, templates
from models import models
from repositories.user_repo import create_admin_user
from routers import login, residence, user

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

app.mount("/dynamic", StaticFiles(directory="dynamic"), name="dynamic")

# templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    # Create the tables
    with engine.begin() as connection:
        models.Base.metadata.create_all(bind=connection)
        db = Session(bind=connection)
        # Create an admin user
        create_admin_user(db)


@app.get("/")
async def login_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/diagram", response_class=HTMLResponse)
def get_chart(request: Request):
    countries = ["Iran", "Ukraine", "Netherlands"]
    percentages = [35, 4.5, 1.5]

    plt.bar(countries, percentages)
    plt.xlabel("Countries")
    plt.ylabel("Percentages")
    plt.title("Percentage Distribution")
    plt.savefig("dynamic/chart.png")
    # plt.show()

    return templates.TemplateResponse("image.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": request.cookies.get("username"),
            "access_token": request.cookies.get("access_token"),
        },
    )
