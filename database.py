import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
with conn:
    cur.execute('''CREATE TABLE IF NOT EXISTS card(
                        id INTEGER,
                        number text,
                        pin text,
                        balance INTEGER DEFAULT 0)''')


def insert_card(card_num, crd_pin):
    with conn:
        cur.execute('INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)', (card_num, crd_pin, 0))


def select_card(card_number, pin):
    with conn:
        cur.execute('SELECT * FROM card WHERE number = (?) AND pin = (?)', (card_number, pin))
        return cur.fetchone()
