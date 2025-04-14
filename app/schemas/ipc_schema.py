from typing import Optional

from pydantic import BaseModel

from app import models

class IPC(BaseModel):
    ipc_code: str
    parent_class: Optional[str]
    title: Optional[str] 

    @classmethod
    def from_model(cls: type["IPC"], m: models.IPC):
        return cls(
            ipc_code=m.ipc_code,
            parent_class=m.parent_class,
            title=m.title
        )