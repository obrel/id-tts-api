from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.routers import api

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/")
async def root():
    return {"status": "ok"}

app.include_router(
    api.router,
    prefix="/api"
)
