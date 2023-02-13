from pydantic import BaseSettings

from enums import EnvEnum


class ServerSettings(BaseSettings):
    app_name: str = "Text To Art API Server"
    app_version: str = "0.5.0"
    app_env: EnvEnum = EnvEnum.DEV


class FireBaseSettings(BaseSettings):
    firebase_app_name: str = "text_to_art"
    firebase_cred_path: str = "./key/serviceAccountKey.json"
    firebase_database_url: str


class CelerySettings(BaseSettings):
    broker_base_uri: str


server_settings = ServerSettings()
firebase_settings = FireBaseSettings()
celery_settings = CelerySettings()
