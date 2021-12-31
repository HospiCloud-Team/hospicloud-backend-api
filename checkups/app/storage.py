from sqlalchemy.orm import Session
from typing import List
from common.schemas.checkup import CheckupIn
from common.models import Checkup
from common.utils import get_current_time


def get_checkup(db: Session, checkup_id: int) -> Checkup:
    return db.query(Checkup).filter(Checkup.id == checkup_id).first()


def get_checkups_by_patient(db: Session, patient_id: int) -> List[Checkup]:
    return db.query(Checkup).filter(Checkup.patient_id == patient_id).all()


def get_checkups_by_doctor(db: Session, doctor_id: int, patient_id: int = None) -> List[Checkup]:
    if patient_id:
        return db.query(Checkup).filter(Checkup.doctor_id == doctor_id, Checkup.patient_id == patient_id).all()

    return db.query(Checkup).filter(Checkup.doctor_id == doctor_id).all()


def create_checkup(db: Session, checkup: CheckupIn) -> Checkup:
    new_checkup = Checkup(**checkup.dict())
    new_checkup.date = get_current_time()

    db.add(new_checkup)

    db.commit()
    db.refresh(new_checkup)

    return new_checkup


def delete_checkup(db: Session, checkup_id: int) -> Checkup:
    checkup = db.query(Checkup).get(checkup_id)
    if not checkup:
        return None

    db.delete(checkup)
    db.commit()

    return checkup
