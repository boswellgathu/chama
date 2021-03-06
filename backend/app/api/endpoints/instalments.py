from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from psycopg2 import IntegrityError
from psycopg2.errors import UniqueViolation


from app.api import dependencies as deps
from app.schemas.instalment import InstalmentCreate, InstalmentUpdate
from app import crud, schemas

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "hello instalments!"}


@router.post("/", response_model=schemas.Instalment)
def create_instalment(
    *, db: Session = Depends(deps.get_db), instalment_in: InstalmentCreate
) -> Any:
    """
    Create new instalment.
    """
    loan = crud.loan.get(db, id=instalment_in.loan_id)
    if not loan:
        raise HTTPException(
            status_code=404,
            detail="The loan whose instalment is being added does not exist in the system",
        )

    try:
        instalment = crud.instalment.create(db, obj_in=instalment_in, loan_db_obj=loan)
        return instalment
    except (IntegrityError, Exception) as err:
        if isinstance(err.orig, UniqueViolation):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": err.orig.args,
                    "detail": "The user has an instalment already created for this month",
                },
            )
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )


@router.put("/{instalment_id}", response_model=schemas.Instalment)
def update_instalment(
    *,
    db: Session = Depends(deps.get_db),
    instalment_id: int,
    instalment_in: InstalmentUpdate
) -> Any:
    """
    Update an instalment.
    """
    instalment = crud.instalment.get(db, id=instalment_id)
    if not instalment:
        raise HTTPException(
            status_code=404,
            detail="The instalment with this ID does not exist in the system",
        )
    instalment = crud.instalment.update(db, db_obj=instalment, obj_in=instalment_in)
    return instalment
