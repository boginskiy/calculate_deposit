from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from calculate_deposit.routers import routers
from calculate_deposit.core.database import engine, SessionLocal
from calculate_deposit.deposit.models import Base
from starlette.responses import Response

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(routers)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


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
