import bcrypt
import traceback
from typing import List
from dependencies import Session
from common.schemas.user import User, UserIn, UserRole, UserUpdate
from common.models import Base, Patient, User, Admin, Doctor, Specialty
from utils import generate_password
from common.utils import get_current_time

ALLOWED_USER_UPDATES = ["name", "last_name",
                        "date_of_birth", "document_number"]

ALLOWED_PATIENT_UPDATES = ["medical_background"]

ALLOWED_DOCTOR_UPDATES = ["schedule", "specialties"]


def create_patient(db: Session, user: UserIn) -> User:
    random_password = generate_password().encode("utf-8")
    hashed_password = bcrypt.hashpw(random_password, bcrypt.gensalt())

    try:
        db_user = User(
            **user.dict(exclude={"patient"}), password=hashed_password
        )

        db_user.created_at = get_current_time()

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


def create_admin(db: Session, user: UserIn) -> User:
    random_password = generate_password().encode("utf-8")
    hashed_password = bcrypt.hashpw(random_password, bcrypt.gensalt())

    try:
        db_user = User(
            **user.dict(exclude={"admin"}), password=hashed_password
        )

        db_user.created_at = get_current_time()

        db_admin = Admin(**user.admin.dict(), user=db_user)

        db.add(db_user)
        db.add(db_admin)

        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def create_doctor(db: Session, user: UserIn) -> User:
    random_password = generate_password().encode("utf-8")
    hashed_password = bcrypt.hashpw(random_password, bcrypt.gensalt())

    try:
        db_user = User(
            **user.dict(exclude={"doctor"}), password=hashed_password
        )

        db_user.created_at = get_current_time()

        db_doctor = Doctor(
            **user.doctor.dict(exclude={"specialties"}), user=db_user)

        specialties = db.query(Specialty).filter(
            Specialty.id.in_(user.doctor.specialties)).all()

        db_doctor.specialties = specialties

        db.add(db_user)
        db.add(db_doctor)

        db.commit()
        db.refresh(db_doctor)

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, user_role: UserRole) -> List[User]:
    if user_role:
        return db.query(User).filter(User.user_role == user_role.value).all()

    return db.query(User).all()


def get_user_by_email(db: Session, email: str) -> User:
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def delete_user(db: Session, user_id: int) -> User:
    user = get_user(db, user_id)
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


def update_user(db: Session, user_id: int, updated_user: UserUpdate) -> User:
    user = get_user(db, user_id)
    if not user:
        return None

    try:
        for key, value in dict(updated_user).items():
            if do_key_and_value_exist(key, value) and key in ALLOWED_USER_UPDATES:
                setattr(user, key, value)

        is_patient_user = updated_user.patient is not None and user.user_role == UserRole.patient
        is_doctor_user = updated_user.doctor is not None and user.user_role == UserRole.doctor

        if is_patient_user:
            for key, value in dict(updated_user.patient).items():
                if do_key_and_value_exist(key, value) and key in ALLOWED_PATIENT_UPDATES:
                    setattr(user.patient, key, value)
        elif is_doctor_user:
            for key, value in dict(updated_user.doctor).items():
                if do_key_and_value_exist(key, value) and key in ALLOWED_DOCTOR_UPDATES:
                    if key == "specialties":
                        value = db.query(Specialty).filter(
                            Specialty.id.in_(updated_user.doctor.specialties)).all()

                    setattr(user.doctor, key, value)

        user.updated_at = get_current_time()

        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def do_key_and_value_exist(key, value) -> bool:
    return key is not None and value is not None


def get_doctors_by_hospital_id(db: Session, hospital_id: int) -> List[User]:
    return db.query(User).join(Doctor).filter(Doctor.hospital_id == hospital_id).all()
