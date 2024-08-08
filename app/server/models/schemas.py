from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime
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
