# -*- coding: utf-8 -*-
from databases import Session,engine
from models import Osauhingud, FuusilisestIsikustOsanikud, JuriidilisestIsikustOsanikud, many_to_many_table_fuusilised_isikud, many_to_many_table_juriidilised_isikud
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

def fuus_isikud_ik_paring(isikukood):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi, Osauhingud.registri_kood).\
            join(Osauhingud.fuusilised_osanikud).\
            filter(FuusilisestIsikustOsanikud.isikukood==isikukood).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['Osaühingu nimi', 'Registrikood'])
        print(paringu_tagastus)
    return paringu_tagastus

def juur_isikud_nimi_paring(marksona):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi, Osauhingud.registri_kood).\
            join(Osauhingud.juriidilised_osanikud).\
            filter(JuriidilisestIsikustOsanikud.nimi.ilike("%"+marksona+"%")).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['Osaühingu nimi', 'Registrikood'])
        print(paringu_tagastus)
    return paringu_tagastus

def juur_isikud_rk_paring(registrikood):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi, Osauhingud.registri_kood).\
            join(Osauhingud.juriidilised_osanikud).\
            filter(JuriidilisestIsikustOsanikud.registrikood==registrikood).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['Osaühingu nimi', 'Registrikood'])
    return paringu_tagastus

def fuus_isikud_asutamine_nimi_paring(marksona):
    with Session() as session:
        paring = session.query(FuusilisestIsikustOsanikud.index,FuusilisestIsikustOsanikud.nimi,FuusilisestIsikustOsanikud.isikukood).filter(FuusilisestIsikustOsanikud.nimi.ilike("%"+marksona+"%")).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['id','Füüsilisest isikust osaniku nimi', 'Isikukood'])
        paringu_tagastus = paringu_tagastus.to_dict(orient='list')
    return paringu_tagastus
        
def fuus_isikud_asutamine_ik_paring(isikukood):
    with Session() as session:
        paring = session.query(FuusilisestIsikustOsanikud.index,FuusilisestIsikustOsanikud.nimi,FuusilisestIsikustOsanikud.isikukood).filter(FuusilisestIsikustOsanikud.isikukood==isikukood).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['id','Füüsilisest isikust osaniku nimi', 'Isikukood'])
        paringu_tagastus = paringu_tagastus.to_dict(orient='list')
    return paringu_tagastus

def juur_isikud_asutamine_nimi_paring(marksona):
    with Session() as session:
        paring = session.query(JuriidilisestIsikustOsanikud.index, JuriidilisestIsikustOsanikud.nimi,JuriidilisestIsikustOsanikud.registrikood).filter(JuriidilisestIsikustOsanikud.nimi.ilike("%"+marksona+"%")).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['id','Juriidilisest isikust osaniku nimi', 'Registrikood'])
        paringu_tagastus = paringu_tagastus.to_dict(orient='list')
    return paringu_tagastus

def juur_isikud_asutamine_rk_paring(registrikood):
    with Session() as session:
        paring = session.query(JuriidilisestIsikustOsanikud.index, JuriidilisestIsikustOsanikud.nimi,JuriidilisestIsikustOsanikud.registrikood).filter(JuriidilisestIsikustOsanikud.registrikood==registrikood).all()
        paringu_tagastus=pd.DataFrame(paring, columns=['id','Juriidilisest isikust osaniku nimi', 'Registrikood'])
        paringu_tagastus = paringu_tagastus.to_dict(orient='list')
    return paringu_tagastus    

def lisa_osauhing_andmebaasi(osauhingu_asutamise_dct):
    with Session() as session:
        row = Osauhingud(**osauhingu_asutamise_dct)
        session.add(row)
        session.commit()

def lisa_asutajad_andmebaasi(asutajad):
    with Session() as session:
        if 'fuus' in asutajad.keys():
            fuus=pd.DataFrame(asutajad['fuus'])
            fuus.to_sql('many_to_many_table_fuusilised_isikud',con=engine)
        if 'jur' in asutajad.keys():
            jur=pd.DataFrame(asutajad['jur'])
            jur.to_sql('many_to_many_table_juriidilised_isikud', con=engine)
        session.commit()

def parse_multidict(osauhingu_asutamise_dct):
    assotsiatsiooni_tabeli_data = []
    for key, value in osauhingu_asutamise_dct.items():
        if 'kapital' in key:
            assotsiatsiooni_tabeli_data['osakapital'] = value
        if 'index' in key:
            assotsiatsiooni_tabeli_data['right_id_osanikud'] = value
        assotsiatsiooni_tabeli_data['is_asutaja'] = 'On'
    return assotsiatsiooni_tabeli_data


def pari_osauhingu_tabelid(osauhingu_nimi):
    with Session() as session:
        paring = session.query(Osauhingud.osauhingu_nimi,Osauhingud.registri_kood, Osauhingud.asutamise_kuupaev, Osauhingud.kapital).filter_by(osauhingu_nimi=osauhingu_nimi).first()
        paringu_tagastus=pd.DataFrame([[paring[0], paring[1], paring[2], paring[3]]], columns=['Osaühingu nimi', 'Registrikood', 'Asutamise kuupäev', 'Kapital'])
        fuusilised_osanikud_paring = session.query(FuusilisestIsikustOsanikud.nimi, FuusilisestIsikustOsanikud.isikukood, many_to_many_table_fuusilised_isikud.c.osakapital, many_to_many_table_fuusilised_isikud.c.is_asutaja)\
                .join(many_to_many_table_fuusilised_isikud, FuusilisestIsikustOsanikud.index == many_to_many_table_fuusilised_isikud.c.right_id_osanikud)\
                .join(Osauhingud, Osauhingud.index == many_to_many_table_fuusilised_isikud.c.left_id_osauhingud)\
                .filter(Osauhingud.osauhingu_nimi == osauhingu_nimi).all()
        fuusilised_osanikud_paringu_tagastus = pd.DataFrame(fuusilised_osanikud_paring, columns=['Füüsilisest isikust osaniku nimi','Isikukood','Osakapital','Asutaja?'])
        juriidilised_osanikud_paring = session.query(JuriidilisestIsikustOsanikud.nimi, JuriidilisestIsikustOsanikud.registrikood, many_to_many_table_juriidilised_isikud.c.osakapital, many_to_many_table_juriidilised_isikud.c.is_asutaja)\
                .join(many_to_many_table_juriidilised_isikud, JuriidilisestIsikustOsanikud.index == many_to_many_table_juriidilised_isikud.c.right_id_osanikud)\
                .join(Osauhingud, Osauhingud.index == many_to_many_table_juriidilised_isikud.c.left_id_osauhingud)\
                .filter(Osauhingud.osauhingu_nimi == osauhingu_nimi).all()
        juriidilised_osanikud_paringu_tagastus = pd.DataFrame(juriidilised_osanikud_paring, columns=['Juriidilisest isikust osaniku nimi','Registrikood','Osakapital','Asutaja'])
     
    return paringu_tagastus, fuusilised_osanikud_paringu_tagastus, juriidilised_osanikud_paringu_tagastus