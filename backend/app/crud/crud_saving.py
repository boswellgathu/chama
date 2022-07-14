from datetime import date
from typing import Any, Dict, Union
from time import strptime

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy.sql.elements import literal_column

from app.crud.base import CRUDBase
from app.crud.crud_fine import fine as fine_class
from app.models import Saving, Fine, User
from app.schemas.saving import SavingCreate, SavingUpdate, Month
from app.schemas.fine import FineCreate, FineReason


class CRUDSaving(CRUDBase[Saving, SavingCreate, SavingUpdate]):
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
                    fine_record = fine_class.get(db, id=db_obj.fine_id)
                    db.delete(fine_record)
                    db.commit()

                    update_data["fine_id"] = None
                    update_data["is_late"] = False
        return update_data

    def current_quarter(self, db: Session):
        month_quarters = {
            "JANUARY": ["JANUARY", "FEBRUARY", "MARCH"],
            "FEBRUARY": ["JANUARY", "FEBRUARY", "MARCH"],
            "MARCH": ["JANUARY", "FEBRUARY", "MARCH"],
            "APRIL": ["JANUARY", "FEBRUARY", "MARCH"],
            "MAY": ["MAY", "JUNE", "JULY"],
            "JUNE": ["MAY", "JUNE", "JULY"],
            "JULY": ["MAY", "JUNE", "JULY"],
            "AUGUST": ["MAY", "JUNE", "JULY"],
            "SEPTEMBER": ["SEPTEMBER", "OCTOBER", "NOVEMBER"],
            "OCTOBER": ["SEPTEMBER", "OCTOBER", "NOVEMBER"],
            "NOVEMBER": ["SEPTEMBER", "OCTOBER", "NOVEMBER"],
            "DECEMBER": ["SEPTEMBER", "OCTOBER", "NOVEMBER"],
        }
        today = date.today()
        year = today.year
        month = today.strftime("%B").upper()

        current_quarter = month_quarters[month]
        s_query = (
            select(
                User.name,
                User.id,
                func.string_agg(Saving.month, literal_column("','")).label("months"),
            )
            .join(User, User.id == Saving.member_id)
            .where(Saving.year == year)
            .where(Saving.month.in_(current_quarter))
            .group_by(User.name, User.id)
        ).subquery()

        query = select(User.name, s_query.c.months).outerjoin(
            s_query, s_query.c.id == User.id
        )

        db_data = db.execute(query).all()
        return {
            user_savings.name: self.process_user_quarter(
                current_quarter, user_savings.months
            )
            for user_savings in db_data
        }

    @staticmethod
    def process_user_quarter(current_quarter_months, user_savings_months):
        user_months = []
        if user_savings_months:
            user_months = user_savings_months.split(",")
        return {month: month in user_months for month in current_quarter_months}


saving = CRUDSaving(Saving)
