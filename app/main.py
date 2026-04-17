from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.resumes import router as resumes_rooter
from app.db.base import Base
from app.db.session import engine
from app.models import resume


@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(resumes_rooter)

