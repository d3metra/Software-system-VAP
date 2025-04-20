from app import models

from pydantic import BaseModel

class Description(BaseModel):
    section_name: str
    section_content: str

    @classmethod
    def from_model(cls: type["Description"], m: models.Description):
        return cls(
            section_name=m.section_name,
            section_content=m.section_content
        )