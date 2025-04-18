from dataclasses import dataclass

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class AssigneesGroup(Base):
    __tablename__ = "assignees_groups"
    group_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patent_number: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents.patent_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    assignee_id: Mapped[int] = mapped_column(ForeignKey(
        "assignees.assignee_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)