from typing import List
from dataclasses import dataclass

from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import *

@dataclass
class Assignee(Base):
    __tablename__ = "assignees"
    assignee_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    assignee_name: Mapped[str] = mapped_column(String(50), nullable=False)
    assignee_type: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    city: Mapped[str] = mapped_column(String(30), nullable=False)

    patents: Mapped[List["Patent"]] = relationship("Patent", secondary="assignees_groups", back_populates="assignees")

    __table_args__ = (
        Index("ix_assignee_name", "assignee_name"),
    )