from typing import List
from dataclasses import dataclass

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import *

@dataclass
class CPC(Base):
    __tablename__ = "cpc"
    cpc_code: Mapped[str] = mapped_column(String(20), primary_key=True, nullable=False)
    parent_class: Mapped[str] = mapped_column(String(20), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)

    patents: Mapped[List["Patent"]] = relationship("Patent", secondary="cpc_classifications", back_populates="cpc_codes")