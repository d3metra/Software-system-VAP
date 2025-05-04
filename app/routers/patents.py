from app import models
from app.schemas import patents
from app.dependencies.db import get_db
from app.errors import responses, NotFound

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime, timezone

def update_collection_of_pf(pf: models.PatentsFamily, pd: patents.PatentRequest):
    for assignee in pd.assignees_list:
        pf.assignees.append(models.Assignee(assignee_name=assignee.assignee_name,
                                                       assignee_type=assignee.assignee_type,
                                                       country=assignee.country,
                                                       city=assignee.city))
            
    for inventor in pd.inventors_list:
        pf.inventors.append(models.Inventor(first_name=inventor.first_name,
                                                       last_name=inventor.last_name,
                                                       country=inventor.country,
                                                       city=inventor.city))

    for description in pd.descriptions:
        pf.descriptions.append(models.Description(section_name=description.section_name,
                                                             section_content=description.section_content))

    for ipc_code in pd.ipc_codes:
        pf.ipc_codes.append(models.IPC(ipc_code=ipc_code))

    for cpc_code in pd.cpc_codes:
        pf.cpc_codes.append(models.CPC(cpc_code=cpc_code))

def create_patents_family(db: Session, patent_data: patents.PatentRequest) -> models.PatentsFamily:
    patent_family = models.PatentsFamily(app_number=patent_data.app_number,
                                         app_date=patent_data.app_date,
                                         title=patent_data.title,
                                         abstract=patent_data.abstract,
                                         claims=patent_data.claims)
    db.add(patent_family)
    patent_family.main_cpc = patent_data.main_cpc
    
    update_collection_of_pf(patent_family, patent_data)

    return patent_family

def update_patents_family(patent_family: models.PatentsFamily, patent_data: patents.PatentRequest) -> models.PatentsFamily:
    patent_family.assignees = []
    patent_family.inventors = []
    patent_family.descriptions = []
    patent_family.ipc_codes = []
    patent_family.cpc_codes = []

    patent_family.main_cpc = patent_data.main_cpc
    patent_family.title = patent_data.title
    patent_family.abstract = patent_data.abstract
    patent_family.claims = patent_data.claims

    update_collection_of_pf(patent_family, patent_data)

    return patent_family


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
) -> patents.Patent:
    patent_db = db.scalars(
        select(models.Patent).
        where(models.Patent.patent_number == patent_number)
    ).one_or_none()
    
    if patent_db is None:
        raise NotFound(f"Patent {patent_number} not found.")
    
    patent_family_db = db.scalars(
        select(models.PatentsFamily).
        where(models.PatentsFamily.app_number == patent_db.patents_family)
    ).one()

    return patents.Patent.from_model(patent_db, patent_family_db,
                                     assignees_needed=assignees_needed, 
                                     inventors_needed=inventors_needed,
                                     descriptions_needed=description_needed,
                                     citations_needed=citations_needed,
                                     ipc_needed=ipc_needed,
                                     cpc_needed=cpc_needed) 

@patents_router.post("/")
def add_patent(
    *,
    patent_scheme: patents.PatentRequest,
    db: Session = Depends(get_db),
) -> patents.Patent:
    patent = models.Patent(patent_number=patent_scheme.patent_number, type=patent_scheme.type, pub_date=patent_scheme.pub_date)
    db.add(patent)

    for citation in patent_scheme.citations:
        patent.citations.append(models.PatentCitation(cited_patent=citation.cited_patent, 
                                                      date=citation.date))

    patent_family = db.scalars(
        select(models.PatentsFamily).
        where(models.PatentsFamily.app_number == patent_scheme.app_number)
        ).one_or_none()
    
    if not patent_family:
    # Создаём соответствующее патентное семейство в случае его отсутствия
        patent_family = create_patents_family(db, patent_scheme)
        
    else:
    # Находим самый "свежий" патентный документ
        latest_publication_date = patent_scheme.pub_date.replace(tzinfo=None)
        for patent_pub in patent_family.patents:
            print(patent_pub.pub_date, latest_publication_date)
            if patent_pub.pub_date > latest_publication_date:
                latest_publication_date = patent_pub.pub_date
    # Обновляем данные Патентного Семейства, если добавляемый патентный документ самый "свежий"
        if patent_scheme.pub_date.replace(tzinfo=None) == latest_publication_date:
            patent_family = update_patents_family(patent_family, patent_scheme)
    
    # Добавляем текущий патентный документ к семейству
    patent_family.patents.append(patent)

    db.flush()
    db.refresh(patent)
    db.refresh(patent_family)

    return patents.Patent.from_model(patent, patent_family,
                                     assignees_needed=True, 
                                     inventors_needed=True,
                                     descriptions_needed=True,
                                     citations_needed=True,
                                     ipc_needed=True,
                                     cpc_needed=True
                                     )