import matplotlib.pyplot as plt
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from config.config import templates

router = APIRouter()


@router.get("/diagram", response_class=HTMLResponse)
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
