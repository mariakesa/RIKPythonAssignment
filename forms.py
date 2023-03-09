# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from datetime import date
from wtforms import Form, StringField, SubmitField, IntegerField, DateField, FormField, FieldList
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired

#Vormide ja otsinguribade genereerimine
class NimelineOtsinguRiba(FlaskForm):
    marksona=StringField('Osaühingu nimi', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class RegistriOtsinguRiba(FlaskForm):
    registrikood=IntegerField('Osaühingu registrikood', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class FuusIsikudNimelineOtsing(FlaskForm):
    fuus_is_marksona=StringField('Füüsilisest isikust osaniku nimi', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class FuusIsikudIsikukoodiOtsing(FlaskForm):
    isikukood=StringField('Füüsilisest isikust osaniku isikukood', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class JuriidilisedIsikudNimelineOtsing(FlaskForm):
    juur_is_marksona=StringField('Juuridilisest osanikust isiku nimi', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class JuriidilisedIsikudRegistrikoodiOtsing(FlaskForm):
    juur_is_registrikood=IntegerField('Juuridilisest osanikust isiku registrikood', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class FuusIsikudVorm(Form):
    fuus_is_asutaja_index = StringField('Füüsilisest isikust osanik')
    fuus_is_asutaja_kapital = StringField('Füüsilisest isikust osaniku isikukood')

class OsauhinguAsutamiseVorm(FlaskForm):
    '''
    Implementeeritud osad valideerimised. Ülejäänud input valideerimised on implementeeritud routes.py's ja Javascriptis. 
    '''
    osauhingu_nimi=StringField('Osaühingu nimi', validators=[DataRequired(),Length(min=3, max=100)])
    registrikood=IntegerField('Registrikood', validators=[DataRequired(),NumberRange(min=1000000, max=9999999)])
    asutamise_kuupaev = DateField('Asutamise kuupäev', validators=[InputRequired()], format='%Y-%m-%d', default=date.today(), render_kw={"max": date.today().strftime('%Y-%m-%d')})
    fuus_is_asutajad = FieldList(FormField(FuusIsikudVorm))
    asuta=SubmitField('Asuta osaühing')
    
