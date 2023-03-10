# -*- coding: utf-8 -*-
from databases import Session,engine, Base
from models import Osauhingud, FuusilisestIsikustOsanikud, JuriidilisestIsikustOsanikud, many_to_many_table_fuusilised_isikud, many_to_many_table_juriidilised_isikud
import pandas as pd
from data_generation import genereeri_test_data_json


###Andmebaasi initsialiseerimine
def init_db():
    '''
    Kood initsialiseerib andmebaasi ning juhuslike andmetega jsoni failid ja lisab need andmebaasi.
    '''
    import models
    Base.metadata.create_all(engine)
    genereeri_test_data_json()
    with Session() as session:
        pd.read_json('test_andmestik.json').to_sql('osauhingud',if_exists='append',index=False,con=engine)
        fi_df=pd.read_json('fuusilised_isikud_test.json')
        fi_df['isikukood']=fi_df['isikukood'].astype(str)
        fi_df.to_sql('fuusilisest_isikust_osanikud',if_exists='append',con=engine)
        pd.read_json('juriidilised_isikud_test.json').to_sql('juriidilisest_isikust_osanikud',if_exists='append',index=False,con=engine)
        pd.read_json('fuusilised_isikud_assotsiatsiooni_tabel_test.json').to_sql('many_to_many_table_fuusilised_isikud',if_exists='append',index=False, con=engine)
        pd.read_json('juriidilised_isikud_assotsiatsiooni_tabel_test.json').to_sql('many_to_many_table_juriidilised_isikud',if_exists='append',index=False,con=engine)
        session.commit()

###Avalehel olevate otsingutega assotsieeruvad päringud
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


###Osaühingute asutamisel vajaminevad päringud
def osauhingu_paring_add_db(registrikood):
    '''
    Osaühingu asutamisel tekib vajadus täita many-to-many tabelid. Selleks on vaja
    äsja osaühingute tabelisse lisatud osaühingu indeksit. See päring teostab
    selle ülesande. 
    '''
    with Session(bind=engine) as session:
        paring = session.query(Osauhingud.index, Osauhingud.registri_kood).\
            filter(Osauhingud.registri_kood==registrikood).all()
    paringu_tagastus=pd.DataFrame(paring, columns=['Index', 'Registrikood'])
    return paringu_tagastus

#Osaühingute asutamisel on vaja otsida füüsilisi ja juriidilisi isikuid. Allolevad päringud teostavad
#selle ülesande.
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
 
###Uute andmete andmebaasi lisamine
def lisa_osauhing_andmebaasi(osauhingu_asutamise_dct):
    with Session() as session:
        row = Osauhingud(**osauhingu_asutamise_dct)
        session.add(row)
        session.commit()

def lisa_asutajad_andmebaasi(asutajad):
    with Session() as session:
        if 'fuus' in asutajad.keys():
            fuus=pd.DataFrame(asutajad['fuus'])
            fuus.to_sql('many_to_many_table_fuusilised_isikud',index=False, if_exists='append', con=engine)
        if 'jur' in asutajad.keys():
            jur=pd.DataFrame(asutajad['jur'])
            jur.to_sql('many_to_many_table_juriidilised_isikud', index=False,if_exists='append',con=engine)
        session.commit()

def genereeri_many_to_many_tabelid(asutaja_dct,indeks):
    '''
    Kood parseb vormist tuleva multidict'i jsoni kujuliseks,
    selleks et selle saaks andmebaasi ladustada.
    '''
    asutajad = {}
    for key, value in asutaja_dct:
        keys = key.split('-')
        if len(keys) != 3:
            continue
        fuusJur, id, index_kapital = keys
        if fuusJur not in ('fuus', 'jur'):
            continue
        if fuusJur not in asutajad:
            asutajad[fuusJur] = {}
        if id not in asutajad[fuusJur]:
            asutajad[fuusJur][id] = {}
        asutajad[fuusJur][id][index_kapital] = int(value) #valideeritud routes.py's
        asutajad[fuusJur][id]['is_asutaja'] = 'On'
        asutajad[fuusJur][id]['left_id_osauhingud']=indeks
    tabel = {}
    for fj, dct in asutajad.items():
        tabel[fj] = [row for _, row in dct.items()]
    return tabel

## Päring, et veenduda, et uue osaühingu nimi on unikaalne (sest osaühingu vaatamise route sõltub osaühingu nimest)
def nimede_paring(osauhingu_nimi):
    with Session(bind=engine) as session:
        paring = session.query(Osauhingud.osauhingu_nimi).\
        filter(Osauhingud.osauhingu_nimi==osauhingu_nimi).all()
    paringu_tagastus=pd.DataFrame(paring, columns=['Osaühingu nimi'])
    return paringu_tagastus


###Osaühingu andmete kuvamisel vajaminevad andmed tulevad sellest päringust. 
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
        juriidilised_osanikud_paringu_tagastus = pd.DataFrame(juriidilised_osanikud_paring, columns=['Juriidilisest isikust osaniku nimi','Registrikood','Osakapital','Asutaja?'])
     
    return paringu_tagastus, fuusilised_osanikud_paringu_tagastus, juriidilised_osanikud_paringu_tagastus