from app import models

from pydantic import BaseModel

class IPC(BaseModel):
    ipc_code: str
    parent_class: str
    title: str

    @classmethod
    def from_model(cls: type["IPC"], m: models.IPC):
        return cls(
            ipc_code=m.ipc_code,
            parent_class=m.parent_class,
            title=m.title
        )