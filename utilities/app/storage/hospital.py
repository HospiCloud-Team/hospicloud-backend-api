import traceback
from common.schemas.hospital import Hospital, HospitalIn
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
        db_hospital = Hospital(**hospital.dict(exclude={"location"}), location=db_location)

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
