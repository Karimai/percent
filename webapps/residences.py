from fastapi import APIRouter, Request

from config.config import templates

router = APIRouter(include_in_schema=False)


@router.route("/")
async def get_residences(request: Request):
    return templates.TemplateResponse("residence.html", {"request": request})
