from fastapi import FastAPI
from routers import coins
import global_can

global_can.init()

app = FastAPI() 

app.include_router(coins.router)
