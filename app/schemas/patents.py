
from datetime import datetime
from typing import Any, List

from pydantic import BaseModel

from app import models
from app.schemas import assignees, inventors, descriptions, patent_citations, ipc_schema, cpc_schema

class PatentBase(BaseModel):
    patent_number: str
    type: str
    pub_date: datetime
    app_number: str
    app_date: datetime
    main_cpc: str
    title: str
    abstract: str
    claims: str

    assignees_list: List[assignees.Assignee]
    inventors_list: List[inventors.Inventor]
    descriptions: List[descriptions.Description]
    citations: List[patent_citations.PatentCitation]

class Patent(PatentBase):
    ipc_codes: List[str]
    cpc_codes: List[str]

class PatentResponse(PatentBase):
    ipc_codes: List[ipc_schema.IPC]
    cpc_codes: List[cpc_schema.CPC]

    @classmethod
    def from_model(cls: type["Patent"], mP: models.Patent, mF: models.PatentsFamily, 
                   assignees_needed: bool = False, 
                   inventors_needed: bool = False,
                   descriptions_needed: bool = False,
                   citations_needed: bool = False,
                   ipc_needed: bool = False,
                   cpc_needed: bool = False):
        return cls(
            patent_number=mP.patent_number,
            type=mP.type,
            pub_date=mP.pub_date,
            app_number=mF.app_number,
            app_date=mF.app_date,
            main_cpc=mF.main_cpc,
            title=mF.title,
            abstract=mF.abstract,
            claims=mF.claims,
            assignees_list=[assignees.Assignee.from_model(assignee) for assignee in mF.assignees] if assignees_needed else [],
            inventors_list=[inventors.Inventor.from_model(inventor) for inventor in mF.inventors] if inventors_needed else [],
            descriptions=[descriptions.Description.from_model(description) for description in mF.descriptions] if descriptions_needed else[],
            citations=[patent_citations.PatentCitation.from_model(citation) for citation in mP.citations] if citations_needed else [],
            ipc_codes=[ipc_schema.IPC.from_model(ipc_code) for ipc_code in mF.ipc_codes] if ipc_needed else [],
            cpc_codes=[cpc_schema.CPC.from_model(cpc_code) for cpc_code in mF.cpc_codes] if cpc_needed else []
        )