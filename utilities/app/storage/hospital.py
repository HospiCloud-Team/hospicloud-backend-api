import traceback
import datetime
from typing import List
from common.schemas.hospital import Hospital, HospitalIn, HospitalUpdate
from common.schemas.location import Province
from common.models import Hospital, Location
from dependencies import Session


def is_province_valid(province: str) -> bool:
    try:
        Province(province)
    except ValueError:
        return False

    return True


def create_hospital(db: Session, hospital: HospitalIn) -> Hospital:
    try:
        if not is_province_valid(hospital.location.province):
            raise ValueError("Invalid province")

        db_location = Location(**hospital.location.dict())
        db_hospital = Hospital(
            **hospital.dict(exclude={"location"}), location=db_location)

        db.add(db_location)
        db.add(db_hospital)

        db.commit()
        db.refresh(db_hospital)

        return db_hospital
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def get_hospital_by_name(db: Session, hospital_name: str) -> Hospital:
    return db.query(Hospital).filter(Hospital.name == hospital_name).first()


def get_hospital_by_id(db: Session, hospital_id: int) -> Hospital:
    return db.query(Hospital).filter(Hospital.id == hospital_id).first()


def get_hospitals(db: Session) -> List[Hospital]:
    return db.query(Hospital).all()


def update_hospital(db: Session, hospital_id: int, updated_hospital: HospitalUpdate) -> Hospital:
    hospital = get_hospital_by_id(db, hospital_id)
    if not hospital:
        return None

    try:
        if updated_hospital.name:
            hospital.name = updated_hospital.name

        if updated_hospital.schedule:
            hospital.schedule = updated_hospital.schedule

        if updated_hospital.location:
            if updated_hospital.location.address:
                hospital.location.address = updated_hospital.location.address

            if updated_hospital.location.province:
                if not is_province_valid(updated_hospital.location.province):
                    raise ValueError("Invalid province")

                hospital.location.province = updated_hospital.location.province

        hospital.updated_at = datetime.datetime.now()

        db.commit()
        db.refresh(hospital)

        return hospital
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def delete_hospital(db: Session, hospital_id: int) -> Hospital:
    hospital = get_hospital_by_id(db, hospital_id)
    if not hospital:
        return None

    try:
        db.delete(hospital)
        db.commit()
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')

    return hospital
