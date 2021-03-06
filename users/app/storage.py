import bcrypt
import traceback
from typing import List

from firebase_admin import initialize_app
from firebase_admin import auth
from sqlalchemy import or_
from sqlalchemy.sql import text

from dependencies import Session
from common.schemas.user import User, UserIn, UserRole, UserUpdate
from common.models import Base, Patient, User, Admin, Doctor, Specialty, Checkup
from utils import generate_password
from common.utils import get_current_time

ALLOWED_USER_UPDATES = ["name", "last_name",
                        "date_of_birth", "document_number"]

ALLOWED_PATIENT_UPDATES = ["medical_background"]

ALLOWED_DOCTOR_UPDATES = ["schedule", "specialties"]

firebase_app = initialize_app()


def create_patient(db: Session, user: UserIn, is_test: bool = False) -> User:
    random_password = generate_password()
    hashed_password = bcrypt.hashpw(
        random_password.encode("utf-8"), bcrypt.gensalt())

    try:
        db_user = User(
            **user.dict(exclude={"patient"}), password=hashed_password)
        db_user.created_at = get_current_time()
        db_patient = Patient(**user.patient.dict(), user=db_user)

        db.add(db_user)
        db.add(db_patient)

        db.commit()
        db.refresh(db_user)

        if not is_test:
            firebase_patient: auth.UserInfo = auth.create_user(
                email=user.email,
                password=random_password,
                display_name=f"{user.name} {user.last_name}",
            )

            auth.set_custom_user_claims(
                firebase_patient.uid,
                {"id": db_user.id, "user_role": UserRole.patient, "hospital_id": None},
            )
            db_user.uid = firebase_patient.uid

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f"Unexpected error: {e}")


def create_admin(db: Session, user: UserIn, is_test: bool = False) -> User:
    random_password = generate_password()
    hashed_password = bcrypt.hashpw(
        random_password.encode("utf-8"), bcrypt.gensalt())

    try:
        db_user = User(
            **user.dict(exclude={"admin"}), password=hashed_password)
        db_user.created_at = get_current_time()

        db_admin = Admin(**user.admin.dict(), user=db_user)

        db.add(db_user)
        db.add(db_admin)

        db.commit()
        db.refresh(db_user)

        if not is_test:
            firebase_admin: auth.UserInfo = auth.create_user(
                email=user.email,
                password=random_password,
                display_name=f"{user.name} {user.last_name}",
            )

            auth.set_custom_user_claims(
                firebase_admin.uid,
                {
                    "id": db_user.id,
                    "user_role": UserRole.admin,
                    "hospital_id": db_admin.hospital_id,
                },
            )
            db_user.uid = firebase_admin.uid

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f"Unexpected error: {e}")


def create_doctor(db: Session, user: UserIn, is_test: bool = False) -> User:
    random_password = generate_password()
    hashed_password = bcrypt.hashpw(
        random_password.encode("utf-8"), bcrypt.gensalt())

    try:
        db_user = User(
            **user.dict(exclude={"doctor"}), password=hashed_password)
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

        if not is_test:
            firebase_doctor: auth.UserInfo = auth.create_user(
                email=user.email,
                password=random_password,
                display_name=f"{user.name} {user.last_name}",
            )

            auth.set_custom_user_claims(
                firebase_doctor.uid,
                {
                    "id": db_user.id,
                    "user_role": UserRole.doctor,
                    "hospital_id": db_doctor.hospital_id,
                },
            )
            db_user.uid = firebase_doctor.uid

        return db_user
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f"Unexpected error: {e}")


def get_user(db: Session, user_id: int = None, document_number: str = None) -> User:
    if user_id:
        return db.query(User).filter(User.id == user_id).first()

    return db.query(User).filter(User.document_number == document_number).first()


def get_users(
    db: Session, user_role: UserRole = None, hospital_id: int = None,
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
            .outerjoin(Doctor)
            .outerjoin(Admin)
            .filter(
                or_(Doctor.hospital_id == hospital_id,
                    Admin.hospital_id == hospital_id)
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


def delete_user(db: Session, user_id: int, test=False) -> User:
    user = get_user(db, user_id)
    if not user:
        return None

    try:
        if not test:
            auth.delete_user(user.uid)
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

        is_patient_user = updated_user.patient is not None and user.user_role == UserRole.patient
        is_doctor_user = updated_user.doctor is not None and user.user_role == UserRole.doctor

        if is_patient_user:
            for key, value in dict(updated_user.patient).items():
                if (
                    do_key_and_value_exist(key, value)
                    and key in ALLOWED_PATIENT_UPDATES
                ):
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
        raise Exception(f"Unexpected error: {e}")


def do_key_and_value_exist(key, value) -> bool:
    return key is not None and value is not None


def get_doctors_by_hospital_id(db: Session, hospital_id: int) -> List[User]:
    return db.query(User).join(Doctor).filter(Doctor.hospital_id == hospital_id).all()


def get_history(db: Session, user_id: int) -> List[User]:
    user = get_user(db, user_id)
    if not user:
        return None

    if user.user_role.name == UserRole.patient.name:
        return get_patient_history(db, user.patient.id)

    return get_doctor_history(db, user.doctor.id)


def get_patient_history(db: Session, patient_id: int) -> List[User]:
    statement = text("""
    SELECT
	    "user".id
    FROM
        checkup
    INNER JOIN doctor
        ON doctor.id = checkup.doctor_id
    INNER JOIN "user"
        ON "user".id = doctor.user_id
    WHERE
        patient_id = :patient_id;
    """)

    parameters = {"patient_id": patient_id}

    output = db.execute(statement, params=parameters).all()

    doctor_ids = [value for (value,) in output]

    return db.query(User).filter(User.id.in_(doctor_ids)).all()


def get_doctor_history(db: Session, doctor_id: int) -> List[User]:
    statement = text("""
    SELECT
        "user".id
    FROM
        checkup
    INNER JOIN patient
        ON patient.id = checkup.patient_id
    INNER JOIN "user"
        ON "user".id = patient.user_id
    WHERE
        doctor_id = 1;
    """)

    parameters = {"doctor_id": doctor_id}

    output = db.execute(statement, params=parameters).all()

    patient_ids = [value for (value,) in output]

    return db.query(User).filter(User.id.in_(patient_ids)).all()
