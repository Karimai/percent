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

router = APIRouter()


@router.get("/diagram", response_class=HTMLResponse)
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
    res_days = defaultdict(lambda: 0)
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM")
        )
        userid = int(payload.get("userid"))
        user_directory = f"dynamic/{userid}"
        os.makedirs(user_directory, exist_ok=True)
        residences = residence_repo.get_residences(db, userid)
        for residence in residences:
            if residence.end_date == "present":
                end_date = date.today()
            else:
                end_date = datetime.strptime(residence.end_date, Date_format).date()
            res_days[residence.country.split(",")[1]] += (
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

        plt.bar(percentages.keys(), percentages.values())
        plt.xlabel("Countries")
        plt.ylabel("Days %")
        plt.title("Percentage Distribution")

        plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter())
        plt.yticks(range(0, 101, 5), fontsize=8)

        plt.savefig(f"{user_directory}/bar_plot.png")
        # plt.show()
        plt.close()

        # Pie Plot
        plt.pie(
            sorted_res_days.values(),
            labels=sorted_res_days.keys(),
            autopct="%1.1f%%",
            startangle=140,
        )
        plt.title("Percentage Distribution")
        plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig(f"{user_directory}/pie_plot.png")
        # plt.show()
        plt.close()

        return templates.TemplateResponse(
            "image.html", {"request": request, "user_id": str(userid)}
        )
    except TypeError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")
    except jwt.ExpiredSignatureError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")


@router.get("/worldmap", response_class=HTMLResponse)
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
