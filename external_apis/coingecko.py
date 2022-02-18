import requests
import time
from exceptions import Re_Exceptions
      

def error_raises(status_code,ignore_not_found = False):
    if status_code >= 200 and status_code < 299 :
        return True
    elif status_code == 429:              
        raise Re_Exceptions.ServerError
    elif status_code >= 400 and status_code < 500 and not ignore_not_found:
        raise Re_Exceptions.CoinNotFoundError           
    elif status_code >= 500:
        raise Re_Exceptions.ServerError

def get_list():
    tries = 0
    while (tries < 3):
        coins_list = requests.get("https://api.coingecko.com/api/v3/coins/list/")
        if coins_list.status_code >= 200 and coins_list.status_code < 299:
            return coins_list.json()
        elif coins_list.status_code == 429:
            time.sleep(1)
            if tries > 3:
                raise Re_Exceptions.ServerError
            else:
                tries += 1



def get_price(coin_id):
    request_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd" .format(coin_id = coin_id))
    if error_raises(request_data.status_code):
        coin_data = request_data.json()
        if "usd" not in coin_data[coin_id]:
            raise Re_Exceptions.NoValueError
        else:
            return (coin_data[coin_id]["usd"])   #print


def get_prices(coin_ids):
    coin_ids_str = "%2c".join(coin_ids)
    request_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd" .format(coin_id = coin_ids_str))
    if error_raises(request_data.status_code, True):
        prices_dict = {}
        for coin_id in coin_ids:
            coin_data = request_data.json()
            if "usd" not in coin_data[coin_id]:
                prices_dict[coin_id] = None
            else:
                prices_dict[coin_id] = coin_data[coin_id]["usd"]
        return prices_dict

