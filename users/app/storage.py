import bcrypt
import traceback
from typing import List

from dependencies import Session
from schemas.user import User, UserIn, UserRole
from common.models import Patient, BaseUser
from utils import generate_password


def create_patient(db: Session, user: UserIn) -> User:
    random_password = generate_password().encode("utf-8")
    hashed_password = bcrypt.hashpw(random_password, bcrypt.gensalt())

    try:
        db_user = BaseUser(**user.dict(exclude={"patient"}), password=hashed_password)
        db_patient = Patient(**user.patient.dict(), user=db_user)

        db.add(db_user)
        db.add(db_patient)

        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def get_user(db: Session, user_id: int) -> User:
    return db.query(BaseUser).filter(BaseUser.id == user_id).first()


def get_users(db: Session, user_role: UserRole) -> List[User]:
    if user_role:
        return db.query(BaseUser).filter(BaseUser.user_role == user_role.value).all()

    return db.query(BaseUser).all()


def get_user_by_email(db: Session, email: str) -> User:
    try:
        return db.query(BaseUser).filter(BaseUser.email == email).first()
    except Exception as e:
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def delete_user(db: Session, user_id: int) -> User:
    user = db.get(BaseUser, user_id)
    if not user:
        return None

    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')

    return user
