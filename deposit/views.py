from fastapi import APIRouter
from starlette.responses import JSONResponse, FileResponse
from .schemas import DataCalculate_IN
from . import service

router = APIRouter()


@router.get("/")
def main_page():
    return FileResponse("templates/index.html")


@router.post("/calculate")
def calculate_deposit(item: DataCalculate_IN):
    new_calculate = service.main_calculate_deposit(item)
    return JSONResponse(content=new_calculate)
