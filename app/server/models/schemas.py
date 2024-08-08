from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    email: EmailStr
    password: constr(min_length=8)

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    access_token: str
    token_type: str

class PipelineCreateResponse(BaseModel):
    pipeline_id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    selection: bool
    training: Optional[bool] = None
    inferencing:Optional[bool] = None
    infra: bool
