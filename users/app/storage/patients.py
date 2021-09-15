import bcrypt

from users.app.dependencies import Session
from users.app.schemas.patient import PatientIn
from common.models import Patient, User


def get_patient(db: Session, patient_id: int) -> Patient:
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patient_by_email(db: Session, email: str) -> Patient:
    return db.query(Patient).filter(Patient.user.email == email).first()


def create_patient(db: Session, patient: PatientIn) -> Patient:
    encoded_password = patient.user.password.encode("utf-8")
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    patient.user.password = hashed_password

    new_patient: Patient = Patient(**patient.dict())

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


def delete_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).get(patient_id)
    if not patient:
        return None

    db.delete(patient)
    db.commit()

    return patient
