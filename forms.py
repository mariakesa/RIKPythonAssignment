# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired 

class NimelineOtsinguRiba(FlaskForm):
    marksona=StringField('Osaühingu nimi', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class RegistriOtsinguRiba(FlaskForm):
    registriotsing=IntegerField('Registrikood', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class OsauhinguAsutamiseVorm(FlaskForm):
    osauhingu_nimi=StringField('Osaühingu nimi', validators=[DataRequired()])
    registrikood=IntegerField('Registrikood', validators=[DataRequired()])
    asutamise_kuupaev= DateField('Asutamise kuupäev', validators=[DataRequired()])
    fuus_is_asutaja = StringField('Füüsilisest isikust osanik', validators=[DataRequired()])
    fuus_is_asutaja_ik = StringField('Füüsilisest isikust osaniku isikukood', validators=[DataRequired()])
    asuta=SubmitField('Asuta osaühing')
