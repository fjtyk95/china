from fastapi import FastAPI

from .database import engine, Base
from .routes import billing, jobs

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(billing.router)
app.include_router(jobs.router, prefix="/v1")
