from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy import create_engine

Base = declarative_base()

class Osauhingud(Base):
    __tablename__='osauhingud'

    index = Column(Integer, primary_key = True)
    osauhingu_nimi = Column(String(100), nullable=False)
    registri_kood = Column(Integer, nullable=False)
    asutamise_kuupaev= Column(Date)

    def __repr__(self):
        return "<User(index='%s', osauhingu nimi='%s', registri kood='%s', asutamise kuupaev='%s')>" % (
            self.index,
            self.osauhingu_nimi,
            self.registri_kood,
            self.asutamise_kuupaev)