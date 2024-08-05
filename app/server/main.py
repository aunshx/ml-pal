from fastapi import FastAPI
from routers import auth
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(auth.router)
# app.include_router(users.router)
