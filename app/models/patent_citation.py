from dataclasses import dataclass

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class PatentCitation(Base):
    __tablename__ = "patent_citations"
    citation_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patent_number: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents.patent_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    cited_patent: Mapped[str] = mapped_column(String(55), nullable=False)
