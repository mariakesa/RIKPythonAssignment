from app import app
from flask import render_template

@app.route('/')
@app.route('/avaleht')
def avaleht():
    return render_template('avaleht.html')