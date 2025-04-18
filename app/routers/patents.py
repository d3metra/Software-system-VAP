from app import models
from app.schemas import patents, assignees
from app.dependencies.db import get_db
from app.errors import responses, NotFound

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime

patents_router = APIRouter()

@patents_router.get("/{patent_number}", responses=responses)
def get_patent(
    *, 
    db: Session = Depends(get_db),
    patent_number: str,
    assignees_needed: bool = False,
    inventors_needed: bool = False,
    description_needed: bool = False,
    citations_needed: bool = False,
    ipc_needed: bool = False,
    cpc_needed: bool = False
) -> patents.PatentResponse:
    patent_db = db.scalars(
        select(models.Patent).
        where(models.Patent.patent_number == patent_number)
    ).one_or_none()
    
    if patent_db is None:
        raise NotFound(f"Patent {patent_number} not found.")
    return patents.PatentResponse.from_model(patent_db, 
                                     assignees_needed=assignees_needed, 
                                     inventors_needed=inventors_needed,
                                     descriptions_needed=description_needed,
                                     citations_needed=citations_needed,
                                     ipc_needed=ipc_needed,
                                     cpc_needed=cpc_needed) 

@patents_router.post("/")
def add_patent(
    *,
    patent_scheme: patents.Patent,
    db: Session = Depends(get_db),
) -> patents.PatentResponse:
    patent = models.Patent(patent_number=patent_scheme.patent_number, type=patent_scheme.type, pub_date=patent_scheme.pub_date, 
                           app_date=patent_scheme.app_date, title=patent_scheme.title, abstract=patent_scheme.abstract, claims=patent_scheme.claims)
    db.add(patent)

    if patent_scheme.assignees_list:
        for assignee in patent_scheme.assignees_list:
            patent.assignees.append(models.Assignee(assignee_name=assignee.assignee_name, 
                                          assignee_type=assignee.assignee_type,
                                          country=assignee.country,
                                          city=assignee.city
                                          ))
    
    if patent_scheme.inventors_list:
        for inventor in patent_scheme.inventors_list:
            patent.inventors.append(models.Inventor(first_name=inventor.first_name,
                                                    last_name=inventor.last_name,
                                                    country=inventor.country,
                                                    city=inventor.city
                                                    ))

    if patent_scheme.descriptions:
        for description in patent_scheme.descriptions:
            patent.descriptions.append(models.Description(section_name=description.section_name,
                                                          section_content=description.section_content
            ))

    if patent_scheme.citations:
        for citation in patent_scheme.citations:
            patent.citations.append(models.PatentCitation(cited_patent=citation.cited_patent))

    if patent_scheme.ipc_codes:
        for ipc_code in patent_scheme.ipc_codes:
            patent.ipc_codes.append(models.IPC(ipc_code=ipc_code))

    patent.main_cpc = patent_scheme.main_cpc
    if patent_scheme.cpc_codes:
        for cpc_code in patent_scheme.cpc_codes:
            patent.cpc_codes.append(models.CPC(cpc_code=cpc_code))

    db.flush()
    db.refresh(patent)

    return patents.PatentResponse.from_model(patent, 
                                     assignees_needed=True, 
                                     inventors_needed=True,
                                     descriptions_needed=True,
                                     citations_needed=True,
                                     ipc_needed=True,
                                     cpc_needed=True
                                     )