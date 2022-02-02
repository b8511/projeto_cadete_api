from fastapi import FastAPI
from routers import coins

app = FastAPI()

app.include_router(coins.router)
