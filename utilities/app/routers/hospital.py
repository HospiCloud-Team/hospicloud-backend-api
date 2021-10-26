from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from common.schemas.hospital import Hospital, HospitalIn
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
