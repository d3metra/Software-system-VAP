from app import models

from pydantic import BaseModel

class IPC(BaseModel):
    ipc_code: str

    @classmethod
    def from_model(cls: type["IPC"], m: models.IPC):
        return cls(
            ipc_code=m.ipc_code
        )