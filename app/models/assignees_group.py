from dataclasses import dataclass

from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class AssigneesGroup(Base):
    __tablename__ = "assignees_groups"
    group_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patents_family: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents_families.app_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    assignee_id: Mapped[int] = mapped_column(ForeignKey(
        "assignees.assignee_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    
    __table_args__ = (
        Index("ix_assignees_groups_patents_family", "patents_family"),
        Index("ix_assignees_groups_assignee_id", "assignee_id")
    )