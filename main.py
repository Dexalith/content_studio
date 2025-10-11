import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import app_config


def create_application() -> FastAPI:
    app_instance = FastAPI(
        title=app_config.project_name,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
    )

app = create_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)