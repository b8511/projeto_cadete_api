from typing import List, Dict, Optional
from unittest import skip
from fastapi import APIRouter, HTTPException, status, Depends
from indexers import coingecko
from exceptions import Re_Exceptions
from sqlalchemy.orm import Session
import schemas, database, models


router = APIRouter(
    prefix="/coins",
    tags = ['coins']
)

get_db = database.get_db

import time                                     #temp
from sqlalchemy.sql import text
@router.get('/list_all',response_model=list[schemas.ShowCoins], response_model_exclude_unset=True )
def list_all(db:Session=Depends (get_db)):
    if not database.check_if_db_empty(db) and not (timed_out_items := database.check_if_db_items_timedout(db,300)):
        print("Database_cheks")
        return database.check_db_out(db)
    try:
        coin_list = coingecko.get_list()
    except Re_Exceptions.ServerError as e:
        raise HTTPException(
            status_code=status.HTTP_400_INTERNAL_SERVER_ERROR,
            detail="ServerError",
        ) from e
    if database.check_if_db_empty(db):
        for record in coin_list:
            data_obj= models.Coins(**record)
            data_obj.date = time.time()
            db.add(data_obj)
    elif timed_out_items:
        coin_dict = {item['id']: item for item in coin_list}
        time_now = time.time()
        print ("found timedout items")
        #print (timed_out_items)
        #query = db.query(models.Coins).filter(time_now - models.Coins.date  > 300).all()
        print ("query_done............")
        num = 0
        for i in timed_out_items:
            # if bridge := next((x for x in coin_list if x["id"] == i.id),None):
            if i.id in coin_dict:
                num +=1
                i.symbol = coin_dict[i.id]["symbol"]
                i.name = coin_dict[i.id]["name"]
                i.date = time_now
                print (num)
        lame_shit = db.query(models.Coins).all()
        album = {song.id: {song.id,song.symbol,song.name} for song in lame_shit}
        #coin_dict['----nibas---']= {"id":"----nibas---", "symbol":"idk","name":"OWS"}
        for id_key in coin_dict:
            if id_key not in album:
                data_obj= models.Coins(**coin_dict[id_key])
                data_obj.date = time_now
                db.add(data_obj)
                print (f"added {id_key}")
        for song_id in album:
            if song_id not in coin_dict:
                print (f"{song_id} is gone 🦀")
                db.query(models.Coins).filter(models.Coins.id == song_id).delete()
    db.commit()
    return database.check_db_out(db)

@router.get('/price')#, response_model=Dict[str, Optional[float]]
def coingecko_api_price_id(coin_id,db:Session=Depends (get_db)):
    if res_db := db.query(models.Prices.id,models.Prices.price).filter(models.Prices.id == coin_id).first():
        print("coingecko_api_price_id")
        return res_db
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

@router.get('/all_prices') #, response_model=Dict[str, Optional[float]]
def coingecko_api_all_prices(db:Session=Depends (get_db)):
    if not database.check_if_db_empty_prices(db) and not (timed_out_items := database.check_if_db_items_timedout_prices(db,300)):
        print("Database_cheks")
        return database.check_db_out_prices(db)    

    dict_new = coingecko.get_price_all()
    time_now = time.time()
    if database.check_if_db_empty_prices(db):
        for record in dict_new:
            data_dict={}
            data_dict.update(id=record,price=dict_new[record],date=time_now) 
            data_obj=models.Prices(id=data_dict["id"],price=data_dict["price"],date=time_now)
            db.add(data_obj)
    elif timed_out_items:
        print ("found timedout items")
        num = 0
        for i in timed_out_items:
            if i.id in dict_new:
                num +=1
                i.price = dict_new[i.id]
                i.date = time_now
                print (num)
        lame_shit = db.query(models.Prices).all()
        album = {song.id:song.price for song in lame_shit}
        #dict_new['----nibas---']= 21  #test delll
        for id_key in dict_new:
            if id_key not in album:
                data_dict={}
                data_dict.update(id=id_key,price=dict_new[id_key],date=time_now) 
                data_obj=models.Prices(id=data_dict["id"],price=data_dict["price"],date=time_now)
                db.add(data_obj)
                print (f"added {id_key}")
        for song_id in album:
            if song_id not in dict_new:
                db.query(models.Prices).filter(models.Prices.id == song_id).delete()
                print (f"{song_id} is gone 🦀")
    db.commit()
    return database.check_db_out_prices(db)