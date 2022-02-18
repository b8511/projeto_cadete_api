from pydantic import BaseModel

class ShowCoins(BaseModel):
    id: str
    symbol: str
    name: str
    
class ShowCoinPrice(BaseModel):
    value: float

class ShowCoinsPrices(BaseModel):
    id: str