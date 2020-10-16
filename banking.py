import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class CreditCard:
    def __init__(self):
        self.number = create_luhn_valid_card_number()
        self.pin = str(random.randint(1000, 9999))
        self.balance = 0


def insert_card(card_num, crd_pin):
    with conn:
        cur.execute('INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)', (card_num, crd_pin, 0))


def select_card(card_num, pin):
    with conn:
        cur.execute('SELECT * FROM card WHERE number = (?) AND pin = (?)', (card_num, pin))
        return cur.fetchone()


def luhn_validation(card_number):
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1

    for count in range(0, num_digits):
        digit = int(card_number[count])

        if not ((count & 1) ^ oddeven):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum = sum + digit

    return (sum % 10) == 0


def deposit_funds(card_info, deposit_amount):
    balance = int(card_info[3]) + int(deposit_amount)
    with conn:
        cur.execute('UPDATE card SET balance = (?) WHERE number = (?)', (balance, card_info[1]))


def delete_account(card_info):
    with conn:
        cur.execute("DELETE FROM card WHERE number = (?)", (card_info[1],))


def menu2(card_info):
    print_menu2 = "1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"
    while (selection := input(print_menu2)) != '0':
        card_info = select_card(card_info[1], card_info[2])
        try:
            selection = int(selection)
            if selection < 0 or selection > 5:
                print("You must enter a number between 0 - 5\n")
        except ValueError:
            print("You must only enter numbers\n")
        if selection == 1:
            print("\nBalance: " + str(card_info[3]) + "\n")
        elif selection == 2:
            income = input('Enter income:\n')
            deposit_funds(card_info, income)
            print("Income was added!\n")
        elif selection == 3:
            deposit_to = input('\nTransfer\nEnter card number:')
            with conn:
                cur.execute('SELECT * FROM card WHERE number = (?)', (deposit_to,))
                transfer_to = cur.fetchone()
            if not luhn_validation(deposit_to):
                print('Probably you made a mistake in the card number.  Please try again!')
            elif transfer_to is None:
                print('Such a card does not exist.')
            elif deposit_to == card_info[1]:
                print('Probably you made a mistake in the card number.  Please try again!')
            else:
                transfer_amount = input('Enter how much money you want to transfer:\n')
                if int(transfer_amount) > card_info[3]:
                    print('not enough money!\n')
                else:
                    deposit_funds(transfer_to, int(transfer_amount))
                    transfer_amount = int(transfer_amount) * -1
                    deposit_funds(card_info, int(transfer_amount))
        elif selection == 4:
            delete_account(card_info)
            print('\nThe account has been closed!\n')
        elif selection == 5:
            print("\nYou have successfully logged out!\n")
            return "continue"
    quit()


def create_luhn_valid_card_number():
    checksum = 0
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
with conn:
    cur.execute('''CREATE TABLE IF NOT EXISTS card(
                        id INTEGER,
                        number text,
                        pin text,
                        balance INTEGER DEFAULT 0)''')
menu1 = '1. Create an account\n2. Log into account\n0. Exit\n'
while (selection := input(menu1)) != '0':
    try:
        selection = int(selection)
        if selection < 0 or selection > 2:
            print("You must enter a number between 0 - 2\n")
    except ValueError:
        print("You must only enter numbers\n")
    if selection == 1:
        card = CreditCard()
        insert_card(card.number, card.pin)
        print(f"\nYour card number: \n{card.number}\nYour card PIN:\n{card.pin}\n")
    elif selection == 2:
        print("\nEnter your card number:")
        card_number = str(input())
        print("Enter your PIN:")
        pin = str(input())
        verify_card = select_card(card_number, pin)
        if verify_card is not None:
            print("\nYou have successfully logged in!\n")
            selection = menu2(verify_card)
        else:
            print("\nWrong card number or PIN!\n")
