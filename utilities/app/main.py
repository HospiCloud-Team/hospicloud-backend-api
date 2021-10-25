from fastapi import FastAPI, status
from starlette.responses import JSONResponse
from routers import templates

app = FastAPI(
    title="Utilities",
    description="Utilities service for HospiCloud app."
)

app.include_router(templates.router)


@app.get("/")
async def home():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={
            "container": "utilities", "message": "Hello World!"}
    )
