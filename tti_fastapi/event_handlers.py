from typing import Callable

import firebase_admin
from celery import Celery
from fastapi import FastAPI
from firebase_admin import credentials
from loguru import logger

from config import celery_settings, firebase_settings


def _setup_firebase(app: FastAPI) -> None:
    cred = credentials.Certificate(firebase_settings.firebase_cred_path)
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": firebase_settings.firebase_database_url
        },
    )


def _setup_celery(app: FastAPI) -> None:
    logger.info("Setup Celery")
    app.state.celery = Celery(broker=celery_settings.broker_uri)


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running App Start Handler.")
        _setup_firebase(app)
        _setup_celery(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running App Shutdown Handler.")
        del app.state.celery
        del app.state.firebase

    return shutdown
