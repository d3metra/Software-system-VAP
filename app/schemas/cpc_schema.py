from typing import Optional

from pydantic import BaseModel

from app import models

class CPCMeta(BaseModel):
    parent_class: Optional[str]
    title: Optional[str]

class CPC(CPCMeta):
    cpc_code: str

    @classmethod
    def from_model(cls: type["CPC"], m: models.CPC):
        return cls(
            cpc_code=m.cpc_code,
            parent_class=m.parent_class,
            title=m.title
        )