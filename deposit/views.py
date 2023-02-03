from fastapi import APIRouter
from starlette.responses import JSONResponse
from .schemas import DataCalculate_IN
from . import service

router = APIRouter()


@router.post("/calculate")
def calculate_deposit(item: DataCalculate_IN):
    new_calculate = service.main_calculate_deposit(item)
    return JSONResponse(content=new_calculate)
