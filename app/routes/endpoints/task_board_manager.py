from fastapi import APIRouter, Query
from typing import Optional
from models.schema_api import PostingData
from utils.taskboard_handler import (
    get_request,
    execute_label_request,
    execute_assignees_request,
    post_request,
    put_request,
    del_request
)

router = APIRouter()


@router.get("/labels")
async def get_labels():
    result = execute_label_request()
    return result


@router.get("/assignees")
async def get_assignees():
    result = execute_assignees_request()
    return result


@router.get("/tasks")
async def get_items():
    result = get_request()
    return result


@router.post("/tasks")
async def post_items(response_model: PostingData):
    result = post_request(response_model)
    return result


@router.put("/tasks")
async def put_items(response_model: PostingData):
    result = put_request(response_model)
    return result


@router.delete("/tasks")
async def delete_items(uuid: Optional[str] = Query(None)):
    result = del_request(uuid)
    return result
