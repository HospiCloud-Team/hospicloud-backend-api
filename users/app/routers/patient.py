from fastapi import APIRouter, Depends, HTTPException

from users.app.dependencies import get_db, Session
from users.app.schemas.patient import PatientIn, Patient
from users.app.storage import patients

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/patients/", response_model=Patient)
def create_user(patient: PatientIn, db: Session = Depends(get_db)):
    db_patient = patients.get_patient_by_email(db, patient.user.email)
    if db_patient:
        raise HTTPException(status_code=400, detail="Patiend already exists")

    return patients.create_patient(db, patient)


@router.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = patients.get_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_patient


@router.delete("/patients/{patient_id}", response_model=Patient)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = patients.delete_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_patient
