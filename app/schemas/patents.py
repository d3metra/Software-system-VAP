
from datetime import datetime
from typing import Any, List

from pydantic import BaseModel

from app import models
from app.schemas import assignees, inventors, descriptions, patent_citations, ipc_schema, cpc_schema

class Patent(BaseModel):
    patent_number: str
    type: str
    pub_date: datetime
    app_date: datetime
    main_cpc: str
    title: str
    abstract: str
    claims: str

    assignees_list: List[assignees.Assignee]
    inventors_list: List[inventors.Inventor]
    descriptions: List[descriptions.Description]
    citations: List[patent_citations.PatentCitation]
    ipc_codes: List[ipc_schema.IPC]
    cpc_codes: List[cpc_schema.CPC]

    @classmethod
    def from_model(cls: type["Patent"], m: models.Patent, 
                   assignees_needed: bool = False, 
                   inventors_needed: bool = False,
                   descriptions_needed: bool = False,
                   citations_needed: bool = False,
                   ipc_needed: bool = False,
                   cpc_needed: bool = False):
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
            inventors_list=[inventors.Inventor.from_model(inventor) for inventor in m.inventors] if inventors_needed else [],
            descriptions=[descriptions.Description.from_model(description) for description in m.descriptions] if descriptions_needed else[],
            citations=[patent_citations.PatentCitation.from_model(citation) for citation in m.citations] if citations_needed else [],
            ipc_codes=[ipc_schema.IPC.from_model(ipc_code) for ipc_code in m.ipc_codes] if ipc_needed else [],
            cpc_codes=[cpc_schema.CPC.from_model(cpc_code) for cpc_code in m.cpc_codes] if cpc_needed else []
        )