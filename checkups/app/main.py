import sqlalchemy
from common import models, database
from common.models import create_tables
from dependencies import get_db
import storage
from typing import List, Optional
from common.schemas.checkup import Checkup, CheckupIn
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Checkups",
              description="Checkups service for HospiCloud app.")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/checkups/doctor/{doctor_id}",
    status_code=status.HTTP_200_OK,
    tags=["checkups"],
)
async def read_checkups_by_doctor(doctor_id: int, patient_id: Optional[int] = None, db_session=Depends(get_db)):
    checkups = storage.get_checkups_by_doctor(db_session, doctor_id, patient_id)
    return checkups


@app.get(
    "/checkups/patient/{patient_id}",
    status_code=status.HTTP_200_OK,
    tags=["checkups"],
)
async def read_checkups_by_patient(patient_id: int, doctor_id: Optional[int] = None, db_session=Depends(get_db)):
    checkups = storage.get_checkups_by_patient(db_session, patient_id, doctor_id)
    return checkups


@app.post(
    "/checkups/",
    response_model=Checkup,
    status_code=status.HTTP_201_CREATED,
    tags=["checkups"],
)
async def add_checkup(checkup: CheckupIn, db_session=Depends(get_db)):
    try:
        checkup_db = storage.create_checkup(db_session, checkup)
        return checkup_db
    except sqlalchemy.exc.IntegrityError as err:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"There has been an error inserting data. {err}"},
        )
