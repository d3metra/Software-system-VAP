
from datetime import datetime
from typing import Any, List

from pydantic import BaseModel

from app import models
from app.schemas import assignees, inventors

class Patent(BaseModel):
    patent_number: str
    type: str
    pub_date: datetime
    app_date: datetime
    main_cpc: str
    title: str
    abstract: str
    claims: str

    assignees_list: List[assignees.Assignee] = []
    inventors_list: List[inventors.Inventor] = []

    @classmethod
    def from_model(cls: type["Patent"], m: models.Patent, assignees_needed: bool = False, inventors_needed: bool = False):
        return cls(
            patent_number=m.patent_number,
            type=m.type,
            pub_date=m.pub_date,
            app_date=m.app_date,
            main_cpc=m.main_cpc,
            title=m.title,
            abstract=m.abstract,
            claims=m.claims,
            assignees_list=[assignees.Assignee.from_model(assignee) for assignee in m.assignees] if assignees_needed else [],
            inventors_list=[inventors.Inventor.from_model(inventor) for inventor in m.inventors] if inventors_needed else []
        )