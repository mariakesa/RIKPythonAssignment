from app import app
from flask import render_template, redirect, request
from forms import *
from utils import *
import pandas as pd
import urllib

@app.route('/', methods=['GET','POST'])
@app.route('/avaleht',methods=['GET','POST'])
def avaleht():
    nimeline_otsing = NimelineOtsinguRiba()
    registri_numbri_otsing = RegistriOtsinguRiba()
    fuus_isikud_nimeline_otsing = FuusIsikudNimelineOtsing()
    fuus_isikud_ik_otsing = FuusIsikudIsikukoodiOtsing()
    juur_isikud_nimeline_otsing = JuriidilisedIsikudNimelineOtsing()
    juur_isikud_rk_otsing = JuriidilisedIsikudRegistrikoodiOtsing()
    paringu_tagastus = pd.DataFrame()
    if nimeline_otsing.validate_on_submit():
        paringu_tagastus = nimeline_otsing_paring(nimeline_otsing.marksona.data)
        print(nimeline_otsing.marksona.data,paringu_tagastus)
    if registri_numbri_otsing.validate_on_submit():
        paringu_tagastus = registri_otsing_paring(registri_numbri_otsing.registrikood.data)
    if fuus_isikud_nimeline_otsing.validate_on_submit():
        paringu_tagastus = fuus_isikud_nimi_paring(fuus_isikud_nimeline_otsing.fuus_is_marksona.data)
    if fuus_isikud_ik_otsing.validate_on_submit():
        paringu_tagastus = fuus_isikud_ik_paring(fuus_isikud_ik_otsing.isikukood.data)
    if juur_isikud_nimeline_otsing.validate_on_submit():
        paringu_tagastus = juur_isikud_nimi_paring(juur_isikud_nimeline_otsing.juur_is_marksona.data)
    if juur_isikud_rk_otsing.validate_on_submit():
        paringu_tagastus = juur_isikud_rk_paring(juur_isikud_rk_otsing.juur_is_registrikood.data)
    return render_template('avaleht.html', 
                            nimeline_otsing = nimeline_otsing, 
                            registri_otsing = registri_numbri_otsing,
                            fuus_isikud_nimeline_otsing = fuus_isikud_nimeline_otsing,
                            fuus_isikud_ik_otsing = fuus_isikud_ik_otsing,
                            juur_isikud_nimeline_otsing = juur_isikud_nimeline_otsing,
                            juur_isikud_rk_otsing = juur_isikud_rk_otsing,
                            df=paringu_tagastus)

@app.route('/osauhingud/<osauhingu_nimi>')
def osauhingu_andmed(osauhingu_nimi):
    osauhingu_nimi = urllib.parse.unquote(osauhingu_nimi)
    andmed = pari_osauhingu_tabelid(osauhingu_nimi)
    return render_template('osauhingu_andmed.html',osauhingu_nimi=osauhingu_nimi,andmed=andmed)

@app.route('/osaniku_otsing', methods=['POST'])
def osaniku_otsing():
    args = request.json
    mapping = {
        'nimi': fuus_isikud_asutamine_nimi_paring,
        'isikukood': fuus_isikud_asutamine_ik_paring,
        'registrikood': juur_isikud_asutamine_rk_paring,
        'jur_nimi': juur_isikud_asutamine_nimi_paring,
    }
    for parameeter, funktsioon in mapping.items():
        if parameeter in args:
            return funktsioon(args[parameeter])
    return "bad request", 400

@app.route('/osauhingu_asutamine', methods=['GET','POST'])
def osauhingu_asutamine():
    osauhingu_asutamise_vorm = OsauhinguAsutamiseVorm()
    fuus_isikud_nimeline_otsing = FuusIsikudNimelineOtsing()
    fuus_isikud_ik_otsing = FuusIsikudIsikukoodiOtsing()
    juur_isikud_nimeline_otsing = JuriidilisedIsikudNimelineOtsing()
    juur_isikud_rk_otsing = JuriidilisedIsikudRegistrikoodiOtsing()
    otsing_dct = {}
    otsing_dct['fuus_isikud_nimeline_otsing'] = fuus_isikud_nimeline_otsing
    otsing_dct['fuus_isikud_ik_otsing'] = fuus_isikud_ik_otsing
    otsing_dct['juur_isikud_nimeline_otsing'] = juur_isikud_nimeline_otsing
    otsing_dct['juur_isikud_rk_otsing'] = juur_isikud_rk_otsing
    fuus_paringu_tagastus={'columns':[],'data':[]}
    juur_paringu_tagastus=pd.DataFrame()
    if fuus_isikud_nimeline_otsing.validate_on_submit():
        fuus_paringu_tagastus = fuus_isikud_asutamine_nimi_paring(fuus_isikud_nimeline_otsing.fuus_is_marksona.data)
    if fuus_isikud_ik_otsing.validate_on_submit():
        fuus_paringu_tagastus = fuus_isikud_asutamine_ik_paring(fuus_isikud_ik_otsing.isikukood.data)
    if juur_isikud_nimeline_otsing.validate_on_submit():
        juur_paringu_tagastus = juur_isikud_asutamine_nimi_paring(juur_isikud_nimeline_otsing.juur_is_marksona.data)
    if juur_isikud_rk_otsing.validate_on_submit():
        juur_paringu_tagastus = juur_isikud_asutamine_rk_paring(juur_isikud_rk_otsing.juur_is_registrikood.data)
    #if osauhingu_asutamise_vorm.validate_on_submit():
        #osauhingu_nimi=osauhingu_asutamise_vorm.osauhingu_nimi.data
        #print('boom',osauhingu_asutamise_vorm.fuus_is_asutajad.data)
        #osauhingu_asutamise_dct={}
        #osauhingu_asutamise_dct['osauhingu_nimi']=osauhingu_nimi
        #osauhingu_asutamise_dct['registri_kood']=osauhingu_asutamise_vorm.registrikood.data
        #osauhingu_asutamise_dct['asutamise_kuupaev']=osauhingu_asutamise_vorm.asutamise_kuupaev.data
        #osauhingu_asutamise_dct['is_asutaja']='On'
        #osauhingu_asutamise_vorm.osauhingu_nimi.data=None
        #osauhingu_asutamise_vorm.registrikood.data=None
        #osauhingu_asutamise_vorm.asutamise_kuupaev.data=None
        #lisa_uus_osauhing_andmebaasi(osauhingu_asutamise_dct)
        #redirect_url = request.form.get('redirect_url').replace('osauhingu_nimi_placeholder', osauhingu_nimi)
        #return redirect(redirect_url)
    else:
        edu='Andmed ei ole andmebaasi salvestatud.'
    return render_template('osauhingu_asutamine.html', osauhingu_asutamise_vorm=osauhingu_asutamise_vorm, edu_sonum=edu, 
                           otsing_dct=otsing_dct,fuus_paringu_tagastus=fuus_paringu_tagastus, juur_paringu_tagastus=juur_paringu_tagastus)

@app.route('/osauhingu_asutamine/entry', methods=['POST'])
def lisa_uus_osauhing_andmebaasi():
    if request.method == 'POST':
        print(request.form.keys())
        print('Shalala', request.form)
        kapital = 0
        for key, value in request.form.items():
            if key.endswith("kapital"):
                try:
                    summa = int(value)
                except ValueError:
                    return "Vigane osakapital: ei ole täisarv", 400
                if summa <= 0:
                    return "Vigane osakapital: negatiivne arv", 400
                kapital += summa
        if kapital < 2500:
            return "Vigane kogukapital: summa alla miinimumnõude", 400
        print("Kapital", kapital)
        osauhingu_asutamise_dct = {}
        osauhingu_asutamise_dct['osauhingu_nimi'] = request.form['osauhingu_nimi']
        osauhingu_asutamise_dct['registri_kood'] = request.form['registrikood']
        osauhingu_asutamise_dct['asutamise_kuupaev'] = request.form['asutamise_kuupaev']
        osauhingu_asutamise_dct['kapital']=kapital
        asutajad = {}
        for key, value in request.form.items():
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
            asutajad[fuusJur][id][index_kapital] = int(value) #valideeritud eelpool
            asutajad[fuusJur][id]['is_asutaja'] = 'On'
        print(asutajad)
        tabel = {}
        for fj, dct in asutajad.items():
            tabel[fj] = [row for _, row in dct.items()]
        print(tabel)
        #lisa_osauhing_andmebaasi(osauhingu_asutamise_dct)
        #lisa_asutajad_andmebaasi(tabel)
    return redirect('/')
    