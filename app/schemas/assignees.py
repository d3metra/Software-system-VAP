from app import models

from pydantic import BaseModel

class Assignee(BaseModel):
    assignee_id: int
    assignee_name: str
    assignee_type: str
    country: str
    city: str

    @classmethod
    def from_model(cls: type["Assignee"], m: models.Assignee):
        return cls(
            assignee_id=m.assignee_id,
            assignee_name=m.assignee_name,
            assignee_type=m.assignee_type,
            county=m.country,
            city=m.city
        )