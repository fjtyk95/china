from sqlalchemy import Column, String
from .database import Base

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    s3_key = Column(String)
    status = Column(String)
