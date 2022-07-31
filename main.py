from fastapi import FastAPI
from routers import coins
import models
from database import engine



app = FastAPI() 

models.Base.metadata.create_all(bind=engine)


app.include_router(coins.router)
