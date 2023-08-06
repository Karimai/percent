import os
from collections import defaultdict
from typing import Annotated

import geopandas as gpd
import matplotlib.pyplot as plt
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt
from sqlalchemy.orm import Session

from config.config import get_db, templates
from repositories import residence_repo

router = APIRouter()


@router.get("/diagram", response_class=HTMLResponse)
def get_chart(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    res_days = defaultdict(lambda: 0)
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM")
        )
        userid = int(payload.get("userid"))
        residences = residence_repo.get_residences(db, userid)
        for residence in residences:
            res_days[residence.country.split(",")[1]] += (
                residence.end_date - residence.start_date
            ).days

        plt.bar(res_days.keys(), res_days.values())
        plt.xlabel("Countries")
        plt.ylabel("Days")
        plt.title("Percentage Distribution")
        plt.savefig("dynamic/chart.png")
        # plt.show()
        plt.close()

        return templates.TemplateResponse("image.html", {"request": request})
    except TypeError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")
    except jwt.ExpiredSignatureError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")


@router.get("/worldmap", response_class=HTMLResponse)
def get_world_map(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
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

        # Create a new column 'color' with default color 'grey'
        world["color"] = "grey"

        # Set the color of the highlighted countries to black
        world.loc[world["name"].isin(highlighted_countries), "color"] = "Visited"

        # Plot the world map with customized colors
        world.plot(
            column="color", legend=True, cmap="Set1", linewidth=0.5, edgecolor="white"
        )

        # Show the map
        plt.savefig("dynamic/chart.png")
        plt.close()
        # plt.show()

        return templates.TemplateResponse("image.html", {"request": request})
    except TypeError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")
    except jwt.ExpiredSignatureError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")
