from pydantic import BaseModel


class TaskLabelCreate(BaseModel):
    label_id: int


class TaskAssigneeCreate(BaseModel):
    assignee_id: int


class TaskLabelOut(BaseModel):
    task_id: int
    label_id: int
    model_config = {"from_attributes": True}


class TaskAssigneeOut(BaseModel):
    task_id: int
    assignee_id: int
    model_config = {"from_attributes": True}