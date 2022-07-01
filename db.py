import sqlite3 as sqlt


def start_db():
    base = sqlt.connect('userID_base.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS data(ID, Name, Last name)')
    base.commit()


async def db_add(id, name, l_name):
    base = sqlt.connect('userID_base.db')
    cur = base.cursor()
    cur.execute('INSERT INTO data VALUES (?, ?, ?)', (id, name, l_name))
    base.commit()
    base.close()

def db_user(id):
    base = sqlt.connect('userID_base.db')
    cur = base.cursor()
    user_id = cur.execute('SELECT * from data WHERE id = ?', (id, )).fetchone()
    base.close()
    return user_id