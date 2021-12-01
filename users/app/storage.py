import bcrypt
import datetime
import traceback
from typing import List

from firebase_admin import initialize_app
from firebase_admin.auth import UserInfo, create_user, set_custom_user_claims

from dependencies import Session
from common.schemas.user import User, UserIn, UserRole, UserUpdate
from common.models import Base, Patient, User, Admin, Doctor, Specialty
from utils import generate_password
from common.utils import get_current_time

ALLOWED_USER_UPDATES = ["name", "last_name", "date_of_birth", "document_number"]

ALLOWED_PATIENT_UPDATES = ["medical_background"]

ALLOWED_DOCTOR_UPDATES = ["schedule", "specialty_ids"]

firebase_app = initialize_app()


def create_patient(db: Session, user: UserIn, is_test: bool = False) -> User:
    random_password = generate_password()
    hashed_password = bcrypt.hashpw(random_password.encode("utf-8"), bcrypt.gensalt())

    try:
        db_user = User(**user.dict(exclude={"patient"}), password=hashed_password)
        db_user.created_at = get_current_time()
        db_patient = Patient(**user.patient.dict(), user=db_user)

        db.add(db_user)
        db.add(db_patient)

        if not is_test:
            firebase_patient: UserInfo = create_user(
                email=user.email,
                password=random_password,
                display_name=f"{user.name} {user.last_name}",
            )

            set_custom_user_claims(
                firebase_patient.uid,
                {"id": db_user.id, "role": UserRole.patient, "hospital_id": None},
            )
            db_user.uid = firebase_patient.uid

        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f"Unexpected error: {e}")


def create_admin(db: Session, user: UserIn, is_test: bool = False) -> User:
    random_password = generate_password()
    hashed_password = bcrypt.hashpw(random_password.encode("utf-8"), bcrypt.gensalt())

    try:
        db_user = User(**user.dict(exclude={"admin"}), password=hashed_password)
        db_user.created_at = get_current_time()

        db_admin = Admin(**user.admin.dict(), user=db_user)

        db.add(db_user)
        db.add(db_admin)

        if not is_test:
            firebase_admin: UserInfo = create_user(
                email=user.email,
                password=random_password,
                display_name=f"{user.name} {user.last_name}",
            )

            set_custom_user_claims(
                firebase_admin.uid,
                {
                    "id": db_user.id,
                    "role": UserRole.admin,
                    "hospital_id": db_admin.hospital_id,
                },
            )
            db_user.uid = firebase_admin.uid

        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f"Unexpected error: {e}")


def create_doctor(db: Session, user: UserIn, is_test: bool = False) -> User:
    random_password = generate_password()
    hashed_password = bcrypt.hashpw(random_password.encode("utf-8"), bcrypt.gensalt())

    try:
        db_user = User(**user.dict(exclude={"doctor"}), password=hashed_password)
        db_user.created_at = get_current_time()
        db_doctor = Doctor(**user.doctor.dict(exclude={"specialty_ids"}), user=db_user)

        specialties = (
            db.query(Specialty)
            .filter(Specialty.id.in_(user.doctor.specialty_ids))
            .all()
        )

        db_doctor.specialties = specialties

        db.add(db_user)
        db.add(db_doctor)

        if not is_test:
            firebase_doctor: UserInfo = create_user(
                email=user.email,
                password=random_password,
                display_name=f"{user.name} {user.last_name}",
            )

            set_custom_user_claims(
                firebase_doctor.uid,
                {
                    "id": db_user.id,
                    "role": UserRole.doctor,
                    "hospital_id": db_doctor.hospital_id,
                },
            )
            db_user.uid = firebase_doctor.uid

        db.commit()
        db.refresh(db_doctor)

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f"Unexpected error: {e}")


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users(
    db: Session, user_role: UserRole = None, hospital_id: int = None
) -> List[User]:
    if user_role and hospital_id:
        if user_role.value == UserRole.admin:
            return (
                db.query(User)
                .join(Admin)
                .filter(
                    User.user_role == user_role.value, Admin.hospital_id == hospital_id
                )
                .all()
            )
        elif user_role.value == UserRole.doctor:
            return (
                db.query(User)
                .join(Doctor)
                .filter(
                    User.user_role == user_role.value, Doctor.hospital_id == hospital_id
                )
                .all()
            )
    elif hospital_id:
        return (
            db.query(User)
            .join(Doctor)
            .join(Admin)
            .filter(
                Doctor.hospital_id == hospital_id or Admin.hospital_id == hospital_id
            )
            .all()
        )
    elif user_role:
        return db.query(User).filter(User.user_role == user_role.value).all()
    else:
        return db.query(User).all()


def get_user_by_email(db: Session, email: str) -> User:
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        print(traceback.format_exc())
        raise Exception(f"Unexpected error: {e}")


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
        raise Exception(f"Unexpected error: {e}")

    return user


def update_user(db: Session, user_id: int, updated_user: UserUpdate) -> User:
    user = get_user(db, user_id)
    if not user:
        return None

    try:
        for key, value in dict(updated_user).items():
            if do_key_and_value_exist(key, value) and key in ALLOWED_USER_UPDATES:
                setattr(user, key, value)

        if updated_user.patient is not None:
            for key, value in dict(updated_user.patient).items():
                if (
                    do_key_and_value_exist(key, value)
                    and key in ALLOWED_PATIENT_UPDATES
                ):
                    setattr(user.patient, key, value)
        elif updated_user.doctor is not None:
            for key, value in dict(updated_user.doctor).items():
                if do_key_and_value_exist(key, value) and key in ALLOWED_DOCTOR_UPDATES:
                    setattr(user.doctor, key, value)

        user.updated_at = get_current_time()

        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f"Unexpected error: {e}")


def do_key_and_value_exist(key, value) -> bool:
    return key is not None and value is not None


def get_doctors_by_hospital_id(db: Session, hospital_id: int) -> List[User]:
    return db.query(User).join(Doctor).filter(Doctor.hospital_id == hospital_id).all()
