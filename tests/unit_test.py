from databases import Session
import random
import pandas as pd
from models import Osauhingud, FuusilisestIsikustOsanikud, JuriidilisestIsikustOsanikud, many_to_many_table_fuusilised_isikud, many_to_many_table_juriidilised_isikud

random.seed(1337)


def unit_test(index):
    '''
    Unit test, mis testib kas osanike kapital on võrdne osaühingu kogukapitaliga. 
    '''
    with Session() as session:
        print(index)
        paring = session.query(Osauhingud.kapital).filter(
            Osauhingud.index == index).all()
        paringu_tagastus_ou = pd.DataFrame(
            paring, columns=['Kapital'])
        # Check uniqueness of primary key
        print(paringu_tagastus_ou)
        assert len(paringu_tagastus_ou) == 1
        fuusilised_osanikud_paring = session.query(FuusilisestIsikustOsanikud.nimi, FuusilisestIsikustOsanikud.isikukood, many_to_many_table_fuusilised_isikud.c.osakapital, many_to_many_table_fuusilised_isikud.c.is_asutaja)\
            .join(many_to_many_table_fuusilised_isikud, FuusilisestIsikustOsanikud.index == many_to_many_table_fuusilised_isikud.c.right_id_osanikud)\
            .join(Osauhingud, Osauhingud.index == many_to_many_table_fuusilised_isikud.c.left_id_osauhingud)\
            .filter(Osauhingud.index == index).all()
        fuusilised_osanikud_paringu_tagastus = pd.DataFrame(fuusilised_osanikud_paring, columns=[
                                                            'Füüsilisest isikust osaniku nimi', 'Isikukood', 'Osakapital', 'Asutaja?'])
        juriidilised_osanikud_paring = session.query(JuriidilisestIsikustOsanikud.nimi, JuriidilisestIsikustOsanikud.registrikood, many_to_many_table_juriidilised_isikud.c.osakapital, many_to_many_table_juriidilised_isikud.c.is_asutaja)\
            .join(many_to_many_table_juriidilised_isikud, JuriidilisestIsikustOsanikud.index == many_to_many_table_juriidilised_isikud.c.right_id_osanikud)\
            .join(Osauhingud, Osauhingud.index == many_to_many_table_juriidilised_isikud.c.left_id_osauhingud)\
            .filter(Osauhingud.index == index).all()
        juriidilised_osanikud_paringu_tagastus = pd.DataFrame(juriidilised_osanikud_paring, columns=[
                                                              'Juriidilisest isikust osaniku nimi', 'Registrikood', 'Osakapital', 'Asutaja?'])
        print('Success!')
        assert len(juriidilised_osanikud_paringu_tagastus) + \
            len(fuusilised_osanikud_paringu_tagastus) > 1
        print(paringu_tagastus_ou.iloc[0]['Kapital'], fuusilised_osanikud_paringu_tagastus['Osakapital'].sum(
            axis=0), juriidilised_osanikud_paringu_tagastus['Osakapital'].sum(axis=0))
        assert paringu_tagastus_ou.iloc[0]['Kapital'] == fuusilised_osanikud_paringu_tagastus['Osakapital'].sum(
            axis=0) + juriidilised_osanikud_paringu_tagastus['Osakapital'].sum(axis=0)
        session.close()
        print('Üks unit test edukalt läbitud!')


def juhusliku_kapitali_gen_test_n(n_test=10):
    '''
    Soorita mitu unit testi erinevate sisendite peal. 
    '''
    # Genereeri juhuslikud indeksid
    n_test_juhtumid = random.sample(range(1, 101), n_test)
    for i in n_test_juhtumid:
        unit_test(i)
    print('Ükski test ei tuvastanud bugisid!')
