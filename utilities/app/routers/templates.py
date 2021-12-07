import traceback
from typing import Optional, List
from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse

from storage import templates
from common.schemas.template import Template, TemplateIn, TemplateUpdate
from dependencies import get_db, Session

router = APIRouter()


@router.post(
    "/templates",
    response_model=Template,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    tags=["templates"]
)
def create_template(template: TemplateIn, db: Session = Depends(get_db)):
    try:
        existing_template = templates.get_template_by_specialty_id(
            db, template.specialty_id, template.hospital_id)
        if existing_template:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Specialty already has a template assigned"}
            )

        return templates.create_template(db, template)
    except Exception:
        print(traceback.format_exc())

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@router.get(
    "/templates/{template_id}",
    response_model=Template,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["templates"]
)
async def get_template(template_id: int, db: Session = Depends(get_db)):
    db_template = templates.get_template_by_id(db, template_id)
    if db_template is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Template not found"}
        )

    return db_template


@router.get(
    "/templates",
    response_model=List[Template],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["templates"]
)
async def get_templates(hospital_id: Optional[int] = None, db: Session = Depends(get_db)):
    return templates.get_templates_by_hospital_id(db, hospital_id)


@router.put(
    "/templates/{template_id}",
    response_model=Template,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["templates"]
)
async def update_template(template_id: int, template: TemplateUpdate, db: Session = Depends(get_db)):
    try:
        db_template = templates.update_template(db, template_id, template)
        if db_template is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Template not found"}
            )

        return db_template
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@router.delete(
    "/templates/{template_id}",
    response_model=Template,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["templates"]
)
async def delete_template(template_id: int, db: Session = Depends(get_db)):
    try:
        db_template = templates.delete_template(db, template_id)
        if db_template is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Template not found"}
            )

        return db_template
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error, try again later"}
        )


@router.get(
    "/templates/doctors/{doctor_id}",
    response_model=List[Template],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    tags=["templates"]
)
async def get_templates_by_doctor_id(doctor_id: int, db: Session = Depends(get_db)):
    return templates.get_templates_by_doctor_id(db, doctor_id)
