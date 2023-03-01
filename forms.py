# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired 

class NimelineOtsinguRiba(FlaskForm):
    marksona=StringField('Osaühingu nimi', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')

class RegistriOtsinguRiba(FlaskForm):
    registriotsing=IntegerField('Registrinumber', validators=[DataRequired()])
    otsi=SubmitField('Otsi!')
