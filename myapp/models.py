from sqlalchemy import Column, Integer, Float, String
from .db import Base


# creating table for database 
# Initializing all the column in database with validation 

class Address(Base):
    __tablename__ = "addresstable"

    id = Column(Integer, primary_key=True, index=True)
    userAddress = Column(String)
    userName = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postalCode = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    mapUrl = Column(String)