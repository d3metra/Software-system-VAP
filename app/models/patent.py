from dataclasses import dataclass

from datetime import datetime

from typing import List

from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import *

@dataclass
class Patent(Base):
    __tablename__ = "patents"
    patent_number: Mapped[str] = mapped_column(String(55), primary_key=True, nullable=False)
    patents_family: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents_families.app_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(String(2), nullable=False)
    pub_date: Mapped[datetime] = mapped_column(nullable=False)

    citations: Mapped[List["PatentCitation"]] = relationship("PatentCitation")

    __table_args__ = (
        Index("ix_patents_patents_family", "patents_family"),
    )