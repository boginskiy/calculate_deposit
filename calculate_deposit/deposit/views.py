from fastapi import APIRouter
from starlette.responses import JSONResponse, FileResponse
from .schemas import DataCalculate_IN
from .service import main_calculate_deposit

router = APIRouter()


@router.get("/")
def main_page():
    """Функция выводит человечий интерфейс калькулятора
    для запроса данных."""

    return FileResponse("calculate_deposit/templates/index.html")


@router.post("/calculate")
def calculate_deposit(item: DataCalculate_IN):
    """Функция выводит полученные значения калькулятора."""

    new_calculate = main_calculate_deposit(item)
    return JSONResponse(content=new_calculate)
