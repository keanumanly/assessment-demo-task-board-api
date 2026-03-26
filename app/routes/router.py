from fastapi import APIRouter, Depends
from .endpoints import task_board_manager
from utils.auth import authenticate

router = APIRouter()


router.include_router(task_board_manager.router, tags=["Task Board API Manager"], dependencies=[Depends(authenticate)])
