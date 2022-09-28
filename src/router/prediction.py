import uuid
from datetime import datetime

import fastapi
from celery import Celery
from fastapi import APIRouter, HTTPException, Request, status
from firebase_admin import db

from config import firebase_settings
from enums import ResponseStatusEnum
from schemas import AsyncTaskResponse, ImageGenerationRequest, ImageGenerationResponse


router = APIRouter()


@router.post("/generate", response_model=AsyncTaskResponse)
def post_generation(
    request: Request,
    data: ImageGenerationRequest,
):
    celery: Celery = request.app.state.celery
    now = datetime.utcnow().timestamp()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    try:
        celery.send_task(
            name="generate",
            kwargs={
                "task_id": task_id,
                "data": dict(data),
            },
            queue="tti",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Celery Error({task_id}): {e}")
    try:
        ref = db.reference(f"{firebase_settings.firebase_app_name}/{task_id}")
        request_body = data.dict()
        request_body["status"] = ResponseStatusEnum.PENDING
        request_body["updated_at"] = now
        ref.set(request_body)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"FireBaseError({task_id}): {e}")
    return AsyncTaskResponse(task_id=task_id, updated_at=now)


@router.get("/result/{task_id}", response_model=ImageGenerationResponse)
async def get_result(task_id: str):
    try:
        ref = db.reference(f"{firebase_settings.firebase_app_name}/{task_id}")
        data = ref.get()
        if data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Task ID({task_id}) not found")
        if data["status"] == ResponseStatusEnum.ERROR:
            raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"]["error_message"])
        return ImageGenerationResponse(
            status=data["status"],
            updated_at=data["updated_at"],
            result=data["results"] if data["status"] == ResponseStatusEnum.COMPLETED else None,
        )
    except Exception as e:
        raise HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"FireBaseError({task_id}): {e}"
        )
