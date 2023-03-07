from app import app
from flask import render_template, redirect
from forms import *
from utils import nimeline_otsing_paring, lisa_uus_osauhing_andmebaasi, pari_osauhingu_tabelid
import pandas as pd
import urllib

@app.route('/', methods=['GET','POST'])
@app.route('/avaleht',methods=['GET','POST'])
def avaleht():
    nimeline_otsing = NimelineOtsinguRiba()
    registri_numbri_otsing = RegistriOtsinguRiba()
    paringu_tagastus=pd.DataFrame()
    if nimeline_otsing.validate_on_submit():
        paringu_tagastus=nimeline_otsing_paring(nimeline_otsing.marksona.data)
        print(nimeline_otsing.marksona.data,paringu_tagastus)
    return render_template('avaleht.html', 
                           nimeline_otsing=nimeline_otsing, 
                           registri_numbri_otsing=registri_numbri_otsing,
                           df=paringu_tagastus)

@app.route('/osauhingud/<osauhingu_nimi>')
def osauhingu_andmed(osauhingu_nimi):
    osauhingu_nimi = urllib.parse.unquote(osauhingu_nimi)
    andmed = pari_osauhingu_tabelid(osauhingu_nimi)
    return render_template('osauhingu_andmed.html',osauhingu_nimi=osauhingu_nimi,andmed=andmed)

@app.route('/osauhingu_asutamine', methods=['GET','POST'])
def osauhingu_asutamine():
    osauhingu_asutamise_vorm = OsauhinguAsutamiseVorm()
    if osauhingu_asutamise_vorm.validate_on_submit():
        print('boom',osauhingu_asutamise_vorm.fuus_is_asutajad.data)
        osauhingu_asutamise_dct={}
        osauhingu_asutamise_dct['osauhingu_nimi']=osauhingu_asutamise_vorm.osauhingu_nimi.data
        osauhingu_asutamise_dct['registri_kood']=osauhingu_asutamise_vorm.registrikood.data
        osauhingu_asutamise_dct['asutamise_kuupaev']=osauhingu_asutamise_vorm.asutamise_kuupaev.data
        osauhingu_asutamise_vorm.osauhingu_nimi.data=None
        osauhingu_asutamise_vorm.registrikood.data=None
        osauhingu_asutamise_vorm.asutamise_kuupaev.data=None
        edu='Osaühing on edukalt loodud.'
        return redirect('/osauhingud/'+osauhingu_asutamise_dct['osauhingu_nimi'])
    else:
        edu='Andmed ei ole andmebaasi salvestatud.'
    return render_template('osauhingu_asutamine.html', osauhingu_asutamise_vorm=osauhingu_asutamise_vorm, edu_sonum=edu)