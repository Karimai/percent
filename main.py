import matplotlib.pyplot as plt
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config.config import engine
from sqlalchemy.orm import Session
from models import models
from repositories import login
from routers import residence, user
from repositories.user_repo import create_admin_user

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

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    # Create the tables
    with engine.begin() as connection:
        models.Base.metadata.create_all(bind=connection)
        db = Session(bind=connection)
        # Create an admin user
        create_admin_user(db)


@app.get("/", response_class=HTMLResponse)
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
