from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import List
from common.schemas.checkup import CheckupIn
from common.models import Checkup, User
from common.utils import get_current_time


def get_checkup(db: Session, checkup_id: int) -> Checkup:
    return db.query(Checkup).filter(Checkup.id == checkup_id).first()


def get_checkups_by_patient(db: Session, patient_id: int) -> List[Checkup]:
    return db.query(Checkup).filter(Checkup.patient_id == patient_id).all()


def get_checkups_by_doctor(db: Session, doctor_id: int) -> List[Checkup]:
    return db.query(Checkup).filter(Checkup.doctor_id == doctor_id).all()


def create_checkup(db: Session, checkup: CheckupIn) -> Checkup:
    if checkup.document_number:
        patient_id = validate_user_with_document_number(db, checkup.document_number)
        
        checkup.patient_id = patient_id

    new_checkup = Checkup(**checkup.dict(exclude={"document_number"}))
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


def validate_user_with_document_number(db: Session, document_number: int):
    user = db.query(User).filter(User.document_number == document_number).first()
    if not user:
        raise NoResultFound

    return user.patient.id
