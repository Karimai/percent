from collections import defaultdict
from typing import Annotated

import matplotlib.pyplot as plt
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
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
    residences = residence_repo.get_residences(db, int(request.cookies.get("userid")))
    for residence in residences:
        res_days[residence.country] += (residence.end_date - residence.start_date).days

    plt.bar(res_days.keys(), res_days.values())
    plt.xlabel("Countries")
    plt.ylabel("Percentages")
    plt.title("Percentage Distribution")
    plt.savefig("dynamic/chart.png")
    # plt.show()
    plt.close()

    return templates.TemplateResponse("image.html", {"request": request})
