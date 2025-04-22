from dataclasses import dataclass

from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

@dataclass
class Inventor(Base):
    __tablename__ = "inventors"
    inventor_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    patents_family: Mapped[str] = mapped_column(String(55), ForeignKey(
        "patents_families.app_number", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    city: Mapped[str] = mapped_column(String(30), nullable=False)

    __table_args__ = (
        Index("ix_inventors_patents_family", "patents_family"),
    )