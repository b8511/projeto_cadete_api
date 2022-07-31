from external_apis import coingecko
from exceptions import Re_Exceptions
import time, database


def get_list():
    return coingecko.get_list()


def get_price(coin_id):
    return coingecko.get_price(coin_id)


def get_price_all(db):
    if not database.check_if_db_empty(db) and not (timed_out_items := database.check_if_db_items_timedout(db,300)):
        print("Database_cheks")
        list_data = database.check_db_out(db)
    else:
        list_data = coingecko.get_list()
    id_price_dic = {}
    coin_id_list = []
    numb = 0
    tries = 0
    for coin_data in list_data:
        try:
            numb+=1
            coin_id_list.append(coin_data["id"])
            if  coin_data == list_data[-1] or numb == 400:
                print ("###########################")
                res = coingecko.get_prices(coin_id_list)
                id_price_dic.update(res)
                if coin_data == list_data[-1]:
                    return id_price_dic
                numb=0
                coin_id_list = []
        except Re_Exceptions.ServerError:
            time.sleep(10)
            if tries > 3:
                break
            tries += 1
            continue
