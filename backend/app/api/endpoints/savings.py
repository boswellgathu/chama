from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session

from app.api import dependencies as deps
from app import crud, schemas, models

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "hello savings!"}


@router.post("/", response_model=schemas.Saving)
def create_saving(
    *, db: Session = Depends(deps.get_db), saving_in: schemas.SavingCreate
) -> Any:
    """
    Create new saving.
    """
    try:
        saving = crud.saving.create(db, obj_in=saving_in)
    except (IntegrityError, Exception) as err:
        if isinstance(err.orig, UniqueViolation):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": err.orig.args,
                    "detail": "The user has a saving already created for this month",
                },
            )
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )
    return saving


@router.put("/{saving_id}", response_model=schemas.Saving)
def update_saving(
    *,
    db: Session = Depends(deps.get_db),
    saving_id: int,
    saving_in: schemas.SavingUpdate
) -> Any:
    """
    Update a saving.
    """

    saving = crud.saving.get(db, id=saving_id)
    if not saving:
        raise HTTPException(
            status_code=404,
            detail="The saving with this id does not exist in the system",
        )
    try:
        saving = crud.saving.update(db, db_obj=saving, obj_in=saving_in)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=str(err.args),
        )
    return saving