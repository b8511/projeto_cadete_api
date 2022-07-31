from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import time

SQLALCHEMY_DATABASE_URL = "sqlite:///./coins.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import models

def check_if_db_empty(db:Session):
    print("is db empty?")
    if db.query(models.Coins).first():
        print ("no____________")
        return False
    print ("yes____________")
    return True
    
def check_if_db_items_timedout(db:Session,max_timestamps):
    time_now = time.time()
    list_low =db.query(models.Coins)\
        .filter(time_now - models.Coins.date  > max_timestamps)\
        .all()
    print (f'timed out items: {len(list_low)}')
    if len(list_low) == 0:
        return False
    return (list_low)
def check_db_out(db:Session):
    return db.query(models.Coins.id,models.Coins.symbol,models.Coins.name).all()

# def load_db_all():
# def load_db_timedout_items():
# def add_n_rmov_items():

def check_if_db_empty_prices(db:Session):
    print("is db empty?")
    if db.query(models.Prices).first():
        print ("no____________")
        return False
    print ("yes____________")
    return True

def check_if_db_items_timedout_prices(db:Session,max_timestamps):
    time_now = time.time()
    list_low =db.query(models.Prices)\
        .filter(time_now - models.Prices.date  > max_timestamps)\
        .all()
    print (f'timed out items: {len(list_low)}')
    if len(list_low) == 0:
        return False
    return (list_low)

def check_db_out_prices(db:Session):
    return db.query(models.Prices.id,models.Prices.price).all()