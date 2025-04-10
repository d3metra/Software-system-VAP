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
    inventors_needed: bool = False
) -> patents.Patent:
    patent_db = db.scalars(
        select(models.Patent).
        where(models.Patent.patent_number == patent_number)
    ).one_or_none()
    
    if patent_db is None:
        raise NotFound(f"Patent {patent_number} not found.")
    return patents.Patent.from_model(patent_db, assignees_needed=assignees_needed, inventors_needed=inventors_needed) 

@patents_router.post("/")
def add_patent(
    *,
    patent_scheme: patents.Patent,
    db: Session = Depends(get_db),
) -> patents.Patent:
    patent = models.Patent(patent_number=patent_scheme.patent_number, type=patent_scheme.type, pub_date=patent_scheme.pub_date, app_date=patent_scheme.app_date,
                           main_cpc=patent_scheme.main_cpc, title=patent_scheme.title, abstract=patent_scheme.abstract, claims=patent_scheme.claims)
    db.add(patent)

    if patent_scheme.assignees_list is not None:
        for assignee in patent_scheme.assignees_list:
            patent.assignees.append(models.Assignee(assignee_name=assignee.assignee_name, 
                                          assignee_type=assignee.assignee_type,
                                          country=assignee.country,
                                          city=assignee.city
                                          ))
    
    if patent_scheme.inventors_list is not None:
        pass

    db.flush()
    db.refresh(patent)

    return patents.Patent.from_model(patent)