import sqlite3
import secrets
import string
import termtables as tt
import json
import ast
import os

from init import Person, Expense


def add_user(password, name, balance):
    if check_duplicate(password):
        p = Person(id=password, name=name, balance=balance)
        conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
        try:
            c = conn.cursor()
            c.execute("INSERT INTO users VALUES(?,?,?)", (p.id, p.name, p.balance))
        finally:
            conn.commit()
            conn.close()
            print("""\n                    ------------------
                    added successfully    :)
                    ------------------\n""")
            return True

    else:
        print("""        -----------------
        this id  existed    :(
        -----------------\n""")
        return False


def delete_user(password, name):
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    try:
        c = conn.cursor()
        c.execute("DELETE FROM users where user_id=? and user_name=?", (password, name))
        c.execute("Delete from asset where user_fk=?", [password])
    finally:
        conn.commit()
        conn.close()
        print("""\n                --------------------
                deleted successfully        Hope you come back soon :)
                --------------------\n""")


def retrieve_user(password, name):
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()
    c.execute("select * from users where user_id=? and  user_name=?", (password, name))
    items = c.fetchone()
    user_items = []
    if items:

        print('\nuser found :)\n')
        for item in items:
            user_items.append(item)
        Person(password, name, user_items[2])
        conn.commit()
        conn.close()
        return user_items[2]

    else:
        print('\nuser not found :(\n')

        conn.commit()
        conn.close()
        return False


def add_income(password, amount):
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()
    temp = ''
    for row in c.execute("select * from users where user_id =?", [password]):
        temp = row[2]
    if temp:

        c.execute(" UPDATE users set balance=? where user_id=?", (temp + amount, password))
        conn.commit()
        conn.close()
        total = temp + amount

        return total
    else:
        print('something got wrong :(')
        conn.commit()
        conn.close()


def check_duplicate(id) -> bool:
    row = ''
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()
    temp = c.execute("select * from users where user_id =?", [id])

    for row in temp:
        pass

    res = type(row) == str

    if res:
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False


def add_payment(id, name, balance, category, cost, date):
    e = Expense(id=id, name=name, balance=balance, category=category, cost=cost, date=date)
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()

    c.execute("INSERT INTO asset VALUES(?,?,?,?,?)", (pay_id_generator(), e.cost, e.category, e.date, e.id))
    c.execute(" UPDATE users set balance=? where user_id=?", (e.spend(), id))

    conn.commit()
    conn.close()

    print("""\n                ------------------
                added successfully    :)
                ------------------\n""")

    return int(balance) - int(cost)


def pay_id_generator():
    N = 7
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N))
    res = '/=' + str(res)
    return res


def show_payment(id):
    row = ''
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()
    temp = c.execute("select category,amount,datetime from asset where user_fk =?", [id])
    zero = []

    for row in temp:
        zero.append(row)

    if type(row) == str:
        print("\nNothing Found ! (NO PAYMENT)\n")
        conn.commit()
        conn.close()
        return False
    else:

        for i in range(len(zero)):
            zero[i] = (i + 1,) + zero[i]

        tbl_info = tt.to_string(
            zero,
            header=["No.", "Category", "Cost", "Date"],
            style=tt.styles.ascii_thin_double,

        )
        print(tbl_info, '\n')

        conn.commit()
        conn.close()


def visualize_asset(id):
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()

    x = []
    y = []
    z = []
    json_msg = json.dumps(c.execute('select * from asset where user_fk=?', [id]).fetchall())
    json_msg = ast.literal_eval(json_msg)

    for items in json_msg:
        y.append(items[1])
        x.append(items[3][:11])
        z.append(items[2])

    conn.commit()
    conn.close()
    return [y + x, z]


def update_pass(newId, oldId):
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()

    c.execute(" UPDATE users set user_id=? where user_id=?", (newId, oldId))
    c.execute(" UPDATE asset set user_fk=? where user_fk=?", (newId, oldId))

    conn.commit()
    conn.close()


def update_transaction(id, cost, category, date, wealth, user_id):
    try:
        conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))

        c = conn.cursor()

        c.execute(" UPDATE asset set amount=?,category=?,datetime=? where asset_id=?", (cost, category, date, id))
        c.execute("UPDATE users set balance=? where user_id=?", (wealth, user_id))

        conn.commit()
        conn.close()
        print("""\n                             --------------------
                             successfully updated :)
                             --------------------
                                                   \n""")
    except:
        print("failed to update :(")


def select_trans_row(num, id):
    row = ''
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()
    temp = c.execute("select asset_id,category,amount,datetime from asset where user_fk =?", [id])
    zero = []

    for i, row in enumerate(temp):
        if i + 1 == num:
            zero.append(row)
            break
    try:

        if type(row) == str:
            print("\nNothing Found ! (NO PAYMENT)\n")
            conn.commit()
            conn.close()
            return False
        else:

            tbl_info = tt.to_string(
                zero,
                header=["Code", "Category", "Cost", "Date"],
                style=tt.styles.ascii_thin_double,

            )
            print(tbl_info, '\n')

            conn.commit()
            conn.close()
            return zero

    except:
        print("\nWrong number  {OUT OF RANGE} :(")
        conn.commit()
        conn.close()
        return False


def delete_transaction(userId, code, newMoney):
    conn = sqlite3.connect(os.path.join('src/db/', 'db.wallet.db'))
    c = conn.cursor()

    try:
        c.execute("DELETE FROM asset where asset_id=? and user_fk=?", (code, userId))
        c.execute("UPDATE users set balance=? where user_id=?", (newMoney, userId))

        print("     \ndeleted successfully :)")

    except:
        print("     \nfailed to delete transaction :(")

    finally:

        conn.commit()
        conn.close()
