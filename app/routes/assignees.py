from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Assignee
from app.schemas.assignee import AssigneeCreate, AssigneeUpdate, AssigneeOut

router = APIRouter(prefix="/assignees", tags=["Assignees"])


@router.get("/", response_model=list[AssigneeOut])
def list_assignees(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Assignee).offset(skip).limit(limit).all()


# @router.get("/{assignee_id}", response_model=AssigneeOut)
# def get_assignee(assignee_id: int, db: Session = Depends(get_db)):
#     assignee = db.query(Assignee).filter(Assignee.id == assignee_id).first()
#     if not assignee:
#         raise HTTPException(status_code=404, detail="Assignee not found")
#     return assignee


# @router.post("/", response_model=AssigneeOut, status_code=201)
# def create_assignee(payload: AssigneeCreate, db: Session = Depends(get_db)):
#     existing = db.query(Assignee).filter(Assignee.email == payload.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     assignee = Assignee(**payload.model_dump())
#     db.add(assignee)
#     db.commit()
#     db.refresh(assignee)
#     return assignee


# @router.patch("/{assignee_id}", response_model=AssigneeOut)
# def update_assignee(assignee_id: int, payload: AssigneeUpdate, db: Session = Depends(get_db)):
#     assignee = db.query(Assignee).filter(Assignee.id == assignee_id).first()
#     if not assignee:
#         raise HTTPException(status_code=404, detail="Assignee not found")
#     for field, value in payload.model_dump(exclude_unset=True).items():
#         setattr(assignee, field, value)
#     db.commit()
#     db.refresh(assignee)
#     return assignee


# @router.delete("/{assignee_id}", status_code=204)
# def delete_assignee(assignee_id: int, db: Session = Depends(get_db)):
#     assignee = db.query(Assignee).filter(Assignee.id == assignee_id).first()
#     if not assignee:
#         raise HTTPException(status_code=404, detail="Assignee not found")
#     db.delete(assignee)
#     db.commit()