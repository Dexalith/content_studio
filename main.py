import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import app_config
from app.api.auth import router as auth_router


def create_application() -> FastAPI:
    app_instance = FastAPI(
        title=app_config.project_name,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
    )

    app_instance.include_router(auth_router)

    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_instance


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_config.app_host,
        port=app_config.app_port,
        reload=True,
    )