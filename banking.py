import random
import math
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
CREATE_CARD_TABLE = '''CREATE TABLE IF NOT EXISTS card(
                        id INTEGER,
                        number text,
                        pin text,
                        balance INTEGER DEFAULT 0)'''

INSERT_CARD = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)"


class CreditCard:
    def __init__(self):
        self.number = create_luhn_valid_card_number()
        self.pin = str(random.randint(1000, 9999))
        self.balance = 0


def menu1():
    print("1. Create an account\n2. Log into account\n0. Exit")
    selection = input()
    try:
        selection = int(selection)
        if selection < 0 or selection > 2:
            print("You must enter a number between 0 - 2")
    except ValueError:
        print("You must only enter numbers")
    if selection == 1:
        card = CreditCard()
        cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", (card.number, card.pin, 0))
        conn.commit()
        print()
        print(f"Your card number: \n{card.number}\nYour card PIN:\n{card.pin}")
        print()
        menu1()
    elif selection == 2:
        print()
        print("Enter your card number:")
        card_number = str(input())
        print("Enter your PIN:")
        pin = str(input())
        authentication = conn.cursor().execute('SELECT * FROM card WHERE number = ?', (str(card_number))).fetchone()
        print(authentication)
        if authentication != None:
            print()
            print("You have successfully logged in!")
            print()
            menu2(authentication)
        else:
            print()
            print("Wrong card number or PIN!")
            print()
    elif selection == 0:
        quit()


def menu2(card_index):
    print("1. Balance\n2. Log out\n0. Exit")
    selection = input()
    try:
        selection = int(selection)
        if selection < 0 or selection > 2:
            print("You must enter a number between 0 - 2")
    except ValueError:
        print("You must only enter numbers")
    if selection == 1:
        print("Balance: " + card_index[3])
        print()
        menu2(card_index)
    elif selection == 2:
        print()
        print("You have successfully logged out!")
        print()
        menu1()
    elif selection == 0:
        quit()


def create_luhn_valid_card_number():
    cc_number = "400000" + str(random.randint(100000000, 999999999))
    cc_list = [number for number in cc_number]
    cc_list = [int(x) for x in cc_list]
    for i in range(len(cc_list)):
        if i % 2 == 0:
            cc_list[i] *= 2
            if cc_list[i] > 9:
                cc_list[i] -= 9
        if sum(cc_list) % 10 == 0:
            checksum = 0
        else:
            checksum = 10 - (sum(cc_list) % 10)
    return str(cc_number) + str(checksum)


# program start
cur.execute(CREATE_CARD_TABLE)
conn.commit()
menu1()
