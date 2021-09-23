import traceback
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

import storage
from schemas.patient import PatientIn, Patient
from dependencies import get_db, Session, create_tables

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

create_tables()


@router.post("/patients", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_user(patient: PatientIn, db: Session = Depends(get_db)):
    try:
        existing_patient = storage.get_patient_by_email(db, patient.user.email)
        if existing_patient:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": f'User with email {patient.user.email} already exists'}
            )

        return storage.create_patient(db, patient)
    except Exception:
        print(traceback.format_exc())

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@router.get("/patients", response_model=List[Patient], status_code=status.HTTP_200_OK)
def get_patients(db: Session = Depends(get_db)):
    return storage.get_patients(db)


@router.get("/patients/{patient_id}", response_model=Patient, status_code=status.HTTP_200_OK)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = storage.get_patient(db, patient_id)
    if db_patient is None:
        return JSONResponse(
            status_code=404,
            content={"message": "User not found"}
        )

    return db_patient


@router.delete("/patients/{patient_id}", response_model=Patient, status_code=status.HTTP_200_OK)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    try:
        db_patient = storage.delete_patient(db, patient_id)
        if db_patient is None:
            return JSONResponse(
                status_code=404,
                content={"message": "User not found"}
            )

        return db_patient
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )
