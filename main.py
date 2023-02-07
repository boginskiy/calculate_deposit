from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from calculate_deposit.routers import routers

app = FastAPI()
app.include_router(routers)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request,
                                 exc: RequestValidationError):
    """Функция обработки ошибок при валидации данных."""

    if len(exc.errors()) > 1:
        err_massage = 'All fields are required'
    else:
        err_massage = (f"field {exc.errors()[0]['loc'][1]}: "
                       f"{exc.errors()[0]['msg']}")

    return JSONResponse(status_code=400, content={"error": err_massage})
