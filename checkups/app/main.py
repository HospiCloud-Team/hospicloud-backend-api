from common import database
from fastapi import FastAPI, status
from starlette.responses import JSONResponse

app = FastAPI(
    title="Checkups", description="Checkups service for HospiCloud app."
)

engine = database.start_engine()
database.create_tables(engine)

@app.get("/", tags=["checkups"])
async def read_checkups():
    pass

@app.post("/", tags=["checkups"])
async def add_checkup():
    pass