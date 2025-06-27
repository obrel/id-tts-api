from fastapi import FastAPI, Depends
from src.routers import api

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

app.include_router(
    api.router,
    prefix="/api"
)
