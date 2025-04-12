from app import models

from pydantic import BaseModel

class CPC(BaseModel):
    cpc_code: str

    @classmethod
    def from_model(cls: type["CPC"], m: models.CPC):
        return cls(
            cpc_code=m.cpc_code
        )