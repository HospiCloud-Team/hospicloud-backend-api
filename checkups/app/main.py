from fastapi import FastAPI, status
from starlette.responses import JSONResponse

app = FastAPI(
    title="Checkups", description="Checkups service for HospiCloud app."
)


@app.get("/")
async def home():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"container": "checkups", "message": "Hello World!"}
    )