import typing as t

from fastapi import FastAPI
from loguru import logger


def create_start_app_handler(app: FastAPI) -> t.Callable:
    @logger.catch
    async def start_handler():
        pass
    return start_handler


def create_stop_app_handler(app: FastAPI) -> t.Callable:
    @logger.catch
    async def stop_handler():
        pass
    return stop_handler
