from fastapi import APIRouter, Depends, HTTPException

import storage
from schemas.patient import PatientIn, Patient
from dependencies import get_db, Session, create_tables

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

create_tables()


@router.post("/patients/", response_model=Patient)
def create_user(patient: PatientIn, db: Session = Depends(get_db)):
    return storage.create_patient(db, patient)


@router.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = storage.get_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_patient


@router.delete("/patients/{patient_id}", response_model=Patient)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = storage.delete_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_patient
