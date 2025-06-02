from sqlalchemy import Column, String
from .db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    s3_key = Column(String, nullable=False)
    status = Column(String, nullable=False, default="queued")
