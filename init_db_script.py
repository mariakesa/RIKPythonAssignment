from utils import init_db
import os.path
from tests.unit_test import juhusliku_kapitali_gen_test_n


def test_db():
    check = os.path.isfile('test.db')
    if check == False:
        init_db()
        # Automaatiline unit testide kogum
        juhusliku_kapitali_gen_test_n()
