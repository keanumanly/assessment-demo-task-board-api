from pydantic import BaseModel, Field
from typing import Optional


class PostingData(BaseModel):
    id: str = Field(..., title="Id")
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")
    status: str = Field(..., title="Status")
    priority: str = Field(..., title="Priority")
    order: int = Field(..., title="Order")
    labels: Optional[list] = Field(..., title="Labels")
    dueDate: str = Field(..., title="dueDate")
    createdAt: str = Field(..., title="createdAt")
    updatedAt: str = Field(..., title="updatedAt")

    class Config:

        def __init__(self):
            pass

        json_schema_extra = {
            "example": {
                "id": "",
                "title": "",
                "description": "",
                "status": "",
                "priority": "",
                "order": 0,
                "labels": [],
                "dueDate": "",
                "createdAt": "",
                "updatedAt": "",
            }
        }
