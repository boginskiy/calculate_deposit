from fastapi import APIRouter
from calculate_deposit.deposit import views

routers = APIRouter()
routers.include_router(views.router, prefix="")
