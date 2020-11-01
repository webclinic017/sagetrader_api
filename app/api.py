from fastapi import APIRouter

from app.apps import login
from app.apps.users import routes as user_routes
from app.apps.mspt import routes as mspt_routes


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
api_router.include_router(mspt_routes.router, prefix="/mspt", tags=["mspt"])
