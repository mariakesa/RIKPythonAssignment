from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy import create_engine

Base = declarative_base()

class Osauhingud(Base):
    __tablename__='osauhingud'

    id = Column(Integer, primary_key = True)
    nimi = Column(String(100), nullable=False)
    registrikood = Column(Integer, nullable=False)
    asutamise_kuupaev= Column(Date)
