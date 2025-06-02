from sqlalchemy import Column, String
from .database import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(String, primary_key=True)
    customer_id = Column(String)
    status = Column(String)
