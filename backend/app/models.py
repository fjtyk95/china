from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    status = Column(String, default="queued")
