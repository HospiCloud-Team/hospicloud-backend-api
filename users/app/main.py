import traceback
import os
from typing import List, Optional
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cloudauth.firebase import FirebaseClaims

import storage
from common.schemas.user import UserIn, User, UserRole, UserUpdate, DoctorOut
from common.schemas.auth import FirebaseUser
from dependencies import Session, get_db, get_current_user

app = FastAPI(title="Users", description="Users service for HospiCloud app.")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def register(user: UserIn, db: Session = Depends(get_db), test: bool = False):
    try:
        existing_user = storage.get_user_by_email(db, user.email)
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Email is already used"},
            )
        if user.user_role == UserRole.admin:
            return storage.create_admin(db, user, test)
        elif user.user_role == UserRole.patient:
            return storage.create_patient(db, user, test)
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
    current_user: FirebaseUser = Depends(get_current_user),
    test: bool = False,
):
    try:
        existing_user = storage.get_user_by_email(db, user.email)
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Email is already used"},
            )
        if current_user.user_role == UserRole.admin and user.user_role in [
            UserRole.admin,
            UserRole.doctor,
        ]:
            if (
                user.user_role == UserRole.doctor
                and user.doctor.hospital_id == current_user.hospital_id
            ):
                return storage.create_doctor(db, user, test)
            elif (
                user.user_role == UserRole.admin
                and user.admin.hospital_id == current_user.hospital_id
            ):
                return storage.create_admin(db, user, test)
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
    deprecated=True,
)
async def get_doctors_by_hospital_id(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user),
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
    current_user: FirebaseUser = Depends(get_current_user),
):
    if current_user.user_role == UserRole.admin:
        if user_role and user_role.value != UserRole.patient:
            return storage.get_users(db, user_role, current_user.hospital_id)
        else:
            return storage.get_users(db, hospital_id=current_user.hospital_id)
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
    current_user: FirebaseUser = Depends(get_current_user),
):
    db_user = storage.get_user(db, user_id)
    if db_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={
                "message": "User not found"}
        )
    elif current_user.user_role not in [UserRole.admin, UserRole.doctor]:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "User not admin or doctor."},
        )

    return db_user


@app.get(
    "/users/document-number/{document_number}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["users"]
)
async def get_user_with_document_number(
    document_number: str,
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user),
):
    db_user = storage.get_user(db, document_number=document_number)
    if db_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"}
        )
    elif current_user.user_role not in [UserRole.admin, UserRole.doctor]:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "User not admin or doctor."},
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
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: FirebaseUser = Depends(get_current_user),
):
    user = storage.get_user(db, user_id)

    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "User not found"},
        )

    current_hospital_id = None
    user_hospital_id = None

    if current_user.user_role != UserRole.patient:
        current_hospital_id = current_user.hospital_id

    if user.user_role != UserRole.patient:
        user_hospital_id = getattr(user, user.user_role).hospital_id

    try:
        if (
            current_user.user_role == UserRole.admin
            and current_hospital_id == user_hospital_id
        ) or (
            current_user.user_role == UserRole.patient and current_user.uid == user.uid
        ):
            db_user = storage.update_user(db, user_id, user_update)
            return db_user
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Operation not allowed."},
            )
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
    current_user: FirebaseUser = Depends(get_current_user),
    test: bool = False,
):
    user = storage.get_user(db, user_id)

    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "User not found"},
        )

    current_hospital_id = None
    user_hospital_id = None

    if current_user.user_role != UserRole.patient:
        current_hospital_id = current_user.hospital_id

    if user.user_role != UserRole.patient:
        user_hospital_id = getattr(user, user.user_role).hospital_id

    try:
        if (
            current_user.user_role == UserRole.admin
            and current_hospital_id == user_hospital_id
        ) or (
            current_user.user_role == UserRole.patient and current_user.uid == user.uid
        ):
            db_user = storage.delete_user(db, user_id, test)
            return db_user
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Operation not allowed."},
            )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"},
        )
