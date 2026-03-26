from pydantic import BaseModel, EmailStr
from datetime import datetime


class AssigneeCreate(BaseModel):
    name: str
    avatar: str | None = None
    email: EmailStr


class AssigneeUpdate(BaseModel):
    name: str | None = None
    avatar: str | None = None
    email: EmailStr | None = None


class AssigneeOut(BaseModel):
    id: int
    name: str
    avatar: str | None
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}