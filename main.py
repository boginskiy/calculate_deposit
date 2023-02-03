from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from routers import routers
from fastapi.exceptions import RequestValidationError


app = FastAPI()
app.include_router(routers)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(response, exc: RequestValidationError):
    answer = f"field {exc.errors()[0]['loc'][1]}: {exc.errors()[0]['msg']}"
    return JSONResponse(status_code=400,
                        content={"error": answer})
