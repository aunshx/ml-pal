from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

origins = origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pipeline.router)
