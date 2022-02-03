import requests
from fastapi import HTTPException, status
import time
      

def error(status_code,coin_id):
    if status_code >= 200 and status_code < 299 :
        return True
    elif status_code == 429:              
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Server could not handle too many requests")
    elif status_code >= 400 and status_code < 500:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Coin with the id {coin_id} was not found!")             
    elif status_code >= 500:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ServerError")

def get_list():
    tries = 0
    while (tries < 3):
        coinfirm = requests.get("https://api.coingecko.com/api/v3/coins/list/")
        if coinfirm.status_code >= 200 and coinfirm.status_code < 299:
            return requests.get("https://api.coingecko.com/api/v3/coins/list/").json()
        elif coinfirm.status_code == 429:
            time.sleep(1)
            if tries > 3:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ServerError")
            else:
                tries += 1



def get_price(coin_id):
    price_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd" .format(coin_id = coin_id))
    data_status_code = price_data.status_code
    if error(data_status_code ,coin_id):
        price_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd" .format(coin_id = coin_id)).json()
        if "usd" not in price_data[coin_id]:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Coin with the id {coin_id} did not have information aboutthe price")
        else:
            return (price_data[coin_id]["usd"], data_status_code)   #print