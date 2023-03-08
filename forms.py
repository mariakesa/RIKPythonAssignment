# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, IntegerField, DateField, FormField, FieldList
from wtforms.validators import DataRequired 

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
    osauhingu_nimi=StringField('Osaühingu nimi', validators=[DataRequired()])
    registrikood=IntegerField('Registrikood', validators=[DataRequired()])
    asutamise_kuupaev= DateField('Asutamise kuupäev', validators=[DataRequired()])
    fuus_is_asutajad = FieldList(FormField(FuusIsikudVorm))
    asuta=SubmitField('Asuta osaühing')
    
