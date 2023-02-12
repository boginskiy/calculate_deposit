from typing import List
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse, FileResponse
from .schemas import DataCalculate_IN, DataCalculate_OUT
from ..core.utils import get_db
from .service import main_calculate_deposit, get_data_deposit
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def main_page():
    """Функция выводит человечий интерфейс калькулятора
    для запроса данных."""

    return FileResponse("calculate_deposit/templates/index.html")


@router.get("/deposit", response_model=List[DataCalculate_OUT])
def get_data_bd(db: Session = Depends(get_db)):
    """Функция выводит последние добавленные данные в БД."""

    data_deposit = get_data_deposit(db)
    return data_deposit


@router.post("/calculate")
def calculate_deposit(item: DataCalculate_IN, db: Session = Depends(get_db)):
    """Функция выводит полученные значения калькулятора
    и собирает данные в базу данных."""

    new_calculate = main_calculate_deposit(db, item)
    return JSONResponse(content=new_calculate)
