from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.database import Base


class Assignee(Base):
    __tablename__ = "assignees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    avatar = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    task_assignees = relationship("TaskAssignee", back_populates="assignee", cascade="all, delete-orphan")


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    color = Column(String(7), nullable=False)  # hex color e.g. #FF5733

    task_labels = relationship("TaskLabel", back_populates="label", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="todo")        # e.g. todo, in_progress, done
    priority = Column(String(50), default="medium")    # e.g. low, medium, high
    task_order = Column(Integer, default=0)
    duedate = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    labels = relationship("TaskLabel", back_populates="task", cascade="all, delete-orphan")
    assignees = relationship("TaskAssignee", back_populates="task", cascade="all, delete-orphan")


class TaskLabel(Base):
    __tablename__ = "task_labels"

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    label_id = Column(Integer, ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (UniqueConstraint("task_id", "label_id", name="uq_task_label"),)

    task = relationship("Task", back_populates="labels")
    label = relationship("Label", back_populates="task_labels")


class TaskAssignee(Base):
    __tablename__ = "task_assignees"

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    assignee_id = Column(Integer, ForeignKey("assignees.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (UniqueConstraint("task_id", "assignee_id", name="uq_task_assignee"),)

    task = relationship("Task", back_populates="assignees")
    assignee = relationship("Assignee", back_populates="task_assignees")