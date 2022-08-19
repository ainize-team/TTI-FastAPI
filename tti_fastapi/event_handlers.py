import os
from typing import Callable

import open_clip
import torch
from constants import CONFIG_FILE_NAME, MODEL_FILE_NAME
from fastapi import FastAPI
from loguru import logger
from omegaconf import OmegaConf

from config import model_settings
from ldm.util import instantiate_from_config


def _load_model(app: FastAPI) -> None:
    logger.info("Load Model")
    config = OmegaConf.load(os.path.join(model_settings.model_path, CONFIG_FILE_NAME))
    pl_sd = torch.load(os.path.join(model_settings.model_path, MODEL_FILE_NAME))
    sd = pl_sd["state_dict"]
    model = instantiate_from_config(config.model)
    m, u = model.load_state_dict(sd, strict=False)
    if len(m) > 0:
        logger.warning(f"Missing Keys : {m}")
    if len(u) > 0:
        logger.warning(f"Unexpected Keys : {u}")
    if torch.cuda.is_available():
        model = model.half().cuda()
    model.eval()
    app.state.model = model


def _load_clip_model(app: FastAPI) -> None:
    clip_model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai")
    app.state.clip_model = clip_model
    app.state.preprocess = preprocess


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running App Start Handler.")
        _load_model(app)
        _load_clip_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running App Shutdown Handler.")
        del app.state.model

    return shutdown
