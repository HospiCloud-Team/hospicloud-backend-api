import traceback
import os
from typing import List, Optional
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cloudauth.firebase import FirebaseCurrentUser, FirebaseClaims

import storage
from common.schemas.user import UserIn, User, UserRole, UserUpdate, DoctorOut
from .tests.test_class import TokenBearer
from dependencies import get_db, Session

app = FastAPI(title="Users", description="Users service for HospiCloud app.")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("ENVIRONMENT") == "TEST":
    get_current_user = TokenBearer()
else:
    get_current_user = FirebaseCurrentUser(project_id=os.getenv("PROJECT_ID"))


@app.get("/")
async def home():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"container": "users", "message": "Hello World!"},
    )


@app.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    tags=["users"],
)
async def register(
    user: UserIn,
    db: Session = Depends(get_db),
):
    try:
        existing_user = storage.get_user_by_email(db, user.email)
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Email is already used"},
            )
        if user.user_role == UserRole.admin:
            return storage.create_admin(db, user)
        elif user.user_role == UserRole.patient:
            return storage.create_patient(db, user)
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Can only register admin or patient."},
            )
    except Exception:
        print(traceback.format_exc())

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"},
        )


@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    tags=["users"],
)
async def create_user(
    user: UserIn,
    db: Session = Depends(get_db),
    current_user: FirebaseClaims = Depends(get_current_user),
):
    try:
        current_user: User = storage.get_user_by_email(current_user.email)
        existing_user = storage.get_user_by_email(db, user.email)
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Email is already used"},
            )
        if current_user["role"] == UserRole.admin and user.user_role in [
            UserRole.admin,
            UserRole.doctor,
        ]:
            if (
                user.user_role == UserRole.doctor
                and user.doctor.hospital_id == current_user.doctor.hospital_id
            ):
                return storage.create_doctor(db, user)
            elif (
                user.user_role == UserRole.admin
                and user.doctor.hospital_id == current_user.admin.hospital_id
            ):
                return storage.create_admin(db, user)
            else:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "User can't add to this hospital."},
                )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "User is not an admin."},
            )

    except Exception:
        print(traceback.format_exc())

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"},
        )


@app.get(
    "/users/doctors",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["users"],
)
async def get_doctors_by_hospital_id(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: FirebaseClaims = Depends(get_current_user),
):
    return storage.get_doctors_by_hospital_id(db, hospital_id)


@app.get(
    "/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["users"],
)
async def get_users(
    db: Session = Depends(get_db),
    user_role: Optional[UserRole] = None,
    current_user: FirebaseClaims = Depends(get_current_user),
):
    current_user: User = storage.get_user_by_email(db, current_user.email)
    current_hospital_id = getattr(current_user, current_user.user_role).hospital_id
    if current_user.user_role == UserRole.admin:
        if user_role and user_role.value != UserRole.patient:
            return storage.get_users(db, user_role, current_hospital_id)
        else:
            return storage.get_users(db, hospital_id=current_hospital_id)
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "User is not an admin."},
        )


@app.get(
    "/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["users"],
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: FirebaseClaims = Depends(get_current_user),
):
    db_user = storage.get_user(db, user_id)
    if db_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"}
        )

    return db_user


@app.put(
    "/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["users"],
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: FirebaseClaims = Depends(get_current_user),
):
    try:
        db_user = storage.update_user(db, user_id, user)
        if db_user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found"},
            )

        return db_user
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"},
        )


@app.delete(
    "/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["users"],
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: FirebaseClaims = Depends(get_current_user),
):
    current_user: User = storage.get_user_by_email(current_user.email)
    user = storage.get_user(db, user_id)
    current_hospital_id, user_hospital_id = None

    if current_user.user_role != UserRole.patient:
        current_hospital_id = getattr(current_user, current_user.user_role).hospital_id

    if user.user_role != UserRole.patient:
        user_hospital_id = getattr(current_user, current_user.user_role).hospital_id

    try:
        if (
            current_user.user_role == UserRole.admin
            and current_hospital_id == user_hospital_id
        ) or (
            current_user.user_role == UserRole.patient and current_user.id == user.id
        ):
            db_user = storage.delete_user(db, user_id)
            if db_user is None:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"message": "User not found"},
                )
            return db_user
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"},
        )
