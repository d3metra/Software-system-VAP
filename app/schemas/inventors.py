from app import models

from pydantic import BaseModel

class Inventor(BaseModel):
    inventor_id: int
    first_name: str
    last_name: str
    country: str
    city: str

    @classmethod
    def from_model(cls: type["Inventor"], m: models.Inventor):
        return cls(
            inventor_id=m.inventor_id,
            first_name=m.first_name,
            last_name=m.last_name,
            country=m.country,
            city=m.city
        )
