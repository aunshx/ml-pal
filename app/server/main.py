from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, pipeline
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

origins = origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(pipeline.router)