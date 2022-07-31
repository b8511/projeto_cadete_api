from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData, Table, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base

metadata_obj = MetaData()

coins = Table('coins',metadata_obj,
    Column('id',Integer,primary_key=True),
    Column('symbol',String),
    Column('name',String)
)

class Coins(Base):
    __tablename__ = "coins"

    id = Column(String,primary_key=True)
    symbol = Column(String)
    name = Column(String)
    date = Column(Float)
    usd_price = Column(Float,ForeignKey('prices.id'))
    #email = Column(String, unique=True, index=True)
    #hashed_password = Column(String)
    #is_active = Column(Boolean, default=True)

    price = relationship("Prices", back_populates="coin")

class Prices(Base):
    __tablename__ = "prices"

    id = Column(String,primary_key=True)
    price = Column(Float)
    date = Column(Float)

    coin = relationship("Coins",back_populates="price")
