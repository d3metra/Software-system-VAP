from app import models
from app.schemas import patents_families
from app.dependencies.db import get_db
from app.errors import responses, NotFound

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

patents_families_router = APIRouter()

@patents_families_router.get("/{app_number}", responses=responses)
def get_patents_family(
    *,
    db: Session = Depends(get_db),
    app_number: str,
    assignees_needed: bool = False,
    inventors_needed: bool = False,
    descriptions_needed: bool = False,
    ipc_needed: bool = False,
    cpc_needed: bool = False
) -> patents_families.PatentsFamily:
    patents_family_db = db.scalars(
        select(models.PatentsFamily).
        where(models.PatentsFamily.app_number == app_number)
    ).one_or_none()

    if patents_family_db is None:
        raise NotFound(f"Patents Family {app_number} not found.")
    
    return patents_families.PatentsFamily.from_model(patents_family_db,
                                                     assignees_needed=assignees_needed,
                                                     inventors_needed=inventors_needed,
                                                     descriptions_needed=descriptions_needed,
                                                     ipc_needed=ipc_needed,
                                                     cpc_needed=cpc_needed)