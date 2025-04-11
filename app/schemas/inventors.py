from app import models

from pydantic import BaseModel

class Inventor(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str

    @classmethod
    def from_model(cls: type["Inventor"], m: models.Inventor):
        return cls(
            first_name=m.first_name,
            last_name=m.last_name,
            country=m.country,
            city=m.city
        )
