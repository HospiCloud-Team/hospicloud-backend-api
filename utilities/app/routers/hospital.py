from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from common.schemas.hospital import Hospital, HospitalIn, HospitalUpdate
from dependencies import get_db, Session
from storage import hospital as hospitals

router = APIRouter()


@router.post(
    "/hospitals",
    response_model=Hospital,
    status_code=status.HTTP_201_CREATED,
    tags=["hospitals"]
)
async def create_hospital(hospital: HospitalIn, db: Session = Depends(get_db)):
    try:
        existing_hospital = hospitals.get_hospital_by_name(db, hospital.name)
        if existing_hospital:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Hospital already exists"}
            )

        return hospitals.create_hospital(db, hospital)
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid province"}
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@router.get(
    "/hospitals/{hospital_id}",
    response_model=Hospital,
    status_code=status.HTTP_200_OK,
    tags=["hospitals"]
)
async def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    db_hospital = hospitals.get_hospital_by_id(db, hospital_id)
    if db_hospital is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Hospital not found"}
        )

    return db_hospital


@router.get(
    "/hospitals",
    response_model=List[Hospital],
    status_code=status.HTTP_200_OK,
    tags=["hospitals"]
)
async def get_hospitals(db: Session = Depends(get_db)):
    return hospitals.get_hospitals(db)


@router.put(
    "/hospitals/{hospital_id}",
    response_model=Hospital,
    status_code=status.HTTP_200_OK,
    tags=["hospitals"]
)
async def update_hospital(hospital_id: int, updated_hospital: HospitalUpdate, db: Session = Depends(get_db)):
    try:
        db_hospital = hospitals.update_hospital(
            db, hospital_id, updated_hospital)
        if db_hospital is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Hospital not found"}
            )
        
        return db_hospital
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@router.delete(
    "/hospitals/{hospital_id}",
    response_model=Hospital,
    status_code=status.HTTP_200_OK,
    tags=["hospitals"]
)
async def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    try:
        db_hospital = hospitals.delete_hospital(db, hospital_id)
        if db_hospital is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Hospital not found"}
            )

        return db_hospital
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )
