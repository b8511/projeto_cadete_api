from fastapi import FastAPI
from routers import coins
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session



app = FastAPI() 

models.Base.metadata.create_all(bind=engine)


app.include_router(coins.router)
