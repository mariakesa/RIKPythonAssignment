# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, IntegerField, DateField, FormField, FieldList
from wtforms.validators import DataRequired 

class NimelineOtsinguRiba(FlaskForm):
    marksona=StringField('Osaühingu nimi', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class RegistriOtsinguRiba(FlaskForm):
    registriotsing=IntegerField('Registrikood', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class FuusIsikudVorm(Form):
    fuus_is_asutaja = StringField('Füüsilisest isikust osanik', validators=[DataRequired()])
    fuus_is_asutaja_ik = StringField('Füüsilisest isikust osaniku isikukood', validators=[DataRequired()])

class OsauhinguAsutamiseVorm(FlaskForm):
    osauhingu_nimi=StringField('Osaühingu nimi', validators=[DataRequired()])
    registrikood=IntegerField('Registrikood', validators=[DataRequired()])
    asutamise_kuupaev= DateField('Asutamise kuupäev', validators=[DataRequired()])
    fuus_is_asutajad = FieldList(FormField(FuusIsikudVorm),min_entries=1)
    asuta=SubmitField('Asuta osaühing')
