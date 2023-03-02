# -*- coding: utf-8 -*-
from databases import Session,engine
from models import Osauhingud,Base
from sqlalchemy import create_engine
import pandas as pd

def init_db():
    import models
    with Session() as session:
        pd.read_json('test_andmestik.json').to_sql('osauhingud',con=engine)
        session.commit()


def nimeline_otsing_paring(marksona):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi,Osauhingud.registri_kood).filter(Osauhingud.osauhingu_nimi.ilike("%"+marksona+"%")).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['Osaühingu nimi', 'Registrikood'])
    return paringu_tagastus

'''
[(0, 'Toomsalu, Kõiv and Toots', 9127513, '1993-05-03'), (1, 'Komarov, Kaljuvee and Sirel', 5633978, '2009-04-22'), (2, 'Borissov-Schmidt', 6063902, '1993-07-31'), (3, 'Kuznetsov, Lillemets and Koitla', 9623269, '2007-07-16'), (4, 'Kaljuste, Kutsar and Põder', 8414787, '2014-07-13'), (5, 'Tamme, Poom and Sokolov', 6224231, '1996-05-06'), (6, 'Paap, Toomsalu and Teder', 9308165, '2004-12-29'), (7, 'Jermakov, Luht and Põllu', 2245225, '2016-12-06')  ... displaying 10 of 100 total bound parameter sets ...  (98, 'Tuul-Paap', 4534526, '1995-05-18'), (99, 'Tiik Ltd', 1250669, '1990-09-14')]
'''