import copy
from datetime import date
from typing import Any, Dict, Union
from time import strptime
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.crud_fine import fine as fine_class
from app.models import Saving, Fine
from app.schemas.saving import SavingCreate, SavingUpdate, Month
from app.schemas.fine import FineCreate, FineReason


class CRUDSaving(CRUDBase[Saving, SavingCreate, SavingUpdate]):
    def get_by_id(self, db: Session, *, id: int) -> None | Saving:
        return db.query(Saving).filter(Saving.id == id).first()

    def create(self, db: Session, *, obj_in: SavingCreate) -> Saving:
        is_saving_late: bool = self.is_saving_late(obj_in.date_sent, obj_in.month)
        db_obj = Saving(
            date_sent=obj_in.date_sent,
            month=obj_in.month,
            year=obj_in.year,
            amount=obj_in.amount,
            is_late=is_saving_late,
            member_id=obj_in.member_id,
            fine_id=obj_in.fine_id,
        )
        db.add(db_obj)

        # update saving with fine_id if it was a late saving
        if is_saving_late:
            fine_obj = self.create_fine(db, obj_in.member_id)
            db_obj.fine_id = fine_obj.id

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Saving,
        obj_in: Union[SavingUpdate, Dict[str, Any]],
    ) -> Saving:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        self.update_saving_and_related_fine_record(
            db, update_data=update_data, db_obj=db_obj
        )
        db.refresh(db_obj)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_saving_late(self, date_sent: date, saving_month: Month) -> bool:
        if date_sent.month > strptime(saving_month, "%B").tm_mon:
            return True
        elif date_sent.day > 5:
            return True
        return False

    def create_fine(self, db: Session, member_id: int) -> Fine:
        fine_data = FineCreate(
            amount=50, reason=FineReason.SavingsFine, member_id=member_id
        )
        fine = fine_class.create(db, obj_in=fine_data)
        return fine

    def update_saving_and_related_fine_record(
        self,
        db: Session,
        update_data: Union[SavingUpdate, Dict[str, Any]],
        db_obj: Saving,
    ):
        date_sent_ = update_data.get("date_sent")
        month_ = update_data.get("month")
        if date_sent_ or month_:
            date_sent, month = (
                (date_sent_, db_obj.month)
                if date_sent_ and (not month_)
                else (db_obj.date_sent, month_)
            )

            is_saving_late: bool = self.is_saving_late(date_sent, month)

            if is_saving_late != db_obj.is_late:
                if is_saving_late and not db_obj.is_late:
                    # is_saving_late = True and is_late = False
                    # add a fine record
                    fine_obj = self.create_fine(db, update_data["member_id"])
                    update_data["fine_id"] = fine_obj.id
                    update_data["is_late"] = True
                elif db_obj.is_late and not is_saving_late:
                    # is_saving_late = False and is_late = True
                    # delete associated fine record
                    fine_record = fine_class.get_by_id(db, id=db_obj.fine_id)
                    db.delete(fine_record)
                    db.commit()

                    update_data["fine_id"] = None
                    update_data["is_late"] = False
        return update_data


saving = CRUDSaving(Saving)
