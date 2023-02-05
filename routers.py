from fastapi import APIRouter
from deposit import views


routers = APIRouter()
routers.include_router(views.router, prefix="")
