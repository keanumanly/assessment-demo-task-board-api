from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.models import Task, TaskLabel, TaskAssignee, Label, Assignee
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.schemas.task_relations import (
    TaskLabelCreate, TaskLabelOut,
    TaskAssigneeCreate, TaskAssigneeOut
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_or_404(task_id: int, db: Session) -> Task:
    task = (
        db.query(Task)
        .options(
            joinedload(Task.labels).joinedload(TaskLabel.label),
            joinedload(Task.assignees).joinedload(TaskAssignee.assignee),
        )
        .filter(Task.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# ── Task CRUD ──────────────────────────────────────────────────

@router.post("/", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return get_task_or_404(task.id, db)


@router.get("/", response_model=list[TaskOut])
def list_tasks(
    status: str | None = None,
    priority: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Task).options(
        joinedload(Task.labels).joinedload(TaskLabel.label),
        joinedload(Task.assignees).joinedload(TaskAssignee.assignee),
    )
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    return query.order_by(Task.task_order).offset(skip).limit(limit).all()


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return get_task_or_404(task_id, db)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    return get_task_or_404(task_id, db)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()


# ── Task ↔ Labels ─────────────────────────────────────────────

@router.post("/{task_id}/labels", response_model=TaskLabelOut, status_code=201)
def add_label_to_task(task_id: int, payload: TaskLabelCreate, db: Session = Depends(get_db)):
    if not db.query(Task).filter(Task.id == task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")
    if not db.query(Label).filter(Label.id == payload.label_id).first():
        raise HTTPException(status_code=404, detail="Label not found")
    existing = db.query(TaskLabel).filter_by(task_id=task_id, label_id=payload.label_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Label already attached to task")
    task_label = TaskLabel(task_id=task_id, label_id=payload.label_id)
    db.add(task_label)
    db.commit()
    db.refresh(task_label)
    return task_label


@router.delete("/{task_id}/labels/{label_id}", status_code=204)
def remove_label_from_task(task_id: int, label_id: int, db: Session = Depends(get_db)):
    task_label = db.query(TaskLabel).filter_by(task_id=task_id, label_id=label_id).first()
    if not task_label:
        raise HTTPException(status_code=404, detail="Task-label relation not found")
    db.delete(task_label)
    db.commit()


# ── Task ↔ Assignees ──────────────────────────────────────────

@router.post("/{task_id}/assignees", response_model=TaskAssigneeOut, status_code=201)
def add_assignee_to_task(task_id: int, payload: TaskAssigneeCreate, db: Session = Depends(get_db)):
    if not db.query(Task).filter(Task.id == task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")
    if not db.query(Assignee).filter(Assignee.id == payload.assignee_id).first():
        raise HTTPException(status_code=404, detail="Assignee not found")
    existing = db.query(TaskAssignee).filter_by(task_id=task_id, assignee_id=payload.assignee_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Assignee already assigned to task")
    task_assignee = TaskAssignee(task_id=task_id, assignee_id=payload.assignee_id)
    db.add(task_assignee)
    db.commit()
    db.refresh(task_assignee)
    return task_assignee


@router.delete("/{task_id}/assignees/{assignee_id}", status_code=204)
def remove_assignee_from_task(task_id: int, assignee_id: int, db: Session = Depends(get_db)):
    task_assignee = db.query(TaskAssignee).filter_by(task_id=task_id, assignee_id=assignee_id).first()
    if not task_assignee:
        raise HTTPException(status_code=404, detail="Task-assignee relation not found")
    db.delete(task_assignee)
    db.commit()