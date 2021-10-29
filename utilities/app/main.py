from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from routers import templates, specialty, hospital

app = FastAPI(
    title="Utilities",
    description="Utilities service for HospiCloud app."
)

app.include_router(templates.router)
app.include_router(specialty.router)
app.include_router(hospital.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={
            "container": "utilities", "message": "Hello World!"}
    )
