from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, status
from indexers import coingecko
from exceptions import Re_Exceptions
import schemas
import global_can


router = APIRouter(
    prefix="/coins",
    tags = ['coins']
)



@router.get('/list_all',response_model=List[schemas.ShowCoins] )
def list_all():
    if  global_can.time_confirmation(global_can.old_time_list):
        return global_can.list_all_coins
    try:
        coin_list = coingecko.get_list()
    except Re_Exceptions.ServerError as e:
        raise HTTPException(
            status_code=status.HTTP_400_INTERNAL_SERVER_ERROR,
            detail="ServerError",
        ) from e
    print(global_can.time_confirmation(global_can.old_time_dict))
    global_can.list_all_coins= coin_list
    global_can.old_time_list= global_can.time_update()
    print ("I got here")
    return coin_list

@router.get('/price', response_model=float)
def coingecko_api_price_id(coin_id):
    if global_can.time_confirmation(global_can.old_time_dict):
        return global_can.dic_all_coins[coin_id]
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

@router.get('/all_prices', response_model=Dict[str, Optional[float]])
def coingecko_api_all_prices():
    if not global_can.time_confirmation(global_can.old_time_dict):
        print(global_can.time_confirmation(global_can.old_time_dict))
        global_can.dic_all_coins = coingecko.get_price_all()
        global_can.old_time_dict = global_can.time_update()
        print ("i got here")
    return global_can.dic_all_coins

