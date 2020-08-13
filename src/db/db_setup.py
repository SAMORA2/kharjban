import sqlite3
import json
import ast
import os.path


# -- intialize database

def init_db():
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id Text PRIMARY KEY not null,
        
        user_name TEXT,
        balance integer
        
        )""")

        c.execute("""CREATE TABLE IF NOT EXISTS asset (
        asset_id Text PRIMARY KEY not null ,
        amount integer ,
        category TEXT ,
        datetime TEXT,
        user_fk text 
        )""")

        # for row in c.execute('select * from users'):
        #     print(row)
        # for row in c.execute('select * from asset'):
        #     print(row)
        x = []
        y = []
        json_msg = json.dumps(c.execute('select * from asset').fetchall())
        json_msg = ast.literal_eval(json_msg)
        for items in json_msg:
            y.append(items[1])
            x.append(items[3][:11])
    except:
        pass
    finally:
        conn.commit()
        conn.close()
