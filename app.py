from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from databases import init_db

app= Flask(__name__)
app.config['SECRET_KEY'] = "secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

from routes import *

if __name__=='__main__':
    app.run(debug=True)



