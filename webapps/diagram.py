import os
from collections import defaultdict
from datetime import date, datetime
from typing import Annotated

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt
from sqlalchemy.orm import Session

from config.config import Date_format, get_db, templates
from repositories import residence_repo

router = APIRouter(tags=["Views"])
api_v01_router = APIRouter(tags=["Views"])


class PlotGenerator:
    def __init__(self, user_id, residences, db):
        self.user_id = user_id
        self.residences = residences
        self.db = db
        self.user_directory = f"dynamic/{self.user_id}"
        os.makedirs(self.user_directory, exist_ok=True)

    def generate_plots(self):
        res_days = defaultdict(int)
        for residence in self.residences:
            if residence.end_date == "present":
                end_date = date.today()
            else:
                end_date = datetime.strptime(residence.end_date, Date_format).date()

            res_days[residence.country.split(",")[1]] = (
                end_date - residence.start_date
            ).days

        sorted_res_days = dict(
            sorted(res_days.items(), key=lambda item: item[1], reverse=True)
        )
        total_days = sum(res_days.values())
        percentages = {
            country: (days / total_days) * 100
            for country, days in sorted_res_days.items()
        }

        self.generate_bar_plot(percentages)
        self.generate_pie_plot(sorted_res_days)

    def generate_bar_plot(self, percentages):
        plt.bar(percentages.keys(), percentages.values())
        plt.xlabel("Countries")
        plt.ylabel("Days %")
        plt.title("Percentage Distribution")
        plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter())
        plt.yticks(range(0, 101, 5), fontsize=8)
        plt.savefig(f"{self.user_directory}/bar_plot.png")
        plt.close()

    def generate_pie_plot(self, sorted_res_days):
        plt.pie(
            sorted_res_days.values(),
            labels=sorted_res_days.keys(),
            autopct="%1.1f%%",
            startangle=140,
        )
        plt.title("Percentage Distribution")
        plt.axis("equal")
        plt.savefig(f"{self.user_directory}/pie_plot.png")
        plt.close()


@router.get("/diagram", response_class=HTMLResponse, include_in_schema=False)
@api_v01_router.get("/diagram", response_class=HTMLResponse)
def get_chart(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Generate and display diagrams showing percentage distribution of residence days by country.

    :param request: The HTTP request object.
    :param db: The database session dependency.
    :return: A template response displaying the generated diagrams.
    """
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM")
        )
        user_id = int(payload.get("userid"))
        residences = residence_repo.get_residences(db, user_id)

        plot_generator = PlotGenerator(user_id=user_id, residences=residences, db=db)
        plot_generator.generate_plots()

        return templates.TemplateResponse(
            "image.html", {"request": request, "user_id": str(user_id)}
        )
    except TypeError as err:
        print(str(err))
        return RedirectResponse(url="/login")
    except jwt.ExpiredSignatureError as err:
        print(str(err))
        return RedirectResponse(url="/login")


@router.get("/worldmap", response_class=HTMLResponse, include_in_schema=False)
@api_v01_router.get("/worldmap", response_class=HTMLResponse)
def get_world_map(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Generate and display a world map highlighting countries visited by the user.

    :param request: The HTTP request object.
    :param db: The database session dependency.
    :return: A template response displaying the generated world map.
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
        highlighted_countries = []
        for residence in residences:
            highlighted_countries.append(residence.country.split(",")[0])

        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

        world["color"] = "grey"

        world.loc[world["name"].isin(highlighted_countries), "color"] = "Visited"

        world.plot(
            column="color", legend=True, cmap="Set1", linewidth=0.5, edgecolor="white"
        )

        user_directory = f"dynamic/{userid}"
        os.makedirs(user_directory, exist_ok=True)
        plt.savefig(f"{user_directory}/world_map.png")
        plt.close()
        # plt.show()

        return templates.TemplateResponse(
            "map.html", {"request": request, "user_id": str(userid)}
        )
    except TypeError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")
    except jwt.ExpiredSignatureError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")
