from dataclasses import dataclass

from datetime import datetime

from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class PatentCitation(Base):
    __tablename__ = "patent_citations"
    citation_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patent_number: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents.patent_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    cited_patent: Mapped[str] = mapped_column(String(55), nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (
        Index("ix_citations_patent_number", "patent_number"),
    )
