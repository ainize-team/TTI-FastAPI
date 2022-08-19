from pydantic import BaseSettings

from enums import EnvEnum


class ServerSettings(BaseSettings):
    app_name: str = "Text To Image Fast API Server"
    app_version: str = "0.1.0"
    app_env: EnvEnum = EnvEnum.DEV


class ModelSettings(BaseSettings):
    model_path: str = "./model"


server_settings = ServerSettings()
model_settings = ModelSettings()
