import traceback
from typing import List, Optional

from sqlalchemy.sql.elements import and_

from common.schemas.specialty import Specialty, SpecialtyIn, SpecialtyUpdate
from common.models import Specialty, Hospital
from dependencies import Session


def create_specialty(db: Session, specialty: SpecialtyIn) -> Specialty:
    if not specialty.name:
        raise ValueError("Specialty name is empty")

    try:
        db_specialty = Specialty(
            name=specialty.name.strip(),
            hospital_id=specialty.hospital_id
        )

        db.add(db_specialty)

        db.commit()
        db.refresh(db_specialty)

        return db_specialty
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def get_specialties(db: Session, hospital_id: int) -> List[Specialty]:
    return db.query(Specialty).filter(Specialty.hospital_id == hospital_id).all()


def get_specialty_by_name(db: Session, specialty_name: str, hospital_id: int) -> Specialty:
    return db.query(Specialty).filter(
        Specialty.name == specialty_name,
        Specialty.hospital_id == hospital_id
    ).first()


def get_specialty_by_id(db: Session, specialty_id: int) -> Specialty:
    return db.query(Specialty).filter(Specialty.id == specialty_id).first()


def update_specialty(db: Session, updated_specialty: SpecialtyUpdate, specialty_id: int) -> Specialty:
    specialty = get_specialty_by_id(db, specialty_id)
    if not specialty:
        return None

    try:
        if updated_specialty.name.strip():
            specialty.name = updated_specialty.name.strip()

        db.commit()
        db.refresh(specialty)

        return specialty
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def delete_specialty(db: Session, specialty_id: int) -> Specialty:
    specialty = get_specialty_by_id(db, specialty_id)
    if not specialty:
        return None

    try:
        db.delete(specialty)
        db.commit()
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')

    return specialty
