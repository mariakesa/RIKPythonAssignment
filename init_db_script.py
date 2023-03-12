from utils import init_db
import os.path


def test_db():
    check = os.path.isfile('test.db')
    if check == False:
        init_db()


test_db()
