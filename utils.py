# -*- coding: utf-8 -*-
from databases import Session,engine
from models import Osauhingud, FuusilisestIsikustOsanikud, JuriidilisestIsikustOsanikud
import pandas as pd

def init_db():
    import models
    with Session() as session:
        pd.read_json('test_andmestik.json').to_sql('osauhingud',con=engine)
        fi_df=pd.read_json('fuusilised_isikud_test.json')
        fi_df['isikukood']=fi_df['isikukood'].astype(str)
        fi_df.to_sql('fuusilisest_isikust_osanikud',con=engine)
        pd.read_json('juriidilised_isikud_test.json').to_sql('juriidilisest_isikust_osanikud',con=engine)
        pd.read_json('fuusilised_isikud_assotsiatsiooni_tabel_test.json').to_sql('many_to_many_table_fuusilised_isikud',con=engine)
        pd.read_json('juriidilised_isikud_assotsiatsiooni_tabel_test.json').to_sql('many_to_many_table_juriidilised_isikud',con=engine)
        session.commit()


def nimeline_otsing_paring(marksona):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi,Osauhingud.registri_kood).filter(Osauhingud.osauhingu_nimi.ilike("%"+marksona+"%")).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['Osaühingu nimi', 'Registrikood'])
        print(paringu_tagastus)
    return paringu_tagastus

def registri_otsing_paring(registrikood):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi,Osauhingud.registri_kood).filter(Osauhingud.registri_kood==registrikood).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['Osaühingu nimi', 'Registrikood'])
        print(paringu_tagastus)
    return paringu_tagastus

def fuus_isikud_nimi_paring(marksona):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi, Osauhingud.registri_kood).\
            join(Osauhingud.fuusilised_osanikud).\
            filter(FuusilisestIsikustOsanikud.nimi.ilike("%"+marksona+"%")).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['Osaühingu nimi', 'Registrikood'])
        print(paringu_tagastus)
    return paringu_tagastus
        

def lisa_uus_osauhing_andmebaasi(osauhingu_asutamise_dct):
    with Session() as session:
        row = Osauhingud(**osauhingu_asutamise_dct)
        session.add(row)
        session.commit()

def pari_osauhingu_tabelid(osauhingu_nimi):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi,Osauhingud.registri_kood, Osauhingud.asutamise_kuupaev).filter_by(osauhingu_nimi=osauhingu_nimi).first()
        print(paring)
        paringu_tagastus=pd.DataFrame([[paring[0], paring[1], paring[2]]], columns=['Osaühingu nimi', 'Registrikood', 'Asutamise kuupäev'])
        fuusilised_osanikud_paring = session.query(FuusilisestIsikustOsanikud.nimi, FuusilisestIsikustOsanikud.isikukood).\
                join(Osauhingud.fuusilised_osanikud).\
                filter(Osauhingud.osauhingu_nimi == osauhingu_nimi).all()
        fuusilised_osanikud_paringu_tagastus=pd.DataFrame(fuusilised_osanikud_paring, columns=['Füüsilisest isikust osaniku nimi', 'Isikukood'])
        print(fuusilised_osanikud_paringu_tagastus)
        juriidilised_osanikud_paring = session.query(JuriidilisestIsikustOsanikud.nimi, JuriidilisestIsikustOsanikud.registrikood).\
                join(Osauhingud.juriidilised_osanikud).\
                filter(Osauhingud.osauhingu_nimi == osauhingu_nimi).all()
        juriidilised_osanikud_paringu_tagastus=pd.DataFrame(juriidilised_osanikud_paring, columns=['Juriidilisest isikust osaniku nimi', 'Registrikood'])
    return paringu_tagastus, fuusilised_osanikud_paringu_tagastus, juriidilised_osanikud_paringu_tagastus

'''
[(0, 'Toomsalu, Kõiv and Toots', 9127513, '1993-05-03'), (1, 'Komarov, Kaljuvee and Sirel', 5633978, '2009-04-22'), (2, 'Borissov-Schmidt', 6063902, '1993-07-31'), (3, 'Kuznetsov, Lillemets and Koitla', 9623269, '2007-07-16'), (4, 'Kaljuste, Kutsar and Põder', 8414787, '2014-07-13'), (5, 'Tamme, Poom and Sokolov', 6224231, '1996-05-06'), (6, 'Paap, Toomsalu and Teder', 9308165, '2004-12-29'), (7, 'Jermakov, Luht and Põllu', 2245225, '2016-12-06')  ... displaying 10 of 100 total bound parameter sets ...  (98, 'Tuul-Paap', 4534526, '1995-05-18'), (99, 'Tiik Ltd', 1250669, '1990-09-14')]
'''