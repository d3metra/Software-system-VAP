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
    patent = models.Patent(patent_number=patent_scheme.patent_number, type=patent_scheme.type, pub_date=patent_scheme.pub_date)
    db.add(patent)

    for citation in patent_scheme.citations:
        patent.citations.append(models.PatentCitation(cited_patent=citation.cited_patent, 
                                                        date=citation.date
                                                        ))

    patent_family = db.scalars(
        select(models.PatentsFamily).
        where(models.PatentsFamily.app_number == patent_scheme.app_number)
        ).one_or_none()
    
    # Создаём соответствующее патентное семейство в случае его отсутствия
    if not patent_family:
        patent_family = models.PatentsFamily(app_number=patent_scheme.app_number,
                                             app_date=patent_scheme.app_date,
                                             main_cpc=patent_scheme.main_cpc,
                                             title=patent_scheme.title,
                                             abstract=patent_scheme.abstract,
                                             claims=patent_scheme.claims)
        db.add(patent_family)

    # Находим самый "свежий" патентный документ
    latest_publication_date = patent_scheme.pub_date
    for patent_pub in patent_family.patents:
        if patent_pub.pub_date > latest_publication_date:
            latest_publication_date = patent_pub.pub_date
    
    # Добавляем текущий патентный документ к семейству
    patent_family.patents.append(patent)

    # Обновляем данные Патентного Семейства, если добавляемый патентный документ первый или самый "свежий"
    if patent_scheme.pub_date == latest_publication_date:

        patent_family.main_cpc = patent_scheme.main_cpc
        patent_family.title = patent_scheme.title
        patent_family.abstract = patent_scheme.abstract
        patent_family.claims = patent_scheme.claims

        for assignee in patent_scheme.assignees_list:
            patent_family.assignees.append(models.Assignee(assignee_name=assignee.assignee_name,
                                                           assignee_type=assignee.assignee_type,
                                                           country=assignee.country,
                                                           city=assignee.city))
            
        for inventor in patent_scheme.inventors_list:
            patent_family.inventors.append(models.Inventor(first_name=inventor.first_name,
                                                           last_name=inventor.last_name,
                                                           country=inventor.country,
                                                           city=inventor.city))

        for description in patent_scheme.descriptions:
            patent_family.descriptions.append(models.Description(section_name=description.section_name,
                                                                 section_content=description.section_content))

        for ipc_code in patent_scheme.ipc_codes:
            patent_family.ipc_codes.append(models.IPC(ipc_code=ipc_code))

        for cpc_code in patent_scheme.cpc_codes:
            patent_family.cpc_codes.append(models.CPC(cpc_code=cpc_code))

    db.flush()
    db.refresh(patent)
    db.refresh(patent_family)

    return patents.PatentResponse.from_model(patent, patent_family,
                                     assignees_needed=True, 
                                     inventors_needed=True,
                                     descriptions_needed=True,
                                     citations_needed=True,
                                     ipc_needed=True,
                                     cpc_needed=True
                                     )