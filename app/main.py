from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles

from app.settings import config
from app.utils.create_dirs import resolve_root_dirs
from app.api import api_router
import app.apps
from app.settings.database import Base, SessionLocal, engine


# Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.PROJECT_NAME, openapi_url=config.API_V1_STR + "/openapi.json")

# CORS
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),


resolve_root_dirs()
# app.mount('/static', StaticFiles(directory="static"), name='static')
app.mount('/media', StaticFiles(directory="media"), name='media')
app.include_router(api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response

