from dataclasses import dataclass

from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class CPCClassification(Base):
    __tablename__ = "cpc_classifications"
    classification_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patent_number: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents.patent_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    cpc_code: Mapped[str] = mapped_column(String(20), ForeignKey(
        "cpc.cpc_code", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    
    __table_args__ = (
        Index("ix_cpc_classifications_patent_number", "patent_number"),
        Index("ix_cpc_classifications_code", "cpc_code")
    )