from fastapi import FastAPI, status
from starlette.responses import JSONResponse

app = FastAPI(
    title="Appointments", description="Appointments service for HospiCloud app."
)


@app.get("/")
async def home():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"container": "appointments", "message": "Hello World!"}
    )
