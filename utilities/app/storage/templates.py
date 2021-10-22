import json
import traceback

from common.schemas.template import Template, TemplateIn
from common.models import Template
from dependencies import Session

VALID_HEADER_TYPE = {
    "string": "str",
    "int": "int"
}


def create_template(db: Session, template: TemplateIn) -> Template:
    json_template: dict = json.loads(template.headers)

    numeric_fields: int = 0
    alphanumeric_fields: int = 0

    for _, value in json_template.items():
        header_type = VALID_HEADER_TYPE[value]

        if header_type == "int":
            numeric_fields = numeric_fields + 1
        elif header_type == "str":
            alphanumeric_fields = alphanumeric_fields + 1

    template.numeric_fields = numeric_fields
    template.alphanumeric_fields = alphanumeric_fields

    try:
        db_template = Template(**template.dict())

        db.add(db_template)

        db.commit()
        db.refresh(db_template)

        return db_template
    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        raise Exception(f'Unexpected error: {e}')


def get_template(db: Session, template_id: int) -> Template:
    return db.query(Template).filter(Template.id == template_id).first()
