from fastapi import APIRouter

from app.apps import login
from app.apps.users import routes as user_routes
from app.apps.mspt import routes as mspt_routes

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
api_router.include_router(mspt_routes.files_router, prefix="/mspt", tags=["mspt"])
api_router.include_router(mspt_routes.instrument_router, prefix="/mspt", tags=["mspt"])
api_router.include_router(mspt_routes.style_router, prefix="/mspt", tags=["mspt"])
api_router.include_router(mspt_routes.strategy_router, prefix="/mspt", tags=["mspt"])
api_router.include_router(mspt_routes.trade_router, prefix="/mspt", tags=["mspt"])
api_router.include_router(mspt_routes.task_router, prefix="/mspt", tags=["mspt"])
api_router.include_router(mspt_routes.trading_plan_router, prefix="/mspt", tags=["mspt"])
api_router.include_router(mspt_routes.study_router, prefix="/mspt", tags=["mspt"])
api_router.include_router(mspt_routes.statistics_router, prefix="/performance", tags=["mspt"])

