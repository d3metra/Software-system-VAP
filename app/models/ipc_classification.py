from dataclasses import dataclass

from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class IPCClassification(Base):
    __tablename__ = "ipc_classifications"
    classification_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patents_family: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents_families.app_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ipc_code: Mapped[str] = mapped_column(String(20), ForeignKey(
        "ipc.ipc_code", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    
    __table_args__ = (
        Index("ix_ipc_classifications_patents_family", "patents_family"),
        Index("ix_ipc_classifications_code", "ipc_code")
    )