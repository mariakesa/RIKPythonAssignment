from faker import Faker
import json
import random
from datetime import date
import json
import numpy as np
import pandas as pd

random.seed(444)
Faker.seed(777)
Faker.seed(777)
np.random.seed(1616)


# Genereeri osanikud

def juhuslik_registrikood(n):
    '''
    Funktsioon genereerib n-kohalise juhusliku arvu, mis on registrikoodiks.
    '''
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


def juhuslik_osaniku_kapital():
    '''
    Fuktsioon genereerib juhusliku osakapitali, 2500 eurost miljonini.
    '''
    return random.randint(2500, 1e6)


def pseudo_isikukood(n):
    '''
    Funktsioon genereerib n-kohalise juhusliku arvu, mida kasutatakse pseudo-isikukoodina.
    '''
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


def genereeri_fuusiline_isik():
    '''
    Funktsioon genereerib juhusliku fuusilise isiku, kellel on nimi ja isikukood.
    '''
    fake = Faker(['et_EE'])
    fuusiline_isik = fake.name()
    isikukood = pseudo_isikukood(11)
    return {'nimi': fuusiline_isik, 'isikukood': str(isikukood)}


def genereeri_juriidiline_isik():
    '''
    Funktsioon genereerib juhusliku juriidilise isiku kellel on nimi 
    (juriidiline_isik muutuja) ja registrikood.
    '''
    fake = Faker(['et_EE'])
    juriidiline_isik = fake.company()
    registrikood = juhuslik_registrikood(8)
    return {'nimi': juriidiline_isik, 'registrikood': registrikood}


def genereeri_juriidilised_isikud_tabel(n_jur_isikud=200):
    '''
    Fuktsioon genereerib n_jur_isikud arvu juhuslikke juriidilisi isikuid
    ja salvestab need json faili.
    '''
    juriidilised_isikud = []
    for i in range(0, n_jur_isikud):
        juriidilised_isikud.append(genereeri_juriidiline_isik())
    with open('juriidilised_isikud_test.json', 'w', encoding='utf-8') as f:
        json.dump(juriidilised_isikud, f, ensure_ascii=False)


def genereeri_fuusilised_isikud_tabel(n_fuus_isikud=200):
    '''
    Fuktsioon genereerib n_fuus_isikud arvu juhuslikke fuusilisi isikuid
    ja salvestab need json faili.
    '''
    fuusilised_isikud = []
    for i in range(0, n_fuus_isikud):
        fuusilised_isikud.append(genereeri_fuusiline_isik())
    with open('fuusilised_isikud_test.json', 'w', encoding='utf-8') as f:
        json.dump(fuusilised_isikud, f, ensure_ascii=False)


def genereeri_osanikud(n_osanikud_uniq=200, max_n_osanikud=5):
    '''
    Funktsioon genereerib osauhingule vastava osanikude ruhma (suurusega osanike_n_per_osauhing).
    '''
    osanike_n_per_osauhing = np.random.randint(1, max_n_osanikud)
    osanikud = np.random.choice(
        np.arange(1, n_osanikud_uniq+1), osanike_n_per_osauhing, replace=False)
    return osanikud


def genereeri_assotsiatsiooni_tabel(fuusilised_isikud=True, n_osahingud=100):
    '''
    Funktsioon genereerib koigile osauhingutele (n_osahingud osauhingut) osanike ruhma ja
    salvestab selle json faili. Funktsioon on vajalik many-to-many tabelite täitmiseks
    SQLAlchemy's. Igal osaühingul võib olla mitu osanikku ning iga osanik võib kuuluda
    mitmesse osaühingusse. Funktsiooniga on võimalik genereerida nii füüsilised isikud
    kui ka juriidilised isikud.
    left_id_osauhingud ja right_id_osanikud peavad olema ühe võrra inkrementeeritud, sest
    sqlite'i indekseerimine algab 1-st.
    '''
    assotsiatsiooni_tabel = []
    for i in range(1, n_osahingud+1):
        osanikud = genereeri_osanikud()
        for o in osanikud:
            assotsiatsiooni_tabel.append({'left_id_osauhingud': int(i), 'right_id_osanikud': int(o),
                                          'osakapital': juhuslik_osaniku_kapital(),
                                         'is_asutaja': random.choice(['On', 'Ei ole'])})
    assotsiatsiooni_tabel_df = pd.DataFrame(assotsiatsiooni_tabel)
    if fuusilised_isikud:
        with open('fuusilised_isikud_assotsiatsiooni_tabel_test.json', 'w', encoding='utf-8') as f:
            json.dump(assotsiatsiooni_tabel, f, ensure_ascii=False)
    else:
        with open('juriidilised_isikud_assotsiatsiooni_tabel_test.json', 'w', encoding='utf-8') as f:
            json.dump(assotsiatsiooni_tabel, f, ensure_ascii=False)
    return assotsiatsiooni_tabel_df

# Genereeri osanikud ilma kapitalita


def juhusliku_osauhingu_nimi():
    '''
    Funktsioon genereerib juhusliku osaühingu nimi kasutades Faker tööriista.
    Osaühingu nimi võib olla 3-100 märki nagu kirjeldatud ülesande specis.
    '''
    fake = Faker(['et_EE'])
    osauhingu_nimi = fake.company()
    while len(osauhingu_nimi) < 3 or len(osauhingu_nimi) > 100:
        osauhingu_nimi = fake.company()
    return osauhingu_nimi


def juhuslik_asutamise_kuupaev():
    '''
    Funktsioon genereerib juhusliku osaühingu asutamise kuupäeva kasutades Faker libraryt.
    Osaühingud võivad olla maksimaalselt 36 aasta vanad, alates 16 Aprillist, 1986 (minu sünnipäev). 
    '''
    fake = Faker()
    juhuslik_asutamise_kuupaev = str(fake.date_between(
        date.fromisoformat('1986-04-16'), date.today()))
    return juhuslik_asutamise_kuupaev


def juhuslik_osauhing():
    '''
    Funktsioon genereerib ühe juhusliku osaühingu. 
    '''
    juhuslik_osauhing = {
        'osauhingu_nimi': juhusliku_osauhingu_nimi(),
        'registri_kood': juhuslik_registrikood(7),
        'asutamise_kuupaev': juhuslik_asutamise_kuupaev()
    }
    return juhuslik_osauhing


def osauhingud_ilma_kapitalita_df(n_osauhingud=100):
    '''
    Funktsioon genereerib ilma kapitalita tabeli, sest kogukapital on
    vaja väljaarvutada osanike osakapitalist ning see tehakse hiljem pärast
    osanike assotsiatsiooni tabelite genereerimine
    '''
    osauhingud_ilma_kapitalita = []

    for a in range(1, n_osauhingud+1):
        osauhingud_ilma_kapitalita.append(juhuslik_osauhing())

    osauhingud_ilma_kapitalita = pd.DataFrame(osauhingud_ilma_kapitalita)
    return osauhingud_ilma_kapitalita


def total_capital_calculation(osauhingud_ilma_kapitalita, osauhing_assoc_1, osauhing_assoc_2):
    '''
    Funktsioon genereerib firma osaühingu kogukapitali veeru kasutades eelnevalt genereeritud
    osanike ja many-to-many assotsiaani tabeleid. Tabel salvestatakse jsoni formaadis.
    Pandase tabeli indeks tuleb muuta, et vältida off-by-one vea, mis tekib sellest et
    kood on kohandatud sobima 1-põhise sqlite andmebaasi indekseerimisega.
    '''
    # Group association tables by "osauhing" and sum the "osamakse" column
    osauhing_assoc_1_sum = osauhing_assoc_1.groupby(
        "left_id_osauhingud")["osakapital"].sum()
    osauhing_assoc_2_sum = osauhing_assoc_2.groupby(
        "left_id_osauhingud")["osakapital"].sum()

    # Merge the two association tables on "osauhing"
    osauhing_assoc_merged = pd.merge(
        osauhing_assoc_1_sum, osauhing_assoc_2_sum, on="left_id_osauhingud", how="inner")

    # Sum the two "osamakse" columns
    osauhing_assoc_merged_sum = osauhing_assoc_merged.sum(axis=1)

    osauhingud_ilma_kapitalita.index = np.arange(
        1, len(osauhingud_ilma_kapitalita) + 1)

    # Add the new column "osakapital" to "osauhingud_ilma_kapitalita" with the calculated values
    osauhingud_ilma_kapitalita["kapital"] = osauhing_assoc_merged_sum

    osauhingud_kapitaliga = osauhingud_ilma_kapitalita

    osauhingud_kapitaliga.to_json('test_andmestik.json')

    return osauhingud_kapitaliga


def genereeri_test_data_json():
    '''
    Funktsioon ühendab loodud juhuslike andmete genereerimise funktsioonid ühtseks 
    pipeline'ks. 
    '''
    # Genereeri osanikud
    genereeri_juriidilised_isikud_tabel()
    genereeri_fuusilised_isikud_tabel()
    # Genereeri osanikud ilma kapitalita
    osauhingud_ilma_kapitalita = osauhingud_ilma_kapitalita_df()
    # Genereeri many-to-many assotsiatsiooni tabelid.
    assotsiatsiooni_tabel_1_df = genereeri_assotsiatsiooni_tabel()
    assotsiatsiooni_tabel_2_df = genereeri_assotsiatsiooni_tabel(
        fuusilised_isikud=False)
    # Genereeri osauhingute tabel, millel on kapitali veerg, mis on korrektselt täidetud
    total_capital_calculation(osauhingud_ilma_kapitalita,
                              assotsiatsiooni_tabel_1_df, assotsiatsiooni_tabel_2_df)
    print('Testandmed on edukalt genereeritud!')
