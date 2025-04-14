from dataclasses import dataclass

from sqlalchemy import ForeignKey, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class Description(Base):
    __tablename__ = "descriptions"
    description_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patent_number: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents.patent_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    section_name: Mapped[str] = mapped_column(String(20), nullable=False)
    section_content: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        Index("ix_description_patent_number", "patent_number"),
    )