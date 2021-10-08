import traceback
from typing import List, Optional

from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse

import storage
from schemas.user import UserIn, User, UserRole, UserUpdate
from dependencies import get_db, Session

app = FastAPI(
    title="Users",
    description="Users service for HospiCloud app."
)


@app.get("/")
async def home():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={
            "container": "users", "message": "Hello World!"}
    )


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    try:
        existing_user = storage.get_user_by_email(db, user.email)
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": f'User with email {user.email} already exists'}
            )

        if user.user_role == UserRole.patient:
            return storage.create_patient(db, user)
        elif user.user_role == UserRole.admin:
            return storage.create_admin(db, user)
        else:
            return storage.create_doctor(db, user)

    except Exception:
        print(traceback.format_exc())

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK, response_model_exclude_none=True)
def get_users(db: Session = Depends(get_db), user_role: Optional[UserRole] = None):
    return storage.get_users(db, user_role)


@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, response_model_exclude_none=True)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = storage.get_user(db, user_id)
    if db_user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"}
        )

    return db_user


@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, response_model_exclude_none=True)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        db_user = storage.update_user(db, user_id, user)
        if db_user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found"}
            )

        return db_user
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@app.delete("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, response_model_exclude_none=True)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = storage.delete_user(db, user_id)
        if db_user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found"}
            )

        return db_user
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )
