from datetime import datetime

from app import models

from pydantic import BaseModel

class PatentCitation(BaseModel):
    cited_patent: str
    date: datetime

    @classmethod
    def from_model(cls: type["PatentCitation"], m: models.PatentCitation):
        return cls(
            cited_patent=m.cited_patent,
            date=m.date
        )