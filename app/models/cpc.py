from dataclasses import dataclass

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from . import *

@dataclass
class CPC(Base):
    __tablename__ = "cpc"
    cpc_code: Mapped[str] = mapped_column(String(20), primary_key=True, nullable=False)
    parent_class: Mapped[str] = mapped_column(String(20), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
