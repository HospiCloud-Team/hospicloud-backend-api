from os import stat
import traceback
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from common.schemas.specialty import Specialty, SpecialtyIn
from storage import specialty as specialties
from dependencies import get_db, Session

router = APIRouter()


@router.post(
    "/specialties",
    response_model=Specialty,
    status_code=status.HTTP_201_CREATED,
    tags=["specialties"]
)
async def create_specialty(specialty: SpecialtyIn, db: Session = Depends(get_db)):
    try:
        existing_specialty = specialties.get_specialty_by_name(
            db, specialty.name, specialty.hospital_id)
        if existing_specialty:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Specialty exists in the current hospital"}
            )

        return specialties.create_specialty(db, specialty)
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Specialty name is empty"}
        )
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


@router.get(
    "/specialties/{specialty_id}",
    response_model=Specialty,
    status_code=status.HTTP_200_OK,
    tags=["specialties"]
)
async def get_specialty(specialty_id: int, db: Session = Depends(get_db)):
    db_specialty = specialties.get_specialty_by_id(db, specialty_id)
    if db_specialty is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Specialty not found"}
        )

    return db_specialty


@router.delete(
    "/specialties/{specialty_id}",
    response_model=Specialty,
    status_code=status.HTTP_200_OK,
    tags=["specialties"]
)
async def delete_specialty(specialty_id: int, db: Session = Depends(get_db)):
    try:
        db_specialty = specialties.delete_specialty(db, specialty_id)
        if db_specialty is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Specialty not found"}
            )

        return db_specialty
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )
