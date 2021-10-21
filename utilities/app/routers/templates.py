import traceback
from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse

from storage import templates
from common.schemas.template import Template, TemplateIn
from dependencies import get_db, Session

router = APIRouter()


@router.post(
    "/templates",
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
