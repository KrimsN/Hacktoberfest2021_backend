import typing as t
import logging
import sys
from loguru import logger
from pathlib import Path
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler

VERSION = "0.0.1"


config = Config(".env")  # config file

HOST = config('HOST', cast=str, default='0.0.0.0')
PORT = config('PORT', cast=int, default=8000)

DEBUG: bool = config("DEBUG", cast=bool, default=False)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

APP_NAME: str = config("APP_NAME", default="Hacktoberfest2021_backend")

ALLOWED_HOSTS: t.List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default=["*"],
)


# logging configuration

FILE_LOGGING: bool = config("FILE_LOGGING", cast=bool, default=False)

LOG_FILEPATH: Path = config("LOG_FILEPATH", cast=Path, default='logs/_api.log')
LOG_ROTATION: t.Optional[str] = config("LOG_ROTATION", default=None)
LOG_RETENTION: t.Optional[str] = config("LOG_RETENTION", default=None)
LOG_FORMAT: str = config("LOG_FORMAT", cast=str, default=None)

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO

_LOGGERS = ("uvicorn.asgi", "uvicorn.access", "uvicorn", "fastapi")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in _LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])


_logging_to_file_params = {
    "sink": LOG_FILEPATH,
    "rotation": LOG_ROTATION,
    "retention": LOG_RETENTION,
    "level": LOGGING_LEVEL,
    "enqueue": True,
    "backtrace": True
}
if LOG_FORMAT:
    _logging_to_file_params["format"] = LOG_FORMAT

if FILE_LOGGING:
    logger.add(**_logging_to_file_params)  # type: ignore
