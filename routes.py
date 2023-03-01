from app import app
from flask import render_template
from forms import *

@app.route('/')
@app.route('/avaleht')
def avaleht():
    nimeline_otsing = NimelineOtsinguRiba()
    registri_numbri_otsing = RegistriOtsinguRiba()
    return render_template('avaleht.html', 
                           nimeline_otsing=nimeline_otsing, 
                           registri_numbri_otsing=registri_numbri_otsing)