import traceback
from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse

from storage import templates
from common.schemas.template import Template, TemplateIn
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
    db_template = templates.get_template(db, template_id)
    if db_template is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Template not found"}
        )

    return db_template
