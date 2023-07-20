import os
from collections import defaultdict
from typing import Annotated

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
            res_days[residence.country] += (
                residence.end_date - residence.start_date
            ).days
        # import plotly.graph_objects as go
        #
        # fig = go.Figure(data=[go.Bar(x=list(res_days.keys()), y=list(res_days.values()))])
        # fig.update_layout(xaxis_title="Countries", yaxis_title="Days", title="Percentage Distribution")
        # fig.write_image("dynamic/chart.png")

        plt.bar(res_days.keys(), res_days.values())
        plt.xlabel("Countries")
        plt.ylabel("Days")
        plt.title("Percentage Distribution")
        plt.savefig("dynamic/chart.png")
        # plt.show()
        plt.close()
        # import pandas as pd
        # import altair as alt
        #
        # # Assuming res_days is a dictionary with country names as keys and days as values
        # df = pd.DataFrame({"Countries": list(res_days.keys()), "Days": list(res_days.values())})
        #
        # chart = alt.Chart(df).mark_bar().encode(
        #     x="Countries",
        #     y="Days",
        # ).properties(
        #     title="Percentage Distribution"
        # )
        #
        # chart.save("dynamic/chart.png", webdriver="chrome")

        return templates.TemplateResponse("image.html", {"request": request})
    except TypeError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")
    except jwt.ExpiredSignatureError as err:
        return RedirectResponse(url=f"/login?errors={[str(err)]}")
