from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, sessionmaker, mapped_column, relationship, validates

from . import *

@dataclass
class PatentsFamily(Base):
    __tablename__ = "patents_families"
    app_number: Mapped[str] = mapped_column(String(55), primary_key=True, nullable=False)
    app_date: Mapped[datetime] = mapped_column(nullable=False)
    main_cpc: Mapped[str] = mapped_column(String(20), ForeignKey(
        "cpc.cpc_code", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    abstract: Mapped[str] = mapped_column(nullable=False)
    claims: Mapped[str] = mapped_column(nullable=False)

    patents: Mapped[List["Patent"]] = relationship("Patent")
    assignees: Mapped[List["Assignee"]] = relationship("Assignee", secondary="assignees_groups", back_populates="patents_families")
    inventors: Mapped[List["Inventor"]] = relationship("Inventor")
    descriptions: Mapped[List["Description"]] = relationship("Description")
    ipc_codes: Mapped[List["IPC"]] = relationship("IPC", secondary="ipc_classifications", back_populates="patents_families")
    cpc_codes: Mapped[List["CPC"]] = relationship("CPC", secondary="cpc_classifications", back_populates="patents_families")

    @validates("assignees")
    def _add_assignee(self, _, assignee):
        sess = sessionmaker.object_session(self)
        persistent_assignee = sess.query(Assignee).filter(Assignee.assignee_name == assignee.assignee_name).one_or_none()

        if persistent_assignee:
            return persistent_assignee
        else:
            return assignee
        
    @validates("ipc_codes")
    def _add_icp_code(self, _, ipc):
        sess = sessionmaker.object_session(self)
        persistent_icp_code = sess.query(IPC).filter(IPC.ipc_code == ipc.ipc_code).one_or_none()

        if persistent_icp_code:
            return persistent_icp_code
        else:
            return ipc
        
    @validates("cpc_codes")
    def _add_cpc_code(self, _, cpc):
        sess = sessionmaker.object_session(self)
        persistent_cpc_code = sess.query(CPC).filter(CPC.cpc_code == cpc.cpc_code).one_or_none()

        if persistent_cpc_code:
            return persistent_cpc_code
        else:
            return cpc

    @validates("main_cpc")
    def _add_main_cpc(self, _, main_cpc):
        sess = sessionmaker.object_session(self)

        if not sess.query(CPC).filter(CPC.cpc_code == main_cpc).one_or_none():
            sess.add(CPC(cpc_code=main_cpc))
        return main_cpc
       