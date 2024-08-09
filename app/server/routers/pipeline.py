from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.db import SessionLocal
from models.schemas import PipelineCreateResponse
from models.pipeline import Pipeline
from fastapi.security import HTTPBearer
from auth.auth import VerifyToken
from typing import List


token_auth_scheme = HTTPBearer()

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/pipeline/create", response_model=PipelineCreateResponse)
async def create_pipeline(response: Response, token: str = Depends(token_auth_scheme)):
    try:
        result = VerifyToken(token.credentials).verify()

        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        db: Session = next(get_db())

        new_pipeline = Pipeline(user_id=result['sub'])
        db.add(new_pipeline)
        db.commit()
        db.refresh(new_pipeline)

        return new_pipeline

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    finally:
        try:
            db.close()
        except:
            pass


@router.get("/api/pipeline/get-all", response_model=List[PipelineCreateResponse])
async def get_all_pipelines(response: Response, token: str = Depends(token_auth_scheme)):
    try:
        result = VerifyToken(token.credentials).verify()
        
        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        db: Session = next(get_db())
        
        pipelines = db.query(Pipeline).filter(Pipeline.user_id == result['sub']).all()

        print('HELLO')
        
        if not pipelines:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pipelines found for the user")
            
        return pipelines

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    finally:
        try:
            db.close()
        except:
            pass

