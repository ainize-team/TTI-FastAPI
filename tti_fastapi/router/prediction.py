import json
import uuid
from datetime import datetime

import pytz
from celery import Celery
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from redis import Redis
from schemas import AsyncTaskResponse, ImageGenerationRequest, ImageGenerationStatuseResponse

from enums import ResponseStatusEnum


router = APIRouter()


@router.post("/generate", response_class=FileResponse)
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
