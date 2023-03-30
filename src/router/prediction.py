import uuid
from datetime import datetime
from typing import Dict, Union

from celery import Celery
from fastapi import APIRouter, HTTPException, Request, status
from firebase_admin import db

from config import firebase_settings
from enums import ResponseStatusEnum
from schemas import (
    AsyncTaskResponse,
    ImageGenerationParams,
    ImageGenerationRequest,
    ImageGenerationResponse,
    ImageGenerationTxHashResponse,
)


router = APIRouter()


@router.post("/generate", response_model=AsyncTaskResponse)
def post_generation(
    request: Request,
    data: ImageGenerationRequest,
):
    celery_dict: Dict[str, Celery] = request.app.state.celery
    model_id = data.params.model_id
    if model_id not in celery_dict:
        valid_model_ids = ", ".join(list(celery_dict.keys()))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only Support : {valid_model_ids}")
    celery = celery_dict[model_id]
    now = int(datetime.utcnow().timestamp() * 1000)
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    request_data = data.params.dict()
    try:
        celery.send_task(
            name="generate",
            kwargs={
                "task_id": task_id,
                "data": request_data,
            },
            queue="tti",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Celery Error({task_id}): {e}")
    try:
        ref = db.reference(f"{firebase_settings.firebase_app_name}/tasks/{task_id}")
        request_body = {
            "message": {
                "guild_id": data.discord.guild_id,
                "channel_id": data.discord.channel_id,
                "message_id": data.discord.message_id,
            },
            "request": request_data,
            "status": ResponseStatusEnum.PENDING,
            "updated_at": now,
            "user_id": data.discord.user_id,
        }
        ref.set(request_body)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"FireBaseError({task_id}): {e}")
    return AsyncTaskResponse(task_id=task_id, updated_at=now)


@router.get("/tasks/{task_id}/images", response_model=ImageGenerationResponse)
async def get_task_image(task_id: str):
    try:
        ref = db.reference(f"{firebase_settings.firebase_app_name}/tasks/{task_id}")
        data = ref.get()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"FireBaseError({task_id}): {e}")
    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Task ID({task_id}) not found")
    if data["status"] == ResponseStatusEnum.ERROR:
        return ImageGenerationResponse(
            status=data["status"],
            updated_at=data["updated_at"],
            result=data["error"]["error_message"],
        )
    return ImageGenerationResponse(
        status=data["status"],
        updated_at=data["updated_at"],
        result=data["response"] if data["status"] == ResponseStatusEnum.COMPLETED else None,
    )


@router.get("/tasks/{task_id}/params", response_model=ImageGenerationParams)
async def get_task_params(task_id: str):
    try:
        ref = db.reference(f"{firebase_settings.firebase_app_name}/tasks/{task_id}/request")
        data = ref.get()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"FireBaseError({task_id}): {e}")
    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Task ID({task_id}) not found")
    return ImageGenerationParams(
        prompt=data["prompt"],
        negative_prompt=data["negative_prompt"],
        steps=data["steps"],
        seed=data["seed"],
        width=data["width"],
        height=data["height"],
        images=data["images"],
        guidance_scale=data["guidance_scale"],
        model_id=data["model_id"],
        scheduler_type=data["scheduler_type"],
    )


@router.get("/tasks/{task_id}/tx-hash", response_model=Union[ImageGenerationTxHashResponse, ImageGenerationResponse])
async def get_tx_hash(task_id: str):
    try:
        ref = db.reference(f"{firebase_settings.firebase_app_name}/tasks/{task_id}")
        data = ref.get()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"FireBaseError({task_id}): {e}")
    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Task ID({task_id}) not found")
    if data["status"] == ResponseStatusEnum.ERROR:
        return ImageGenerationResponse(
            status=data["status"],
            updated_at=data["updated_at"],
            result=data["error"]["error_message"],
        )
    return ImageGenerationTxHashResponse(
        status=data["status"],
        result=data["tx_hash"],
        updated_at=data["updated_at"],
    )
