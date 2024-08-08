from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.db import SessionLocal
from models.schemas import PipelineCreateResponse
from models.pipeline import Pipeline
from fastapi.security import HTTPBearer
from auth.auth import VerifyToken


token_auth_scheme = HTTPBearer()

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/pipeline/create",response_model=PipelineCreateResponse)
async def create_pipeline(response: Response, token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()

    print(token)

    db = next(get_db())
    new_pipeline = Pipeline(user_id=result['sub'])
    db.add(new_pipeline)
    db.commit()
    db.refresh(new_pipeline)
    db.close()
    return new_pipeline

@router.get("/pipeline/protected")
def protected_route(token: str = Depends(token_auth_scheme)):
    return {"message": "This is a protected route", "user": token}
