import traceback
from typing import List, Optional

from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse

import storage
from schemas.user import UserIn, User, UserRole
from dependencies import get_db, Session, create_tables

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

create_tables()


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    try:
        existing_user = storage.get_user_by_email(db, user.email)
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": f'User with email {user.email} already exists'}
            )

        return storage.create_patient(db, user)
    except Exception:
        print(traceback.format_exc())

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db), user_role: Optional[UserRole] = None):
    return storage.get_users(db, user_role)


@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = storage.get_user(db, user_id)
    if db_user is None:
        return JSONResponse(
            status_code=404,
            content={"message": "User not found"}
        )

    return db_user


@app.delete("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = storage.delete_user(db, user_id)
        if db_user is None:
            return JSONResponse(
                status_code=404,
                content={"message": "User not found"}
            )

        return db_user
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )
