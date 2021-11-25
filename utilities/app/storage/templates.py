import json
import traceback
from typing import List

from sqlalchemy.sql import text
from sqlalchemy import and_

from common.schemas.template import Template, TemplateIn, TemplateUpdate
from common.models import Template
from common.utils import get_current_time
from dependencies import Session

VALID_HEADER_TYPE = {
    "string": "str",
    "int": "int"
}


def create_template(db: Session, template: TemplateIn) -> Template:
    numeric_fields, alphanumeric_fields = calculate_template_fields(template)

    template.numeric_fields = numeric_fields
    template.alphanumeric_fields = alphanumeric_fields

    try:
        db_template = Template(**template.dict())
        db_template.created_at = get_current_time()

        db.add(db_template)

        db.commit()
        db.refresh(db_template)

        return db_template
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def get_template_by_specialty_id(db: Session, specialty_id: int, hospital_id: int) -> Template:
    return db.query(Template).filter(
        and_(
            Template.specialty_id == specialty_id,
            Template.hospital_id == hospital_id
        )
    ).first()


def get_template_by_id(db: Session, template_id: int) -> Template:
    return db.query(Template).filter(Template.id == template_id).first()


def get_templates_by_hospital_id(db: Session, hospital_id: int) -> Template:
    filter_params: dict = {"hospital_id": hospital_id}

    filter_params = {key: value for (
        key, value) in filter_params.items() if value}

    return db.query(Template).filter_by(**filter_params).all()


def update_template(db: Session, template_id: int, updated_template: TemplateUpdate) -> Template:
    template = get_template_by_id(db, template_id)
    if not template:
        return None

    try:
        if updated_template.title:
            template.title = updated_template.title

        if updated_template.headers:
            numeric_fields, alphanumeric_fields = calculate_template_fields(
                updated_template)

            template.numeric_fields = numeric_fields
            template.alphanumeric_fields = alphanumeric_fields
            template.headers = updated_template.headers

        template.updated_at = get_current_time()

        db.commit()
        db.refresh(template)

        return template
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def delete_template(db: Session, template_id: int) -> Template:
    template = get_template_by_id(db, template_id)
    if not template:
        return None

    try:
        db.delete(template)
        db.commit()
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')

    return template


def get_templates_by_doctor_id(db: Session, doctor_id: int) -> List[Template]:
    statement = text("""
        SELECT
            t.*
        FROM
            doctor as d
        INNER JOIN doctor_specialty as ds
            ON d.id = ds.doctor_id
        INNER JOIN specialty as s
            ON s.id = ds.specialty_id
        INNER JOIN template as t
            ON t.specialty_id = s.id
        WHERE
            d.id = :doctor_id;
    """)

    parameters = {"doctor_id": doctor_id}

    return db.execute(statement, params=parameters).all()


def calculate_template_fields(template: TemplateIn):
    json_template: dict = json.loads(template.headers)

    numeric_fields: int = 0
    alphanumeric_fields: int = 0

    for _, value in json_template.items():
        header_type = VALID_HEADER_TYPE[value]

        if header_type == "int":
            numeric_fields = numeric_fields + 1
        elif header_type == "str":
            alphanumeric_fields = alphanumeric_fields + 1

    return numeric_fields, alphanumeric_fields
