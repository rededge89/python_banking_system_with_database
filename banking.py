import random

all_cards = []


class CreditCard:
    def __init__(self):
        # Luhn Validation
        cc_number = "400000" + str(random.randint(100000000, 999999999))
        cc_list = cc_number.split()
        cc_list = [int(x) for x in cc_list]
        doubled_second_digit_list = list()
        digits = list(enumerate(cc_list, start=1))
        for index, digit in digits:
            if index % 2 == 0:
                doubled_second_digit_list.append(digit * 2)
            else:
                doubled_second_digit_list.append(digit)
        sum_of_digits = 0
        for digit in digits:
            if digit > 9:
                digit -= 9
                sum_of_digits += digit
            else:
                sum_of_digits += digit
            remainder = sum_of_digits % 10
            checksum = 10 - remainder

        self.number = "400000" + str(cc_number) + str(checksum)
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
        all_cards.append(card.number)
        all_cards.append(card.pin)
        all_cards.append(card.balance)
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
        if card_number not in all_cards:
            print("Wrong card number or PIN!")
            menu1()
        elif pin != all_cards[all_cards.index(card_number) + 1]:
            print("Wrong card number or PIN!")
            menu1()
        else:
            print()
            print("You have successfully logged in!")
            print()
            menu2(all_cards.index(card_number))
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
        print(all_cards[card_index + 2])
        print()
        menu2(card_index)
    elif selection == 2:
        print()
        print("You have successfully logged out!")
        print()
        menu1()
    elif selection == 0:
        quit()


# program start
menu1()
