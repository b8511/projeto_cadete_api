from fastapi import APIRouter, HTTPException, status
from repository import coingecko
from exceptions import Re_Exceptions



router = APIRouter(
    prefix="/coins",
    tags = ['coins']
)



@router.get('/list_all')
def list_all():
    try:
        coin_list = coingecko.get_list()
    except Re_Exceptions.ServerError as e:
        raise HTTPException(
            status_code=status.HTTP_400_INTERNAL_SERVER_ERROR,
            detail="ServerError",
        ) from e

    return coin_list

@router.get('/price')
def coingecko_api_price_id(coin_id):
    try:
        coin_price = coingecko.get_price(coin_id)
    except Re_Exceptions.ServerError as e:
        raise HTTPException(
            status_code=status.HTTP_400_INTERNAL_SERVER_ERROR,
            detail="ServerError",
        ) from e

    except Re_Exceptions.NoValueError as e:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"Coin with the id {coin_id} did not have information aboutthe price",
        ) from e

    except Re_Exceptions.CoinNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coin with the id {coin_id} was not found!",
        ) from e

    return coin_price 



            
