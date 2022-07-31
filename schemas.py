from pydantic import BaseModel
from typing import List, Dict, Optional

class ShowCoins(BaseModel):
    id: str
    symbol: str
    name: str
    price: Optional[float] = None
class ShowCoinPrice(BaseModel):
    id : str 
    price : Optional[float] = None

class ShowCoinsPrices(BaseModel):
    id : str = "",
    price : Optional[float] = None

class CoinsB(ShowCoinsPrices):
    class Config():
        orm_mode = True

class Coins(BaseModel):
    id : Optional[str] = None 
    price : Optional[float] = None