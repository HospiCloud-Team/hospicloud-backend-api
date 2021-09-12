from fastapi import FastAPI, status
from starlette.responses import JSONResponse

app = FastAPI(
    title="Templates", description="Templates service for HospiCloud app."
)


@app.get("/")
async def home():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"container": "templates", "message": "Hello World!"}
    )
