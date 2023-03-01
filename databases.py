from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

engine = create_engine("sqlite:///test.db",echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    import models
    Base.metadata.create_all(bind=engine, checkfirst=True)
    pd.read_json('test_andmestik.json').to_sql('osauhingud',con=engine)
    session=Session()
    session.commit()
    session.close()