from dataclasses import dataclass

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class IPCClassification(Base):
    __tablename__ = "ipc_classifications"
    classification_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patent_number: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents.patent_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ipc_code: Mapped[str] = mapped_column(String(20), ForeignKey(
        "ipc.ipc_code", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)