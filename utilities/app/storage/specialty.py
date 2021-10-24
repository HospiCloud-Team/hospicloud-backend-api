import traceback
from typing import List

from common.schemas.specialty import Specialty, SpecialtyIn
from common.models import Specialty, Hospital, hospital_to_specialty_association
from dependencies import Session


def create_specialty(db: Session, specialty: SpecialtyIn) -> Specialty:
    if not specialty.name:
        raise ValueError("Specialty name is empty")

    try:
        db_specialty = Specialty(**specialty.dict())

        db.add(db_specialty)

        db.commit()
        db.refresh(db_specialty)

        return db_specialty
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def get_specialties(db: Session, hospital_id: int) -> List[Specialty]:
    if hospital_id:
        return db.query(Specialty).join(hospital_to_specialty_association).filter(hospital_to_specialty_association.c.hospital_id == hospital_id).all()

    return db.query(Specialty).all()


def get_specialty(db: Session, specialty_id: int) -> Specialty:
    return db.query(Specialty).filter(Specialty.id == specialty_id).first()


def delete_specialty(db: Session, specialty_id: int) -> Specialty:
    specialty = get_specialty(db, specialty_id)
    if specialty:
        return None

    try:
        db.delete(specialty)
        db.commit()
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')

    return specialty


def update_specialty(db: Session, updated_specialty: SpecialtyIn, specialty_id: int) -> Specialty:
    specialty = get_specialty(db, specialty_id)
    if specialty:
        return None

    try:
        if updated_specialty.name:
            raise ValueError("missing specialty name")

        specialty.name = updated_specialty.name

        db.commit()
        db.refresh(specialty)

        return specialty
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')
