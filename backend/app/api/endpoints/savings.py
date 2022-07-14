from enum import Enum
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import IntegrityError
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session

from app.api import dependencies as deps
from app import crud, schemas

router = APIRouter()


class Quarter(str, Enum):
    First = "First"
    Second = "Second"
    Third = "Third"


@router.get("/", response_model=list[schemas.AllSavings])
async def get_all_savings(
    *,
    db: Session = Depends(deps.get_db),
    year: int | None = None,
    quarter: Quarter | None = None,
    current_quarter: bool = False,
) -> Any:
    return crud.saving.get_all_savings(db, year, quarter, current_quarter)


@router.get("/current-quarter-stats")
async def get_current_quarter_savings(*, db: Session = Depends(deps.get_db)) -> Any:
    return crud.saving.current_quarter(db)


@router.post("/", response_model=schemas.Saving)
def create_saving(
    *, db: Session = Depends(deps.get_db), saving_in: schemas.SavingCreate
) -> Any:
    """
    Create new saving.
    """

    member = crud.user.get(db, id=saving_in.member_id)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member whose saving is being added does not exist in the system",
        )

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
    saving_in: schemas.SavingUpdate,
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


@router.post("/bulk", response_model=list[schemas.Saving])
def bulk_insert(
    *, db: Session = Depends(deps.get_db), savings_in: list[schemas.SavingCreate]
) -> Any:
    """
    bulk create new savings
    Only used for historical data insert.
    """
    savings = []
    for saving_in in savings_in:
        member = crud.user.get(db, id=saving_in.member_id)
        if not member:
            raise HTTPException(
                status_code=404,
                detail=f"The member id: {saving_in.member_id} saving is being added does not exist in the system",
            )

        try:
            saving = crud.saving.create(db, obj_in=saving_in, is_late=False)
        except (IntegrityError, Exception) as err:
            if hasattr(err, "orig") and isinstance(err.orig, UniqueViolation):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": err.orig.args,
                        "detail": f"The user id: {saving_in.member_id} has a saving already created for this month",
                    },
                )
            raise HTTPException(
                status_code=400,
                detail=str(err),
            )
        savings.append(saving)
    return savings
