import json
import uuid
from datetime import datetime

import fastapi
import pytz
from celery import Celery
from fastapi import APIRouter, HTTPException, Request
from redis import Redis
from schemas import AsyncTaskResponse, ImageGenerationRequest, ImageGenerationStatuseResponse

from enums import ResponseStatusEnum


router = APIRouter()


@router.post("/generate", response_class=AsyncTaskResponse)
def post_generation(request: Request, data: ImageGenerationRequest):
    redis: Redis = request.app.state.redis
    celery: Celery = request.app.state.celery
    now = datetime.utcnow().replace(tzinfo=pytz.utc).timestamp()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    response = ImageGenerationStatuseResponse(status=ResponseStatusEnum.PENDING, updated_at=now)
    redis.set(task_id, json.dumps(dict(response)))
    celery.send_task(
        name="generate",
        kwargs={
            "task_id": task_id,
            "data": dict(data),
        },
        queue="tti",
    )
    return AsyncTaskResponse(task_id=task_id)


@router.get("/status/{task_id}", response_class=ImageGenerationStatuseResponse)
async def get_result(request: Request, task_id: str):
    redis: Redis = request.app.state.redis
    data = json.loads(redis.get(task_id))
    if data is None:
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=f"Task ID({task_id}) not found")
    if hasattr(data, "message"):
        raise HTTPException(status_code=data["status_code"], detail=data["message"])
    return ImageGenerationStatuseResponse(status=data["status"], result=data["result"], updated_at=data["updated_at"])
