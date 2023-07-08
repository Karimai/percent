from fastapi import APIRouter, Request

from config.config import templates

router = APIRouter()


@router.get("/")
async def get_residences(request: Request, msg: str = None):
    return templates.TemplateResponse(
        "residence.html", {"request": request, "msg": msg}
    )
