from common import models, database
from common.models import create_tables
from dependencies import get_db
import storage
from typing import List
from schemas.checkups import Checkup, CheckupIn
from fastapi import FastAPI, status, Depends
from starlette.responses import JSONResponse

app = FastAPI(title="Checkups", description="Checkups service for HospiCloud app.")

create_tables()


@app.get(
    "/checkups/doctor/{doctor_id}", response_model=List[Checkup], tags=["checkups"]
)
async def read_checkups_by_doctor(
    doctor_id: int, skip: int = 0, limit: int = 100, db_session=Depends(get_db)
):
    checkups = storage.get_checkups_by_doctor(db_session, doctor_id)
    return checkups


@app.get(
    "/checkups/doctor/{patient_id}", response_model=List[Checkup], tags=["checkups"]
)
async def read_checkups_by_doctor(
    patient_id: int, skip: int = 0, limit: int = 100, db_session=Depends(get_db)
):
    checkups = storage.get_checkups_by_patient(db_session, patient_id)
    return checkups


@app.post("/checkups", tags=["checkups"])
async def add_checkup(checkup: CheckupIn, db_session=Depends(get_db)):
    checkup_db = storage.create_checkup(db_session, checkup)
    return checkup_db
