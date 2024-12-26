
import aiosqlite
from time import time
import random
import string

async def generate_string(length):
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols) for _ in range(length))
    return result


async def connect_db():
    global cs, sql
    sql=await aiosqlite.connect('data//DataBase.db')
    cs=await sql.cursor()


    await cs.execute("""CREATE TABLE IF NOT EXISTS user_data(
        user_id INTEGER PRIMARY KEY,
        user_money INTEGER,
        user_unix INTEGER,
        user_status BOOL,
        user_referal INTEGER
    )""")

    await cs.execute("""CREATE TABLE IF NOT EXISTS product_catolog(
        catolog_id TEXT PRIMARY KEY,
        catolog_name TEXT,
        catalog_discription TEXT,
        catalog_photo TEXT,
        catolog_req TEXT
    )""")

    await cs.execute("""CREATE TABLE IF NOT EXISTS product(
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        product_discription TEXT,
        product_photo TEXT,
        product_req TEXT,
        product_infinity INTEGER,
        product_price INTEGER,
        product_textbuy TEXT
    )""")

    await cs.execute("""CREATE TABLE IF NOT EXISTS history(
        history_type TEXT,
        history_id INTEGER,
        history_product TEXT,
        history_logs TEXT,
        history_sum TEXT,
        history_user INTEGER,
        history_unix INTEGER
    )""")

    await cs.execute("""CREATE TABLE IF NOT EXISTS logs(
        log_name TEXT,
        log_req TEXT
    )""")

    await cs.execute("""CREATE TABLE IF NOT EXISTS pay_settings(
        pay_name TEXT PRIMARY KEY,
        pay_onoff INTEGER,
        pay_token TEXT
    )""")

    await cs.execute("""CREATE TABLE IF NOT EXISTS chennal_data(
        chat_id INTEGER PRIMARY KEY,
        chat_link TEXT
    )""")

    try:
        await cs.execute("INSERT INTO pay_settings VALUES(?, ?, ?)", ['yoomoney', 0, 0])
        await cs.execute("INSERT INTO pay_settings VALUES(?, ?, ?)", ['lolz', 0, 0])
        await cs.execute("INSERT INTO pay_settings VALUES(?, ?, ?)", ['cryptobot', 0, 0])
    except:
        pass
    await sql.commit()


async def add_user(user_id):
    data=[user_id, 0, time(), 1, 0]
    await cs.execute("INSERT INTO user_data VALUES(?, ?, ?, ?, ?)", data)
    await sql.commit()

async def get_allusers():
    await cs.execute(f"SELECT * FROM user_data")
    return await cs.fetchall()

async def get_dataUser(user_id):
    await cs.execute(f"SELECT * FROM user_data WHERE user_id = '{user_id}'")
    return await cs.fetchall()

async def get_banUser(user_id):
    await cs.execute(f"SELECT user_status FROM user_data WHERE user_id = '{user_id}'")
    return await cs.fetchone()

async def replace_user(item, edit, user_id):
    await cs.execute(f"UPDATE user_data SET {item} = {edit} WHERE user_id = '{user_id}'")
    await sql.commit()

async def replace_balance(summ, user_id):
    await cs.execute(f"UPDATE user_data SET user_money = {summ} WHERE user_id = {user_id}")
    await sql.commit()

async def add_catalog(name, discription, photo, req):
    await cs.execute(f"SELECT * FROM product_catolog")
    catalog=await cs.fetchall()
    data=[1 if len(catalog) == 0 else int(catalog[-1][0])+1, name, discription, photo, req]
    await cs.execute("INSERT INTO product_catolog VALUES(?, ?, ?, ?, ?)", data)
    await sql.commit()

async def take_balance(summ, user_id):
    await cs.execute(f"UPDATE user_data SET user_money = user_money-{summ} WHERE user_id = {user_id}")
    await sql.commit()

async def get_balance(summ, user_id):
    await cs.execute(f"UPDATE user_data SET user_money = user_money+{summ} WHERE user_id = {user_id}")
    await sql.commit()

async def get_dataCatalog():
    await cs.execute(f"SELECT * FROM product_catolog")
    return await cs.fetchall()

async def get_catalog(ctg_id):
    await cs.execute(f"SELECT * FROM product_catolog WHERE catolog_id = '{ctg_id}'")
    return await cs.fetchall()

async def delete_catalog(ctg_id):
    await cs.execute(f"DELETE FROM product_catolog WHERE catolog_id = '{ctg_id}'")
    await sql.commit()

async def replace_catalog(item, edit, ctg_id):
    await cs.execute(f"UPDATE product_catolog SET {item} = '{edit}' WHERE catolog_id = '{ctg_id}'")
    await sql.commit()

async def get_dataProduct():
    await cs.execute(f"SELECT * FROM product")
    return await cs.fetchall()

async def add_product(name, discription, photo, req, price, buytext):
    await cs.execute(f"SELECT * FROM product")
    product=await cs.fetchall()
    data=[1 if len(product) == 0 else int(product[-1][0])+1, name, discription, photo, req, 0, price, buytext]
    await cs.execute("INSERT INTO product VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)
    await sql.commit()

async def get_product(prd_id):
    await cs.execute(f"SELECT * FROM product WHERE product_id = '{prd_id}'")
    return await cs.fetchall()

async def delete_product(prd_id):
    await cs.execute(f"DELETE FROM product WHERE product_id = '{prd_id}'")
    await sql.commit()

async def replace_product(item, edit, prd_id):
    await cs.execute(f"UPDATE product SET {item} = '{edit}' WHERE product_id = '{prd_id}'")
    await sql.commit()

async def get_log(prd_id):
    await cs.execute(f"SELECT * FROM logs WHERE log_req = '{prd_id}'")
    return await cs.fetchall()

async def add_log(log, prd_id):
    data=[log, prd_id]
    await cs.execute("INSERT INTO logs VALUES(?, ?)", data)
    await sql.commit()

async def del_log(prd_id, item='log_req'):
    data=[prd_id]
    await cs.execute(f"DELETE FROM logs WHERE {item} = '{prd_id}'")
    await sql.commit()

async def get_dataPay():
    await cs.execute(f"SELECT * FROM pay_settings")
    return await cs.fetchall()

async def get_pay(pay):
    await cs.execute(f"SELECT * FROM pay_settings WHERE pay_name = '{pay}'")
    return await cs.fetchall()

async def replace_pay(item, edit, pay):
    await cs.execute(f"UPDATE pay_settings SET {item} = '{edit}' WHERE pay_name = '{pay}'")
    await sql.commit()

async def get_history(id, item='history_id'):
    await cs.execute(f"SELECT * FROM history WHERE {item} = '{id}'")
    return await cs.fetchall()

async def add_history(typee, product, logs, summ, user_id):
    while True:
        id_history=await generate_string(8)
        if await get_history(id) == list():
            break
    data=[typee, id_history, product, logs, summ, user_id, time()]
    await cs.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?, ?, ?)", data)
    await sql.commit()
    return id_history

async def add_chennal(chat_id, link):
    data=[chat_id, link]
    await cs.execute("INSERT INTO chennal_data VALUES(?, ?)", data)
    await sql.commit()

async def get_dataChennal():
    await cs.execute(f"SELECT * FROM chennal_data")
    return await cs.fetchall()

async def delete_chennal(chat_id):
    await cs.execute(f"DELETE FROM chennal_data WHERE chat_id = '{chat_id}'")
    await sql.commit()