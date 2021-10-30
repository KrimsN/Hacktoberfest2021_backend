from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import (
    HOST,
    PORT,
    ALLOWED_HOSTS,
    DEBUG,
    APP_NAME,
    VERSION
)

from app.core.events import create_start_app_handler, create_stop_app_handler
from app.api.routes.api import api_router


def get_application() -> FastAPI:
    application = FastAPI(title=APP_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(api_router)
    return application


app = get_application()

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
