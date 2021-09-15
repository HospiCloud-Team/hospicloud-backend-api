from fastapi import FastAPI, status
from starlette.responses import JSONResponse

from users.app.routers import users

app = FastAPI(
    title="Users",
    description="Users service for HospiCloud app.",
)

app.include_router(users.router)


@app.get("/")
async def home():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={
            "container": "users", "message": "Hello World!"}
    )
