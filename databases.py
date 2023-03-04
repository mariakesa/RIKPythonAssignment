from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

engine = create_engine("sqlite:///test.db",echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
#Base.metadata.create_all(engine)
