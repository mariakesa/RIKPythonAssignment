from routes import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from init_db_script import test_db

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# See rida on vajalik Flaski jaoks
# autopep8: off
from routes import *

test_db()

if __name__ == '__main__':
    app.run(debug=False)
