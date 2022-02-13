import requests
import time
from exceptions import Re_Exceptions
      

def error_raises(status_code):
    if status_code >= 200 and status_code < 299 :
        return True
    elif status_code == 429:              
        raise Re_Exceptions.ServerError
    elif status_code >= 400 and status_code < 500:
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


def get_price_all():
    list_data = get_list()
    id_price_dic = {}
    url_string = "https://api.coingecko.com/api/v3/simple/price?ids="
    numb = 0
    tries = 0
    while True:
        try:
            for i in list_data:
                if  i == list_data[-1]:
                    url_string += f'{i["id"]}&vs_currencies=usd'
                    prices_carriage = requests.get(url_string)
                    if error_raises(prices_carriage.status_code):
                        prices_carriage =prices_carriage.json()
                        for key in prices_carriage:
                            if prices_carriage[key]:
                                id_price_dic[key] = prices_carriage[key]["usd"]
                        return id_price_dic
                elif numb == 400 :
                    url_string += "&vs_currencies=usd"
                    prices_carriage = requests.get(url_string)
                    if error_raises(prices_carriage.status_code):
                        prices_carriage = prices_carriage.json()
                        for key in prices_carriage :
                            if prices_carriage[key]:
                                id_price_dic[key] = prices_carriage[key]["usd"]
                        #id_price_dic = {key: key["usd"] for key in prices_carriage}
                    numb = 0
                    url_string = "https://api.coingecko.com/api/v3/simple/price?ids="
                else:
                    numb+=1
                    url_string += f'{i["id"]}%2c'
        except Re_Exceptions.NoValueError:
            pass
        except Re_Exceptions.ServerError:
            time.sleep(10)
            if tries > 3:
                break
            tries += 1
            continue
        except Re_Exceptions.CoinNotFoundError:
            pass

    return id_price_dic
