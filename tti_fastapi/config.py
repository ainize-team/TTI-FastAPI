from pydantic import BaseSettings

from enums import EnvEnum


class ServerSettings(BaseSettings):
    app_name: str = "Fast API Server"
    app_version: str = "0.1.0"
    app_env: EnvEnum = EnvEnum.DEV


class FireBaseSettings(BaseSettings):
    firebase_app_name: str = "text-to-image"
    firebase_cred_path: str = "./key/serviceAccountKey.json"
    firebase_database_url: str


class CelerySettings(BaseSettings):
    broker_uri: str


server_settings = ServerSettings()
firebase_settings = FireBaseSettings()
celery_settings = CelerySettings()
