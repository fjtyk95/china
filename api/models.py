from sqlalchemy import Column, String
from .database import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(String, primary_key=True)
    customer_id = Column(String)
    status = Column(String)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    s3_key = Column(String, nullable=False)
    status = Column(String, nullable=False, default="queued")
