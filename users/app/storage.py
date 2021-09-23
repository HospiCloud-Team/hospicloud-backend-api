import bcrypt
import traceback

from dependencies import Session
from schemas.patient import PatientIn
from common.models import Patient, BaseUser


def get_patient(db: Session, patient_id: int) -> Patient:
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patients(db: Session) -> Patient:
    return db.query(Patient).all()


def get_patient_by_email(db: Session, email: str) -> Patient:
    try:
        return db.query(BaseUser).filter(BaseUser.email == email).first()
    except Exception as e:
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def create_patient(db: Session, patient: PatientIn) -> Patient:
    encoded_password = patient.user.password.encode("utf-8")
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    patient.user.password = hashed_password

    try:
        db_user = BaseUser(**patient.user.dict())
        db_patient = Patient(
            user=db_user,
            blood_type=patient.blood_type.value,
            medical_background=patient.medical_background
        )

        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

        return db_patient
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def delete_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).get(patient_id)
    if not patient:
        return None

    try:
        db.delete(patient)
        db.commit()
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')

    return patient
