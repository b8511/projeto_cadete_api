from fastapi import APIRouter
from repository import coingecko



router = APIRouter(
    prefix="/coins",
    tags = ['coins']
)



@router.get('/list_all')
def list_all():
    return coingecko.get_list()

@router.get('/price')
def coingecko_api_price_id(coin_id):
    return coingecko.get_price(coin_id)

            
