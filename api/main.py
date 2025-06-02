from fastapi import FastAPI
from .routes import jobs
from .db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(jobs.router, prefix="/v1")
