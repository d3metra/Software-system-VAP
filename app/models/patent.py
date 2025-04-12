from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, sessionmaker, mapped_column, relationship, validates

from . import *

@dataclass
class Patent(Base):
    __tablename__ = "patents"
    patent_number: Mapped[str] = mapped_column(String(55), primary_key=True, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    pub_date: Mapped[datetime] = mapped_column(nullable=False)
    app_date: Mapped[datetime] = mapped_column(nullable=False)
    main_cpc: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    abstract: Mapped[str] = mapped_column(nullable=False)
    claims: Mapped[str] = mapped_column(nullable=False)

    assignees: Mapped[List["Assignee"]] = relationship("Assignee", secondary="assignees_groups", back_populates="patents")
    inventors: Mapped[List["Inventor"]] = relationship("Inventor")
    descriptions: Mapped[List["Description"]] = relationship("Description")
    citations: Mapped[List["PatentCitation"]] = relationship("PatentCitation")
    ipc_codes: Mapped[List["IPC"]] = relationship("IPC")
    cpc_codes: Mapped[List["CPC"]] = relationship("CPC")

    @validates("assignees")
    def _add_assignee(self, _, assignee):
        sess = sessionmaker.object_session(self)
        persistent_assignee = sess.query(Assignee).filter(Assignee.assignee_name == assignee.assignee_name).one_or_none()

        if persistent_assignee:
            return persistent_assignee
        else:
            return assignee