import pytest

from src.db.db_operations import *
from src.spider.spider import *


@pytest.fixture(autouse=True)
def clear_all_users():
    conn = sqlite3.connect("D:\\Documents\\Projects\\PythonProjects\\finance-management\\src\\db\\db.wallet.db")
    try:
        c = conn.cursor()
        c.execute("DELETE FROM users ")
    finally:
        conn.commit()
        conn.close()


def test_add_data():
    conn = sqlite3.connect("D:\\Documents\\Projects\\PythonProjects\\finance-management\\src\\db\\db.wallet.db")
    try:

        c = conn.cursor()
        c.execute("INSERT INTO users VALUES(?,?,?)", ('sd4r', 'Sunder pichai', 97542000))
        rs = c.execute("select * from users").fetchall()

        assert len(rs) == 1
    finally:
        conn.commit()
        conn.close()


def test_check_internet():
    if requests.get("http://sanjesh.org"):
        assert check_internet() == True


def test_check_laptop():
    assert laptop_spider() == True


def test_check_crypto():
    assert crypto_spider() == True
