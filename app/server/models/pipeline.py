from sqlalchemy import Column, BigInteger, Boolean, Integer, String, DateTime, create_engine, event, text
from sqlalchemy.sql import func
import os
from datetime import datetime
from .db import Base

class Pipeline(Base):
    __tablename__ = 'pipeline'
    pipeline_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    selection = Column(Boolean, default=True)
    training = Column(Boolean)
    inferencing = Column(Boolean)
    infra = Column(Boolean, default=True)
